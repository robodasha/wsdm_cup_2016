
import logging
import statistics

import numpy
from scipy import stats


__author__ = 'damirah'
__email__ = 'damirah@live.com'


class Ranker(object):

    def __init__(self):
        self.ranking_method = 'min'
        self.logger = logging.getLogger(__name__)

    def normalise_data(self, data):
        """
        :param data: array with data
        :return: array with data normalised to interval [0, 1]
        """
        self.logger.info('Normalising data')
        self.logger.debug('Finding max value')
        max_value = max(data)
        self.logger.debug('Max value is {0}'.format(max_value))
        self.logger.debug('Normalising the data')
        data_normalised = data / max_value
        self.logger.info('Done normalising, returning results')
        return data_normalised

    def normalise_rank(self, rank):
        """
        :param rank: list of ranks
        :return: list of normalised ranks
        """
        self.logger.info('Normalising rank')
        self.logger.debug('Finding max rank')
        max_rank = max(rank)
        self.logger.debug('Max rank is {0}'.format(max_rank))
        self.logger.debug('Normalising the rank')
        rank_normalised = rank / max_rank
        self.logger.info('Done normalising, returning results')
        return rank_normalised

    def reverse_rank(self, rank):
        """
        Reverse the rank (turn highest numbers to lowest numbers and vice versa)
        e.g. [1,1,3,4] will be reversed to [4,4,2,1]
        :param rank: list of ranks
        :return:
        """
        self.logger.info('Reversing rank')
        max_rank = max(rank)
        self.logger.debug('Max rank: %s, reversing the rank', max_rank)
        return (max_rank + 1) - rank

    def rank_by_column(self, df, col_name):
        """
        :param df: pandas.DataFrame
        :param col_name: column name
        :return: list of ranks (normalised)
        """
        self.logger.info('Ranking DataFrame data using column %s', col_name)
        col_normalised = numpy.array(self.normalise_data(df[col_name]))
        rank = stats.rankdata(col_normalised, method=self.ranking_method)
        return self.normalise_rank(rank)

    def rank_with_weighting_values(self, df, col_weights):
        """
        :param df: pandas.DataFrame
        :param col_weights: dictionary of {<string> column_name: <float> weight}
        :return: list of ranks (normalised)
        """
        if not col_weights:
            self.logger.error('No column weights provided')
            return []
        weighted_cols = []
        self.logger.info('Weighting each column')
        for col in col_weights:
            self.logger.debug('Multiplying column %s by it\'s weight', col)
            weighted_cols.append(numpy.multiply(
                numpy.array(self.normalise_data(df[col])), col_weights[col]))
        self.logger.info('Summing all weighted columns')
        merged = [sum(x) for x in zip(*weighted_cols)]
        self.logger.info('Ranking the sum')
        final_rank = stats.rankdata(merged, method=self.ranking_method)
        self.logger.info('Normalising the final rank')
        return self.normalise_rank(final_rank)
