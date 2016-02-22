
import logging

import numpy as np


__author__ = 'damirah'
__email__ = 'damirah@live.com'


class FoSNetwork(object):

    def __init__(self, citation_network, fos_m):
        self.logger = logging.getLogger(__name__)
        self.cit_net = citation_network
        self.fos_m = fos_m

    def get_fos_publications(self):
        """
        :return: numpy.array with number of publications per field of study
        """
        self.logger.info('Counting number of papers per field of study')
        num_pub = self.fos_m.sum(axis=0).ravel().tolist()[0]
        self.logger.info('Least and most papers per field of study: %s, %s',
                         min(num_pub), max(num_pub))
        return np.array(num_pub)

    def get_paper_fos_count(self):
        """
        :return: numpy.array with number of publications per field of study
        """
        self.logger.info('Counting number of fields of study per paper')
        num_fos = self.fos_m.sum(axis=1).ravel().tolist()[0]
        self.logger.info('Least and most fields of study per paper: %s, %s',
                         min(num_fos), max(num_fos))
        return np.array(num_fos)

    def get_paper_fos_publication_matrix(self):
        """
        :return: scipy.sparse.csr_matrix with number of publications talking
                 about the fields of study
        """
        fos_pub = self.get_fos_publications()
        self.logger.debug('Copying paper-field of study matrix as CSR matrix')
        fos_pub_m = self.fos_m.tocsr().copy()
        self.logger.debug('Replacing matrix data with field publication counts')
        fos_pub_m.data = fos_pub[fos_pub_m.indices]
        self.logger.info('Least and most publications: %s, %s',
                         fos_pub_m.min(), fos_pub_m.max())
        return fos_pub_m

    def get_fos_citations(self):
        """
        :return: numpy.array with citation score for each venue
        """
        self.logger.info('Counting sum of citations per field of study')
        self.logger.debug('Counting citations per paper')
        cit_per_paper = np.array(self.cit_net.get_total_citations())
        self.logger.debug('Copying paper-field of study matrix as CSC matrix')
        fos_cit_m = self.fos_m.tocsc().copy()
        self.logger.debug('Replacing matrix with citation data and summing')
        fos_cit_m.data = cit_per_paper[fos_cit_m.indices]
        fos_cit = fos_cit_m.sum(axis=0).ravel().tolist()[0]
        self.logger.info('Least and most cited fields of study: %s, %s',
                         min(fos_cit), max(fos_cit))
        return fos_cit

    def get_paper_fos_citations(self, subtract=False, mean_per_field=False,
                                mean_per_paper=False):
        """
        :param subtract: whether to subtract citations received by a paper
                         from the field of study total, e.g. if paper X was
                         talking about field Y, the field Y was cited 300 times
                         in total and the paper 45 times, then the result for
                         the paper will be 300-45=255
        :param mean_per_field: whether to retrieve sum of citation per field of study
                     (mean=False) or mean citations per paper talking about
                     the topic (mean=True). When 'mean' is set to True, the
                     retrieved values are equal to Impact Factor for the field
                     of study with time frame equal to age of the field
                     (rather than past X years)
        :return: numpy.array with a value for each paper
        """
        fos_cit = np.array(self.get_fos_citations())
        self.logger.debug('Copying paper-field of study matrix as CSR matrix')
        fos_cit_m = self.fos_m.tocsr().copy()
        self.logger.debug('Replacing matrix data with field citation data')
        fos_cit_m.data = fos_cit[fos_cit_m.indices]

        if subtract:
            self.logger.info('Subtracting paper citations from field citation')
            self.logger.debug('Loading total citations per paper')
            paper_citations = np.array(self.cit_net.get_total_citations())
            self.logger.debug('Copying paper-fields matrix as CSC matrix')
            paper_cit_m = self.fos_m.tocsc().copy()
            self.logger.debug('Replacing paper-field matrix with paper '
                              'citation data')
            paper_cit_m.data = paper_citations[paper_cit_m.indices]
            self.logger.debug('Converting the matrix to CSR format')
            paper_cit_m = paper_cit_m.tocsr()
            self.logger.info('Subtracting paper citations from field citations')
            fos_cit_m.data = fos_cit_m.data - paper_cit_m.data
            fos_cit_m.data[fos_cit_m.data < 0] = 0
            self.logger.info('After subtracting paper citations min and max is '
                             '%s, %s', fos_cit_m.min(), fos_cit_m.max())

        if mean_per_field:
            self.logger.info('Dividing field citations by number of papers')
            num_pub = self.get_paper_fos_publication_matrix()
            if subtract:
                num_pub.data = num_pub.data - 1
            # to avoid division by zero
            num_pub.data[num_pub.data <= 0] = 1
            # both matrices are in CSR format so this should be OK
            fos_cit_m.data = fos_cit_m.data / num_pub.data
            self.logger.info('Min and max mean field citations per pub: %s, %s',
                             fos_cit_m.min(), fos_cit_m.max())

        if mean_per_paper:
            self.logger.debug('Counting mean per paper')
            fos_cit_per_paper = fos_cit_m.sum(axis=1).ravel().tolist()[0]
            fos_num_per_paper = self.get_paper_fos_count()
            fos_num_per_paper[fos_num_per_paper <= 0] = 1
            mean_cit_per_paper = fos_cit_per_paper / fos_num_per_paper
            self.logger.info('Least and most citations: %s, %s',
                             min(mean_cit_per_paper), max(mean_cit_per_paper))
            return np.array(mean_cit_per_paper)
        else:
            fos_cit_per_paper = fos_cit_m.sum(axis=1).ravel().tolist()[0]
            self.logger.info('Least and most citations: %s, %s',
                             min(fos_cit_per_paper), max(fos_cit_per_paper))
            return np.array(fos_cit_per_paper)
