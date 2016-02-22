"""
Module offering methods for direct access to the HDF5 data file.
This module provides universal load and store methods.
"""

import logging

import numpy
import pandas
import tables
from scipy import sparse

import wsdmcup.logging as wsdmlog
from wsdmcup.config import Config
from wsdmcup.data.csv_datastore import CsvDatastore

__author__ = 'damirah'
__email__ = 'damirah@live.com'


class Hdf5Datastore(object):
    """
    Class for storing and loading data to and from the HDF5 data file.
    """

    def __init__(self, datastore_fname = Config.DATASTORE_FNAME):
        self.datastore_path = Config.get_path_to_hdf5_file(datastore_fname)
        self.logger = logging.getLogger(__name__)

    def get_datastore_path(self):
        """
        Get location of the HDF5 file with data.
        :return: absolute path as string
        """
        return self.datastore_path

    def _remove_node(self, ds, name):
        """
        Remove node from datastore
        :param ds: pointer to datastore to remove node from
        :param name: node name
        :return: None
        """
        try:
            self.logger.debug('Trying to remove node %s', name)
            ds.remove_node(ds.root, name=name)
            self.logger.debug('Node %s was removed', name)
        except tables.NoSuchNodeError:
            self.logger.debug('Node %s not found', name)

    def store_array(self, arr, name):
        """
        Store an array in hdf5
        :param arr:
        :param name:
        :return:
        """
        with tables.open_file(self.datastore_path, 'a') as ds:
            self._remove_node(ds, name)
            atom = tables.Atom.from_dtype(arr.dtype)
            ds_array = ds.create_carray(ds.root, name, atom, arr.shape)
            self.logger.debug('Created array %s', name)
            ds_array[:] = arr

    def load_array(self, name):
        """
        :param name:
        :return:
        """
        with tables.open_file(self.datastore_path) as ds:
            arr = getattr(ds.root, name).read()
        return arr

    def store_sparse_matrix(self, matrix, name):
        """
        Store sparse matrix in HDF5 datastore. Matrix has to be of type
        scipy.sparse.csr_matrix.
        :param matrix: the matrix to be stored
        :param name: name of the node in the HDF5 datastore under which to
                     store the matrix
        :return: None
        """
        msg = "The matrix has to be in CSR format"
        assert(sparse.isspmatrix_csr(matrix)), msg
        with tables.open_file(self.datastore_path, 'a') as ds:
            for par in ('data', 'indices', 'indptr', 'shape'):
                full_name = '%s_%s' % (name, par)
                self._remove_node(ds, full_name)
                arr = numpy.array(getattr(matrix, par))
                atom = tables.Atom.from_dtype(arr.dtype)
                ds_array = ds.create_carray(ds.root, full_name, atom, arr.shape)
                self.logger.debug('Created array %s', full_name)
                ds_array[:] = arr

    def load_sparse_matrix(self, name):
        """
        Load sparse matrix from HDF5 datastore.
        :param name: node from which to load the matrix
        :return: scipy.sparse.csr_matrix
        """
        with tables.open_file(self.datastore_path) as ds:
            pars = []
            for par in ('data', 'indices', 'indptr', 'shape'):
                pars.append(getattr(ds.root, '%s_%s' % (name, par)).read())
        # it's necessary to tell scipy explicitly the datatype of the matrix
        # otherwise when summing rows/columns of the matrix the result might
        # overflow!! (because in the HDF5 store the matrix is stored
        # as numpy.int8 matrix)
        matrix = sparse.csr_matrix(tuple(pars[:3]), shape=pars[3],
                                   dtype=numpy.uint32)
        return matrix

    def store_dataframe(self, df, name, description):
        """
        :param df: pandas.DataFrame
        :param name: node in which to store the dataframe
        :return: None
        """
        self.logger.debug('Checking the number of rows to be stored')
        total = len(df)
        self.logger.debug('Total: %s', total)
        with tables.open_file(self.datastore_path, 'a') as ds:
            # first remove old node
            self._remove_node(ds, name)
            # then create again
            table = ds.create_table(ds.root, name,
                                    description=description,
                                    expectedrows=total)
            self.logger.debug('Created table %s', name)
            self.logger.info('Storing dataframe in table')
            self.logger.debug('Converting dataframe to list of tuples')
            data = [tuple(x) for x in df.values]
            self.logger.debug('Storing data in dataframe')
            table.append(data)
            self.logger.info('Storing done')
        return

    def store_table(self, name, description, csv_path, csv_mapping):
        """
        Read CSV file line by line and store the data in HDF5 data store
        :param name: name of the table
        :param description: instance of tables.IsDescription, class describing
                            the columns of the table (number, data types, etc.)
        :param csv_path: path to the input CSV file
        :param csv_mapping: Enum instance containing mapping of the HDF5
                            table description columns to the CSV columns
                            (for each column in 'description' this should
                            contain index of the column in the input CSV)
        :return: how many rows were stored in the datastore
        """
        msg = ("The descriptor parameter has to be instance "
               "of tables.IsDescription class")
        assert(issubclass(description, tables.IsDescription)), msg

        msg = "No intersection between HDF5 description and CSV mapping"
        assert(len(set([i.name for i in csv_mapping])
                   .intersection(description.columns)) > 0), msg

        row_index = 0
        self.logger.debug('Checking the number of rows to be stored')
        total = wsdmlog.get_total(csv_path)
        self.logger.debug('Total: %s', total)
        how_often = wsdmlog.how_often(total)

        with tables.open_file(self.datastore_path, 'a') as ds:
            # first remove old node
            self._remove_node(ds, name)
            # then create again
            table = ds.create_table(ds.root, name,
                                    description=description,
                                    expectedrows=total)
            self.logger.debug('Created table %s', name)
            hdf_row = table.row
            # iterate over csv and write it in the table line by line
            csv_datastore = CsvDatastore()
            for csv_row in csv_datastore.read_csv(csv_path):
                for column in description.columns:
                    if hasattr(csv_mapping, column):
                        csv_col_index = getattr(csv_mapping, column).value
                        hdf_row[column] = str.encode(csv_row[csv_col_index])
                    elif column.endswith('_index'):
                        hdf_row[column] = row_index
                hdf_row.append()
                table.flush()
                row_index += 1
                if row_index % how_often == 0:
                    self.logger.debug(wsdmlog.get_progress(row_index, total))

        return row_index

    def load_table(self, name):
        """
        Load specified table into pandas DataFrame
        :param name: table name
        :return: pandas.DataFrame with the table data
        """
        with tables.open_file(self.datastore_path, 'r') as ds:
            table = getattr(ds.root, name)
            return pandas.DataFrame.from_records(table.read())
