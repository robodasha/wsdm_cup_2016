
import csv
import logging
import shutil
from collections import Counter

import numpy as np
from scipy import stats
import pandas

import wsdmcup.logging as wsdmlog
from wsdmcup.timing import timeit
from wsdmcup.config import Config
from wsdmcup.model.authorship_network import AuthorshipNetwork
from wsdmcup.model.affiliation_network import AffiliationNetwork
from wsdmcup.model.citation_network import CitationNetwork
from wsdmcup.model.venue_network import VenueNetwork
from wsdmcup.model.fos_network import FoSNetwork
from wsdmcup.data.csv_datastore import CsvDatastore, Mag
from wsdmcup.data.hdf5_manager import Hdf5Manager
from wsdmcup.ranking.ranker import Ranker
from wsdmcup.tasks.other_tasks import upload_results


__author__ = 'damirah'
__email__ = 'damirah@live.com'


def log_data_statistics(data_arr, desc):
    """
    :param data_arr: numpy.array with data
    :param desc: string description
    :return: None
    """
    logger = logging.getLogger(__name__)
    logger.debug('%s statistics', desc)
    logger.debug(stats.describe(data_arr))
    logger.debug('Number of unique values: %s', len(np.unique(data_arr)))


def decode_column(df, column):
    """
    :param df: pandas.DataFrame
    :param column: string column name
    :return:
    """
    logger = logging.getLogger(__name__)
    logger.info('Decoding column %s', column)
    df[column] = df[column].str.decode(encoding='utf-8')
    logger.info('Done decoding, returning DataFrame')
    return df


def output_results(df, columns):
    """
    :param df: pandas.DataFrame
    :param columns: columns with paper_id and results
    :return: None
    """
    logger = logging.getLogger(__name__)
    results_path = Config.get_next_results_file_path()
    upload_path = Config.get_results_upload_path()
    logger.info('Storing results in a CSV %s', results_path)
    CsvDatastore().store_results(df, results_path, columns)
    logger.info('Copying results to the upload file %s', upload_path)
    shutil.copyfile(results_path, upload_path)
    return


@timeit
def rank():
    """
    Create a test submission -- rank papers only by number of received citations
    :return: None
    """
    logger = logging.getLogger(__name__)
    logger.info('Loading data')
    h5 = Hdf5Manager()
    # author_h_index = h5.load_author_h_index()
    papers = h5.load_papers().sort('paper_index')
    authors = h5.load_authors().sort('author_index')
    citation_network = CitationNetwork(
        papers, h5.load_citation_matrix())
    paper_journal_net = VenueNetwork(
        citation_network, h5.load_paper_journal_matrix())
    paper_conf_net = VenueNetwork(
        citation_network, h5.load_paper_conf_series_matrix())
    authorship_network = AuthorshipNetwork(
        authors, h5.load_authorship_matrix(), citation_network)
    affiliation_network = AffiliationNetwork(
        h5.load_affiliation_matrix(), h5.load_paper_affiliation_matrix(),
        citation_network)
    # fos_network = FoSNetwork(
    #     citation_network, h5.load_paper_field_of_study_matrix())

    papers = decode_column(papers, 'paper_id')

    num_authors = np.array(authorship_network.get_num_authors_per_paper())
    num_authors[num_authors == 0] = 1

    # PAPERS ================================================================= #

    total_citations_threshold = np.array(citation_network.get_total_citations(
        limit=5000))
    mean_citations_threshold = total_citations_threshold / num_authors

    # YEAR =================================================================== #

    pub_year = np.array(papers['publish_year'])
    pub_year[pub_year > 2015] = 0

    # AFFILIATIONS =========================================================== #

    paper_citations = np.array(citation_network.get_total_citations())
    aff_cit = affiliation_network.get_sum_aff_citations_per_paper()
    num_aff = affiliation_network.get_num_affiliations_per_paper()
    subtract = num_aff * paper_citations
    num_aff[num_aff == 0] = 1
    mean_aff_cit = (aff_cit - subtract) / num_aff

    # AUTHORS ================================================================ #

    author_citations = np.array(authorship_network.get_author_sum_per_paper(
        time_decay=False, limit=None, mean=True))
    mean_author_citations = author_citations / num_authors

    # JOURNALS =============================================================== #

    journal_cit_sub = paper_journal_net.get_paper_venue_citations(subtract=True)

    # CONFERENCES ============================================================ #

    conf_cit_sub = paper_conf_net.get_paper_venue_citations(subtract=True)

    # FIELDS OF STUDY ======================================================== #

    # fos_cit_total = fos_network.get_paper_fos_citations()

    # OUTPUT ================================================================= #

    papers['pub_threshold'] = mean_citations_threshold
    papers['auth'] = mean_author_citations
    papers['aff'] = mean_aff_cit
    papers['journal'] = journal_cit_sub
    papers['conf'] = conf_cit_sub
    papers['year'] = pub_year

    log_data_statistics(papers['pub_threshold'], 'pub_threshold')
    log_data_statistics(papers['auth'], 'auth')
    log_data_statistics(papers['aff'], 'aff')
    log_data_statistics(papers['journal'], 'journal')
    log_data_statistics(papers['conf'], 'conf')
    log_data_statistics(papers['year'], 'year')

    col_weights = {
        'pub_threshold': 2.5,
        'auth': 1.0,
        'aff': 0.01,
        'journal': 0.1,
        'conf': 0.1,
        'year': 0.1,
    }
    papers['rank'] = Ranker().rank_with_weighting_values(papers, col_weights)

    log_data_statistics(papers['rank'], 'rank')

    output_columns = ['paper_id', 'rank']
    output_results(papers, output_columns)
    upload_results()

    return
