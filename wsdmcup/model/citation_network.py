"""
Representation of the citation network (papers & citations)
"""

import math
import logging
import datetime

import numpy as np
import pandas
from scipy import sparse
from scipy.sparse import csgraph

__author__ = 'damirah'
__email__ = 'damirah@live.com'


class CitationNetwork(object):

    def __init__(self, nodes, edges):
        """
        :param edges: scipy.sparse.csr_matrix
        :return: None
        """
        self.nodes = nodes
        self.edges = edges
        self.logger = logging.getLogger(__name__)

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges

    def _delete_rows_csr(self, mat, indices):
        """
        Return a copy or matrix 'mat' with rows denoted by 'indices' removed.
        :param mat: scipy.sparse.csr_matrix
        :param indices: list of indices to be removed
        :return: scipy.sparse.csr_matrix with 'indices' rows removed
        """
        self.logger.debug('Removing %s rows from edge matrix', len(indices))
        if not isinstance(mat, sparse.csr_matrix):
            raise ValueError("works only for CSR format -- use .tocsr() first")
        indices = list(indices)
        mask = np.ones(mat.shape[0], dtype=bool)
        mask[indices] = False
        return mat[mask]

    def _remove_erroneous_years(self, arr):
        """
        Check which nodes have a missing or future year of publication and
        remove data of these nodes from 'arr'.
        :param arr: numpy.array from which to remove data from erroneous years
        :return: numpy.array 'arr' with erroneous years removed
        """
        year = datetime.date.today().year
        self.logger.info('Finding erroneous (missing or future) publish years')
        missing_year = np.array(self.nodes['publish_year'].isnull())
        future_year = np.array(self.nodes['publish_year'] > year)
        self.logger.debug('Found %s papers with missing year of publication '
                          'and %s papers with future year of publication',
                          np.sum(missing_year), np.sum(future_year))
        self.logger.debug('Removing data for erroneous years')
        arr[missing_year] = 0
        arr[future_year] = 0
        self.logger.info('Done removing erroneous data from array, returning')
        return arr

    def get_total_references(self):
        """
        :return: numpy.array with list of total reference counts per paper
        """
        self.logger.info('Counting total references per paper')
        total_references = self._remove_erroneous_years(
            np.array(self.edges.sum(axis=1).ravel().tolist()[0]))
        self.logger.debug('Least and most references: %s, %s',
                          min(total_references), max(total_references))
        return total_references

    def get_total_citations(self, limit=None, mult=None):
        """
        :param mult:
        :param limit:
        :return: list of total citation counts per paper
        """
        year = datetime.date.today().year
        self.logger.info('Counting total citations per paper until %s', year)
        total_citations = np.array(
            self.edges.sum(axis=0).ravel().tolist()[0])

        self.logger.info('Finding erroneous (missing or future) publish years')
        missing_year = np.array(self.nodes['publish_year'].isnull())
        future_year = np.array(self.nodes['publish_year'] > year)
        self.logger.debug('Found %s papers with missing year of publication '
                          'and %s papers with future year of publication',
                          np.sum(missing_year), np.sum(future_year))
        self.logger.debug('Removing citation data for erroneous years')
        total_citations[missing_year] = 0
        total_citations[future_year] = 0
        self.logger.debug('Most citations received: %s', max(total_citations))
        if limit:
            self.logger.info('Limiting total citations to <= %s', limit)
            above_limit = total_citations > limit
            self.logger.info('This will affect %s papers', sum(above_limit))
            if not mult:
                mult = 1
            self.logger.info('Multiplying log by %s', mult)
            # total_citations[above_limit] = (
            #     mult * (
            #         np.log10(total_citations[above_limit] - (limit - 1))
            #     ) +
            #     limit)
            total_citations[above_limit] = limit
            total_citations = np.nan_to_num(total_citations)
            self.logger.info('After applying limit, mix and max is %s, %s',
                             min(total_citations), max(total_citations))
        self.logger.info('Done, returning data')
        return total_citations

    def get_total_citations_with_time_decay(self):
        """
        :return:
        """
        alpha = 0.1
        self.logger.info('Counting total citations with exponential time '
                         'decay using parameter alpha=%s', alpha)
        year = datetime.date.today().year
        publish_years = np.array(self.nodes['publish_year'])
        self.logger.debug('Correcting papers with future publish year')
        publish_years[publish_years > year] = year
        self.logger.debug('Converting citation matrix to CSC format')
        # this makes a copy
        citation_matrix = self.edges.tocsc()
        self.logger.debug('Finding paper age')
        citation_matrix.data = publish_years[citation_matrix.indices]
        citation_matrix.data = year - citation_matrix.data
        self.logger.debug('Applying exponential decay function to paper age')
        citation_matrix.data = np.exp(-alpha * citation_matrix.data)
        self.logger.debug('Summing citations per paper')
        total_citations = np.array(
            citation_matrix.sum(axis=0).ravel().tolist()[0])
        self.logger.debug('Least and most cited paper: %s, %s',
                          min(total_citations), max(total_citations))
        self.logger.info('Done counting total citations, returning data')
        return total_citations

    def get_paper_age(self):
        """
        :return:
        """
        year = datetime.date.today().year
        self.logger.info('Counting paper age in %s', year)
        self.logger.debug('Finding erroneous (missing or future) publish years')
        missing_year = np.array(self.nodes['publish_year'].isnull())
        future_year = np.array(self.nodes['publish_year'] > year)
        self.logger.debug('Fixing erroneous years in DataFrame')
        publish_year = np.array(self.nodes['publish_year'])
        publish_year[missing_year] = year
        publish_year[future_year] = year
        self.logger.debug('Counting paper age')
        age = year - publish_year + 1
        self.logger.debug('Min paper age: %s, max paper age: %s',
                          min(age), max(age))
        self.logger.info('Done counting, returning data')
        return age

    def get_citation_per_year(self, time_decay=True):
        """
        :param time_decay:
        :return:
        """
        self.logger.info('Counting citations per paper and paper age')
        if time_decay:
            paper_citations = self.get_total_citations_with_time_decay()
        else:
            paper_citations = self.get_total_citations()
        age = self.get_paper_age()
        self.logger.info('Counting mean citation per year')
        mean_citation = paper_citations / age
        self.logger.debug('Min and max citation per year: %s, %s ',
                          min(mean_citation), max(mean_citation))
        self.logger.info('Done counting, returning data')
        return mean_citation

    def get_cc(self):
        """
        :return:
        """
        return csgraph.connected_components(self.edges, directed=True,
                                            connection='weak',
                                            return_labels=True)
