
import logging

import numpy as np


__author__ = 'damirah'
__email__ = 'damirah@live.com'


class VenueNetwork(object):

    def __init__(self, citation_network, paper_venue_m):
        """
        :param citation_network: instance of wsdmcup.model.CitationNetwork
        :param paper_venue_m: binary incidence matrix, where rows represent
                              papers, cols represent venues and fields (values 0
                              and 1) represent whether a paper was published
                              at a venue
        :return: None
        """
        self.logger = logging.getLogger(__name__)
        self.cit_net = citation_network
        self.paper_venue_m = paper_venue_m

    def get_venue_publications(self):
        """
        :return: numpy.array with number of publications per venue
        """
        self.logger.info('Counting number of papers per venue')
        num_pub = self.paper_venue_m.sum(axis=0).ravel().tolist()[0]
        self.logger.info('Least and most papers per venue: %s, %s',
                         min(num_pub), max(num_pub))
        return num_pub

    def get_paper_venue_publications(self):
        """
        :return: numpy.array with number of publications published at that
                 publication's venue
        """
        venue_pub = np.array(self.get_venue_publications())
        self.logger.debug('Copying paper-venue matrix as CSR matrix')
        venue_pub_m = self.paper_venue_m.tocsr().copy()
        self.logger.debug('Replacing matrix data with venue publication counts')
        venue_pub_m.data = venue_pub[venue_pub_m.indices]
        venue_pub_per_paper = venue_pub_m.sum(axis=1).ravel().tolist()[0]
        self.logger.info('Least and most publications: %s, %s',
                         min(venue_pub_per_paper), max(venue_pub_per_paper))
        return np.array(venue_pub_per_paper)

    def get_venue_citations(self):
        """
        :return: numpy.array with citation score for each venue
        """
        self.logger.info('Counting sum of citations per venue')
        self.logger.debug('Counting citations per paper')
        cit_per_paper = np.array(self.cit_net.get_total_citations())
        self.logger.debug('Copying paper-venue matrix as CSC matrix')
        venue_cit_m = self.paper_venue_m.tocsc().copy()
        self.logger.debug('Replacing matrix with citation data and summing')
        venue_cit_m.data = cit_per_paper[venue_cit_m.indices]
        venue_cit = venue_cit_m.sum(axis=0).ravel().tolist()[0]
        self.logger.info('Least and most cited venues: %s, %s',
                         min(venue_cit), max(venue_cit))
        return venue_cit

    def get_paper_venue_citations(self, subtract=False, mean=False):
        """
        :param subtract: whether to subtract citations received by a paper
                         from the venue total, e.g. if paper X was published
                         at venue Y, the venue Y was cited 300 times in total
                         and the paper 45 times, then the result for the paper
                         will be 300-45=255
        :param mean: whether to retrieve sum of citation per venue (mean=False)
                     or mean citations per paper published at the venue
                     (mean=True). When 'mean' is set to True, the retrieved
                     values are equal to Impact Factor for the venue with
                     time frame equal to age of the venue (rather than
                     past X years)
        :return: numpy.array with a value for each paper
        """
        venue_cit = np.array(self.get_venue_citations())
        self.logger.debug('Copying paper-venue matrix as CSR matrix')
        venue_cit_m = self.paper_venue_m.tocsr().copy()
        self.logger.debug('Replacing matrix data with venue citation data')
        venue_cit_m.data = venue_cit[venue_cit_m.indices]
        venue_cit_per_paper = venue_cit_m.sum(axis=1).ravel().tolist()[0]
        self.logger.info('Least and most citations: %s, %s',
                         min(venue_cit_per_paper), max(venue_cit_per_paper))
        if subtract:
            paper_citations = np.array(self.cit_net.get_total_citations())
            self.logger.info('Subtracting paper citations from venue citations')
            venue_cit_per_paper = venue_cit_per_paper - paper_citations
            venue_cit_per_paper[venue_cit_per_paper < 0] = 0
            self.logger.info('After subtracting paper citations min and max is '
                             '%s, %s', min(venue_cit_per_paper),
                             max(venue_cit_per_paper))
        if mean:
            self.logger.info('Dividing venue citations by number of papers '
                             'published at the venue')
            num_pub = self.get_paper_venue_publications()
            if subtract:
                num_pub -= 1
            # to avoid division by zero
            num_pub[num_pub <= 0] = 1
            mean_cit = venue_cit_per_paper / num_pub
            self.logger.info('Min and max mean venue citations per pub: %s, %s',
                             min(mean_cit), max(mean_cit))
            return np.array(mean_cit)
        else:
            return np.array(venue_cit_per_paper)
