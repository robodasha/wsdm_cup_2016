
import logging

import numpy as np


__author__ = 'damirah'
__email__ = 'damirah@live.com'


class AffiliationNetwork(object):

    def __init__(self, aff_m, paper_aff_m, cit_net):
        self.logger = logging.getLogger(__name__)
        self.aff_m = aff_m
        self.paper_aff_m = paper_aff_m
        self.cit_net = cit_net

    def get_citations_per_affiliation(self):
        """
        :return: numpy.array
        """
        self.logger.info('Finding sum of citations per affiliation')
        self.logger.debug('Counting citations per paper')
        cit_per_paper = np.array(self.cit_net.get_total_citations())
        self.logger.debug('Copying paper-affiliation matrix')
        aff_cit_m = self.paper_aff_m.tocsc()
        self.logger.debug('Replacing matrix with citation data and summing')
        aff_cit_m.data = cit_per_paper[aff_cit_m.indices]
        cit_per_aff = aff_cit_m.sum(axis=0).ravel().tolist()[0]
        self.logger.debug('Least and most cited affiliation: %s, %s',
                          min(cit_per_aff), max(cit_per_aff))
        self.logger.debug('Done counting citations per affiliation, returning')
        return np.array(cit_per_aff)

    def get_mean_citations_per_affiliation(self):
        """
        :return: numpy.array
        """
        self.logger.info('Counting mean affiliation citation (per publication)')
        aff_cit = self.get_citations_per_affiliation()
        aff_pub = self.get_num_papers_per_affiliation()
        self.logger.debug('Replacing 0 values in array to avoid division by 0')
        aff_pub[aff_pub == 0] = 1
        self.logger.debug('Counting mean affiliation citations')
        mean_aff_cit = aff_cit / aff_pub
        self.logger.debug('Min and max mean affiliation citation: %s, %s',
                          min(mean_aff_cit), max(mean_aff_cit))
        return mean_aff_cit

    def get_sum_aff_citations_per_paper(self, mean=False):
        """
        :return: numpy.array
        """
        self.logger.info('Finding sum of affiliation citations per paper')
        if mean:
            cit_per_aff = np.array(self.get_mean_citations_per_affiliation())
        else:
            cit_per_aff = np.array(self.get_citations_per_affiliation())
        self.logger.debug('Copying paper affiliation matrix')
        pap_aff_m = self.paper_aff_m.copy()
        self.logger.debug('Replacing data with affiliation citations')
        pap_aff_m.data = cit_per_aff[pap_aff_m.indices]
        aff_cit_per_paper = pap_aff_m.sum(axis=1).ravel().tolist()[0]
        self.logger.debug('Min and max affiliation cit sum per paper %s, %s',
                          min(aff_cit_per_paper), max(aff_cit_per_paper))
        self.logger.info('Done finding affiliation cit per paper, returning')
        return np.array(aff_cit_per_paper)

    def get_num_affiliations_per_paper(self):
        """
        :return:
        """
        self.logger.info('Finding number of affiliations per paper')
        pap_aff_m = self.paper_aff_m.copy()
        num_aff = pap_aff_m.sum(axis=1).ravel().tolist()[0]
        self.logger.debug('Least and most affiliations on paper %s, %s',
                          min(num_aff), max(num_aff))
        self.logger.info('Done counting number of aff per paper, returning')
        return np.array(num_aff)

    def get_num_papers_per_affiliation(self):
        """
        :return:
        """
        self.logger.info('Finding number of papers per affiliation')
        pap_aff_m = self.paper_aff_m.copy()
        num_pub = pap_aff_m.sum(axis=0).ravel().tolist()[0]
        self.logger.debug('Least and most papers per affiliation %s, %s',
                          min(num_pub), max(num_pub))
        self.logger.info('Done counting number of papers per aff, returning')
        return np.array(num_pub)

    def get_num_authors_per_affiliation(self):

        pass
