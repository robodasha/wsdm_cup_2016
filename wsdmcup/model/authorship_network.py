"""
Representation of authorship network (authors, papers, authorship information
and citation information)
"""

import logging

import numpy as np

import wsdmcup.logging as wsdmlog

__author__ = 'damirah'
__email__ = 'damirah@live.com'


def h_index_fast(citations):
    """
    :param citations: numpy.array
    :return:
    """
    if not citations.size:
        return 0
    num_items = len(citations)
    counts = np.zeros(shape=num_items + 1, dtype=np.int32)
    for i in range(0, num_items):
        counts[min(num_items, citations[i])] += 1
    total = 0
    for i in range(num_items, 0, -1):
        total += counts[i]
        if total >= i:
            return i
    return 0


class AuthorshipNetwork(object):

    def __init__(self, authors, auth_net, cit_net):
        """
        :param authors: pandas.DataFrame
        :param auth_net: scipy.sparse.csr_matrix
        :param cit_net: wsdmcup.model.CitationNetwork
        :return:
        """
        self.authors = authors
        self.auth_net = auth_net
        self.cit_net = cit_net
        self.logger = logging.getLogger(__name__)

    def get_num_docs_per_author(self):
        """
        :return:
        """
        self.logger.info('Counting total documents per author')
        total_docs = np.array(self.auth_net.sum(axis=0).ravel().tolist()[0])
        self.logger.debug('Authors with least and most documents: %s, %s',
                          min(total_docs), max(total_docs))
        self.logger.info('Done counting author documents, returning data')
        return total_docs

    def get_total_references_per_author(self):
        """
        :return:
        """
        self.logger.info('Counting total references per document')
        ref_per_doc = self.cit_net.get_total_references()
        self.logger.info('Counting total references per author')
        self.logger.debug('Copying authorship matrix')
        auth_ref = self.auth_net.tocoo(copy=True).tocsc()
        self.logger.debug('Updating authorship matrix data')
        auth_ref.data = ref_per_doc[auth_ref.indices]
        auth_ref.eliminate_zeros()
        self.logger.debug('Summing references per author')
        total_ref = auth_ref.sum(axis=0).ravel().tolist()[0]
        self.logger.debug('Authors with least and most references: %s, %s',
                          min(total_ref), max(total_ref))
        self.logger.info('Done counting author references, returning data')
        return total_ref

    def get_total_citations_per_author(self, time_decay=False, limit=None):
        """
        :return:
        """
        self.logger.info('Counting total citations per document')
        if time_decay:
            cit_per_doc = np.array(
                self.cit_net.get_total_citations_with_time_decay())
        else:
            cit_per_doc = np.array(self.cit_net.get_total_citations())
        if limit is not None:
            cit_per_doc[cit_per_doc > limit] = 0
        self.logger.info('Counting total citations per author')
        self.logger.debug('Copying authorship matrix')
        auth_cit = self.auth_net.tocoo(copy=True).tocsc()
        auth_cit.data = cit_per_doc[auth_cit.indices]
        auth_cit.eliminate_zeros()
        self.logger.debug('Summing citations per author')
        total_cit = auth_cit.sum(axis=0).ravel().tolist()[0]
        self.logger.debug('Least and most cited authors: %s, %s',
                          min(total_cit), max(total_cit))
        self.logger.info('Done counting author citations, returning data')
        return total_cit

    def get_mean_citations_per_author(self, time_decay=False, limit=None):
        """
        :param time_decay:
        :param limit:
        :return:
        """
        self.logger.info('Counting total citations per author')
        total_author_cit = self.get_total_citations_per_author(
            time_decay=time_decay, limit=limit)
        self.logger.info('Counting number of publications per author')
        total_author_pub = self.get_num_docs_per_author()
        self.logger.info('Counting number of citations per author publication')
        mean_author_cit = total_author_cit / total_author_pub
        self.logger.debug('Min and max mean author citation: %s, %s',
                          min(mean_author_cit), max(mean_author_cit))
        self.logger.info('Done counting, returning data')
        return mean_author_cit

    def get_num_authors_per_paper(self):
        """
        :return: number of authors per paper
        """
        self.logger.info('Counting number of authors per paper')
        num_authors = self.auth_net.sum(axis=1).ravel().tolist()[0]
        self.logger.debug('Least and most authors on a paper: %s, %s',
                          min(num_authors), max(num_authors))
        self.logger.info('Done counting, returning data')
        return num_authors

    def get_most_author_cit_per_paper(self):
        """
        :return:
        """
        author_citations = np.array(self.get_total_citations_per_author())
        self.logger.info('Finding most cited author for each paper')
        authorship_matrix = self.auth_net.copy()
        authorship_matrix.data = author_citations[authorship_matrix.indices]
        authorship_matrix.eliminate_zeros()
        max_cited_authors = np.zeros(len(self.cit_net.get_nodes()))
        maxs = authorship_matrix.max(axis=1)
        max_cited_authors[maxs.row] = maxs.data
        self.logger.debug('Least and most cited max authors %s, %s',
                          min(max_cited_authors), max(max_cited_authors))
        self.logger.info('Done counting, returning data')
        return max_cited_authors

    def get_author_sum_per_paper(self, time_decay=False, limit=None,
                                 mean=False):
        """
        :param time_decay:
        :param limit:
        :param mean:
        :return:
        """
        if mean:
            author_citations = np.array(
                self.get_mean_citations_per_author(time_decay, limit))
        else:
            author_citations = np.array(
                self.get_total_citations_per_author(time_decay, limit))
        self.logger.info('Counting total citations to authors of each paper')
        authorship_matrix = self.auth_net.copy()
        authorship_matrix.data = author_citations[authorship_matrix.indices]
        authorship_matrix.eliminate_zeros()
        total_auth_cit = authorship_matrix.sum(axis=1).ravel().tolist()[0]
        self.logger.debug('Least and most citations per all authors %s, %s',
                          min(total_auth_cit), max(total_auth_cit))
        self.logger.info('Done counting, returning data')
        return total_auth_cit

    def get_mean_author_citations_per_paper(self, time_decay=False, limit=None):
        """
        :return:
        """
        self.logger.info('Getting number of authors per paper')
        num_authors = np.array(self.get_num_authors_per_paper())
        self.logger.info('Getting sum of author citations per paper')
        sum_citations = np.array(
            self.get_author_sum_per_paper(time_decay, limit))
        self.logger.info('Counting mean author citations per paper')
        mean_citations = sum_citations / num_authors
        self.logger.debug('Min and max mean author citations: %s, %s',
                          min(mean_citations), max(mean_citations))
        self.logger.info('Done couting, returning data')
        return mean_citations

    def get_h_index(self):
        """
        :return: numpy.array with h_index value per author
        """
        self.logger.info('Counting author h-index')
        self.logger.debug('Copying the paper-author matrix as CSC matrix')
        paper_author_m = self.auth_net.copy().tocsc()
        paper_author_m.sort_indices()
        self.logger.debug('Replacing matrix data with paper citation data')
        cit_per_doc = np.array(self.cit_net.get_total_citations())
        paper_author_m.data = cit_per_doc[paper_author_m.indices]
        paper_author_m.eliminate_zeros()
        self.logger.debug('Iterating over columns and calculating h-index')
        total = paper_author_m.shape[1]
        how_often = wsdmlog.how_often(total)
        author_h_index = np.zeros(total)
        for i in range(0, paper_author_m.shape[1]):
            author_citations = paper_author_m.getcol(i).data
            author_h_index[i] = h_index_fast(author_citations)
            if i % how_often == 0:
                self.logger.debug(wsdmlog.get_progress(i, total))
        return author_h_index

    def _get_author_h_index_matrix(self, author_h_index):
        """
        :param author_h_index: numpy.array with author h-index values
        :return: scipy.sparse.csr_matrix
        """
        self.logger.debug('Copying paper authorship matrix')
        authorship_matrix = self.auth_net.copy()
        self.logger.debug('Replacing matrix data with h-index values')
        authorship_matrix.data = author_h_index[authorship_matrix.indices]
        authorship_matrix.eliminate_zeros()
        self.logger.debug('Done replacing, returning matrix')
        return authorship_matrix

    def get_mean_h_index_per_paper(self, author_h_index):
        """
        :param author_h_index: numpy.array
        :return: numpy.array
        """
        self.logger.info('Calculating mean author h-index per paper')
        self.logger.debug('Getting number of authors per paper')
        num_authors = np.array(self.get_num_authors_per_paper())
        self.logger.debug('Getting sum of author h-index values per paper')
        total_h_index = self.get_sum_h_index_per_paper(author_h_index)
        self.logger.debug('Counting mean author h-index per paper')
        mean_h_index = total_h_index / num_authors
        self.logger.debug('Min and max mean h-index per paper: %s, %s',
                          min(mean_h_index), max(mean_h_index))
        self.logger.info('Done calculating, returning data')
        return mean_h_index

    def get_max_h_index_per_paper(self, author_h_index):
        """
        :param author_h_index: numpy.array
        :return: numpy.array
        """
        self.logger.info('Finding max h-index per paper')
        authorship_matrix = self._get_author_h_index_matrix(author_h_index)
        max_h_index = np.zeros(authorship_matrix.shape[0])
        maxs = authorship_matrix.max(axis=1)
        max_h_index[maxs.row] = maxs.data
        self.logger.debug('Min and max h-index per paper: %s, %s',
                          min(max_h_index), max(max_h_index))
        return max_h_index

    def get_sum_h_index_per_paper(self, author_h_index):
        """
        :param author_h_index: numpy.array
        :return: numpy.array
        """
        self.logger.info('Finding total h-index per paper')
        authorship_matrix = self._get_author_h_index_matrix(author_h_index)
        sum_h_index = authorship_matrix.sum(axis=1).ravel().tolist()[0]
        self.logger.debug('Min and max total h-index per paper: %s, %s',
                          min(sum_h_index), max(sum_h_index))
        return sum_h_index
