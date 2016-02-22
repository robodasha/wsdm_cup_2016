"""
Class for reading and writing CSV files in MAG format.
"""

import csv
from csv import QUOTE_NONE
import logging

import numpy
import pandas
from scipy import sparse

import wsdmcup.logging as wsdmlog

__author__ = 'damirah'
__email__ = 'damirah@live.com'


class Mag(object):
    """
    CSV dialect class with settings for reading and writing
    the Microsoft Academic Graph TSV files.
    When creating a CSV reader of writer, pass this
    to the reader/writer as dialect= parameter.
    E.g.
    from wsdmcup.data.csv_dialect import Mag
    csv_reader = csv.reader(file_path, dialect=Mag)
    """
    delimiter = '\t'
    quotechar = None
    escapechar = None
    doublequote = False
    skipinitialspace = False
    lineterminator = '\n'
    quoting = QUOTE_NONE


class CsvDatastore(object):
    """
    Class for reading MAG data files
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def read_csv(self, csv_path):
        """
        Read CSV (TSV) using MAG dialect
        :param csv_path: path to CSV to be read
        :return: generator
        """
        self.logger.info('Reading file %s', csv_path)
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, dialect=Mag)
            for csv_row in csv_reader:
                yield csv_row

    def load_dataframe(self, fpath, index_cols):
        """
        Load DataFrame from specified CSV file
        :param fpath: path to the file to be loaded
        :param index_cols: list of indexes of columns to be used as index
        :return: pandas.DataFrame
        """
        return pandas.DataFrame.from_csv(fpath, sep=Mag.delimiter,
                                         index_col=index_cols)

    def store_dataframe(self, data, fpath, columns):
        """
        Store pandas DataFrame in CSV in temp_files directory
        :param data: the data frame to be stored
        :param fpath: path to the output CSV file
        :param columns: which columns to store in the file
        :return: None
        """
        self.logger.info('Storing DataFrame in %s', fpath)
        data.to_csv(fpath, sep=Mag.delimiter, columns=columns, header=True,
                    index=True, line_terminator=Mag.lineterminator,
                    quoting=Mag.quoting)

    def store_results(self, data, fpath, columns):
        """
        Store DataFrame in results format
        :param data: pandas.DataFrame
        :param fpath:
        :param columns:
        :return:
        """
        self.logger.info('Storing results in %s', fpath)
        data.to_csv(fpath, sep=Mag.delimiter, header=False, index=False,
                    float_format='%.5e', columns=columns,
                    line_terminator=Mag.lineterminator, quoting=Mag.quoting,
                    quotechar=Mag.quotechar, doublequote=Mag.doublequote,
                    escapechar=Mag.escapechar)

    def csv_to_dataframe(self, csv_path, csv_mapping, load_cols,
                         index_col, id_col):
        """
        Load MAG TSV file into DataFrame
        :param csv_path:
        :param csv_mapping:
        :param load_cols:
        :param index_col:
        :param id_col:
        :return: pandas.DataFrame
        """
        self.logger.info('Loading data from %s', csv_path)
        self.logger.debug('Columns to be loaded: %s', load_cols)

        # for printing progress
        processed = 0
        self.logger.debug('Checking the number of rows to be loaded')
        total = wsdmlog.get_total(csv_path)
        self.logger.debug('Total: %s', total)
        how_often = wsdmlog.how_often(total)

        data = []
        self.logger.info('Processing CSV')
        for csv_row in self.read_csv(csv_path):
            data.append({col: csv_row[csv_mapping[col].value]
                         if csv_row[csv_mapping[col].value].isdigit() or
                            not csv_row[csv_mapping[col].value]
                         else csv_row[csv_mapping[col].value].encode()
                         for col in load_cols})
            processed += 1
            if processed % how_often == 0:
                self.logger.debug(wsdmlog.get_progress(processed, total))

        self.logger.info('Converting to DataFrame')
        df = pandas.DataFrame(data)

        self.logger.info('Adding index to DataFrame')
        df[index_col] = df.index
        df.index = [numpy.array(df[id_col]), numpy.array(df[index_col])]
        df.index.names = [id_col, index_col]
        self.logger.info('Indexing done')
        return df

    def csv_to_relation_matrix(self, fpath, row_id_csv_col, row_map,
                               col_id_csv_col, col_map,
                               data_csv_col=None, data_map=None):
        """
        Build authorship matrix from list of edges in PaperReferences.txt file
        :return: scipy.sparse.csr_matrix
        """
        self.logger.info('Got list of %s row indices and %s column indices',
                         len(row_map), len(col_map))

        # for updating progress
        processed = 0
        self.logger.debug('Checking the number of rows to be loaded')
        total = wsdmlog.get_total(fpath)
        self.logger.debug('Total: %s', total)
        how_often = wsdmlog.how_often(total)

        append_data = data_csv_col is not None

        row_indices = []
        col_indices = []
        data = []

        self.logger.info('Loading data from %s', fpath)
        for line in self.read_csv(fpath):
            row_id = line[row_id_csv_col]
            col_id = line[col_id_csv_col]
            if not row_id or not col_id:
                processed += 1
                if processed % how_often == 0:
                    self.logger.debug(wsdmlog.get_progress(processed, total))
                continue

            # appending data ===================================================

            if append_data:
                data_value = line[data_csv_col]
                if not data_value:
                    processed += 1
                    if processed % how_often == 0:
                        self.logger.debug(
                            wsdmlog.get_progress(processed, total))
                    continue
                if data_map:
                    data.append(data_map[data_value])
                else:
                    data.append(data_value)

            # not appending data ===============================================

            else:
                data.append(1)

            # both cases =======================================================

            row_indices.append(row_map[row_id])
            col_indices.append(col_map[col_id])
            processed += 1
            if processed % how_often == 0:
                self.logger.debug(wsdmlog.get_progress(processed, total))

        self.logger.info('Loaded {0}, {1} references'
                         .format(len(row_indices), len(col_indices)))
        self.logger.info('Constructing sparse matrix from the reference list')
        rel_matrix = sparse.coo_matrix((data, (row_indices, col_indices)),
                                       shape=(len(row_map), len(col_map)),
                                       dtype=numpy.uint32)
        self.logger.info('Relation matrix filled!')
        self.logger.debug('Number of items %s', rel_matrix.nnz)
        self.logger.info('Converting to CSR format')
        csr_m = rel_matrix.tocsr()
        # the previous line makes a copy, so for saving memory
        del rel_matrix
        self.logger.info('Done converting')
        return csr_m
