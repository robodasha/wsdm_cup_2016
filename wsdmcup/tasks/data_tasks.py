
import sys
import logging

import numpy

from wsdmcup.timing import timeit
from wsdmcup.data.csv_manager import CsvManager
from wsdmcup.data.hdf5_manager import Hdf5Manager
from wsdmcup.model.citation_network import CitationNetwork
from wsdmcup.model.authorship_network import AuthorshipNetwork

__author__ = 'damirah'
__email__ = 'damirah@live.com'


def df2dict(df, id_col, idx_col):
    """
    :param df: pandas.DataFrame
    :param id_col:
    :param idx_col:
    :return:
    """
    logger = logging.getLogger(__name__)
    logger.info('Creating dictionary of {0}: {1}'
                .format(id_col, idx_col))
    logger.debug('Converting ID column from byte to string')
    df[id_col] = df[id_col].str.decode(encoding='utf-8')
    logger.debug('Creating the dictionary')
    return df.set_index(id_col)[idx_col].to_dict()


@timeit
def papers_to_hdf5():
    """
    :return: None
    """
    logger = logging.getLogger(__name__)
    print('Are you sure? This will rewrite existing data. '
          'Please select (y/N)')
    char = sys.stdin.read(1)
    if char == 'y':
        hdf5_manager = Hdf5Manager()
        hdf5_manager.store_papers()
    else:
        logger.info('Selected no --> exiting')
    return


@timeit
def citation_matrix_to_hdf5():
    """
    :return: None
    """
    logger = logging.getLogger(__name__)
    print('Are you sure? This will rewrite existing data. '
          'Please select (y/N)')
    char = sys.stdin.read(1)
    if char == 'y':
        hdf5_manager = Hdf5Manager()
        papers = hdf5_manager.load_papers()
        papers_dict = df2dict(papers, 'paper_id', 'paper_index')
        # for saving memory
        del papers
        cit_m = CsvManager().load_citation_matrix(papers_dict)
        hdf5_manager.store_citation_matrix(cit_m)
    else:
        logger.info('Selected no --> exiting')
    return


@timeit
def authors_to_hdf5():
    """
    :return: None
    """
    logger = logging.getLogger(__name__)
    print('Are you sure? This will rewrite existing data. '
          'Please select (y/N)')
    char = sys.stdin.read(1)
    if char == 'y':
        hdf5_manager = Hdf5Manager()
        hdf5_manager.store_authors()
    else:
        logger.info('Selected no --> exiting')
    return


@timeit
def authorship_matrix_to_hdf5():
    """
    :return: None
    """
    logger = logging.getLogger(__name__)
    print('Are you sure? This will rewrite existing data. '
          'Please select (y/N)')
    char = sys.stdin.read(1)
    if char == 'y':
        hdf5_manager = Hdf5Manager()
        papers = hdf5_manager.load_papers()
        authors = hdf5_manager.load_authors()
        papers_dict = df2dict(papers, 'paper_id', 'paper_index')
        authors_dict = df2dict(authors, 'author_id', 'author_index')
        # for saving memory
        del papers, authors
        logger.info('Creating authorship matrix')
        auth_m = CsvManager().load_authorship_matrix(papers_dict, authors_dict)
        logger.info('Storing authorship matrix')
        hdf5_manager.store_authorship_matrix(auth_m)
    else:
        logger.info('Selected no --> exiting')
    return


@timeit
def affiliations_to_hdf5():
    """
    :return: None
    """
    logger = logging.getLogger(__name__)
    print('Are you sure? This will rewrite existing data. '
          'Please select (y/N)')
    char = sys.stdin.read(1)
    if char == 'y':
        hdf5_manager = Hdf5Manager()
        hdf5_manager.store_affiliations()

        papers = hdf5_manager.load_papers()
        authors = hdf5_manager.load_authors()
        affiliations = hdf5_manager.load_affiliations()
        papers_dict = df2dict(papers, 'paper_id', 'paper_index')
        authors_dict = df2dict(authors, 'author_id', 'author_index')
        affiliations_dict = df2dict(affiliations, 'affiliation_id',
                                    'affiliation_index')

        # for saving memory
        del papers, authors, affiliations

        logger.info('Creating paper-author-affiliation matrix')
        aff_m = CsvManager().load_affiliation_matrix(
            papers_dict, authors_dict, affiliations_dict)
        logger.info('Storing paper-author-affiliation matrix')
        hdf5_manager.store_affiliation_matrix(aff_m)

        logger.info('Creating paper-affiliation matrix')
        paper_aff_m = CsvManager().load_paper_affiliation_matrix(
            papers_dict, affiliations_dict)
        # there might be duplicate entries in the matrix, remove them
        logger.info('Removing duplicate entries')
        paper_aff_m.data = numpy.ones(len(paper_aff_m.data),
                                      dtype=paper_aff_m.dtype)
        logger.info('Storing paper-affiliation matrix')
        hdf5_manager.store_paper_affiliation_matrix(paper_aff_m)
    else:
        logger.info('Selected no --> exiting')
    return


@timeit
def author_sequence_matrix_to_hdf5():
    """
    :return: None
    """
    logger = logging.getLogger(__name__)
    print('Are you sure? This will rewrite existing data. '
          'Please select (y/N)')
    char = sys.stdin.read(1)
    if char == 'y':
        hdf5_manager = Hdf5Manager()
        papers = hdf5_manager.load_papers()
        authors = hdf5_manager.load_authors()
        papers_dict = df2dict(papers, 'paper_id', 'paper_index')
        authors_dict = df2dict(authors, 'author_id', 'author_index')

        # for saving memory
        del papers, authors
        logger.info('Creating author sequence number matrix')
        auth_seq_m = CsvManager().load_author_sequence_matrix(
            papers_dict, authors_dict)
        logger.info('Storing paper-author-affiliation matrix')
        hdf5_manager.store_author_sequence_matrix(auth_seq_m)
    else:
        logger.info('Selected no --> exiting')
    return


@timeit
def journals_to_hdf5():
    """
    :return: None
    """
    logger = logging.getLogger(__name__)
    print('Are you sure? This will rewrite existing data. '
          'Please select (y/N)')
    char = sys.stdin.read(1)
    if char == 'y':
        hdf5_manager = Hdf5Manager()
        hdf5_manager.store_journals()

        papers = hdf5_manager.load_papers()
        journals = hdf5_manager.load_journals()

        papers_dict = df2dict(papers, 'paper_id', 'paper_index')
        journals_dict = df2dict(journals, 'journal_id', 'journal_index')

        # for saving memory
        del papers, journals
        logger.info('Creating papers-journals matrix')
        journal_m = CsvManager().load_paper_journal_matrix(
            papers_dict, journals_dict)
        logger.info('Storing paper-journal matrix')
        hdf5_manager.store_paper_journal_matrix(journal_m)
    else:
        logger.info('Selected no --> exiting')
    return


@timeit
def conference_series_to_hdf5():
    """
    :return: None
    """
    logger = logging.getLogger(__name__)
    print('Are you sure? This will rewrite existing data. '
          'Please select (y/N)')
    char = sys.stdin.read(1)
    if char == 'y':
        hdf5_manager = Hdf5Manager()
        hdf5_manager.store_conference_series()

        papers = hdf5_manager.load_papers()
        conf_series = hdf5_manager.load_conference_series()

        papers_dict = df2dict(papers, 'paper_id', 'paper_index')
        conf_dict = df2dict(conf_series, 'conference_series_id',
                            'conference_series_index')

        # for saving memory
        del papers, conf_series
        logger.info('Creating papers-conference series matrix')
        conf_series_m = CsvManager().load_paper_conf_series_matrix(
            papers_dict, conf_dict)
        logger.info('Storing paper-conference series matrix')
        hdf5_manager.store_paper_conf_series_matrix(conf_series_m)
    else:
        logger.info('Selected no --> exiting')
    return


@timeit
def fields_of_study_to_hdf5():
    """
    :return: None
    """
    logger = logging.getLogger(__name__)
    print('Are you sure? This will rewrite existing data. '
          'Please select (y/N)')
    char = sys.stdin.read(1)
    if char == 'y':
        hdf5_manager = Hdf5Manager()
        hdf5_manager.store_fields_of_study()

        papers = hdf5_manager.load_papers()
        fos = hdf5_manager.load_fields_of_study()

        papers_dict = df2dict(papers, 'paper_id', 'paper_index')
        fos_dict = df2dict(fos, 'field_id', 'field_index')

        # for saving memory
        del papers, fos

        logger.info('Creating papers-fields of study matrix')
        fos_m = CsvManager().load_paper_field_of_study_matrix(
            papers_dict, fos_dict)
        logger.info('Storing paper-fields of study matrix')
        hdf5_manager.store_paper_field_of_study_matrix(fos_m)
    else:
        logger.info('Selected no --> exiting')
    return


@timeit
def h_index_to_hdf5():
    logger = logging.getLogger(__name__)
    h5 = Hdf5Manager()
    papers = h5.load_papers().sort('paper_index')
    authors = h5.load_authors().sort('author_index')
    citation_network = CitationNetwork(
        papers, h5.load_citation_matrix())
    authorship_network = AuthorshipNetwork(
        authors, h5.load_authorship_matrix(), citation_network)
    h_indices = authorship_network.get_h_index()
    logger.info('Got h-indices, storing them in hdf5')
    h5.store_author_h_index(h_indices)
    return
