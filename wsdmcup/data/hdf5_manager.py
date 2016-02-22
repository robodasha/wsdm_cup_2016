"""
Module for accessing data in HDF5 data store.
This module provides methods for accessing specific data.
"""

import logging

from wsdmcup.config import Config
from wsdmcup.data.hdf5_mappings import (
    Papers as PapersHdf5,
    Authors as AuthorsHdf5,
    Affiliations as AffiliationsHdf5,
    Journals as JournalsHdf5,
    ConferenceSeries as ConferenceSeriesHdf5,
    AuthorStatistics as AuthorStatisticsHdf5,
    FieldsOfStudy as FieldsOfStudyHdf5,
)
from wsdmcup.data.csv_mappings import (
    Papers as PapersCsv,
    Authors as AuthorsCsv,
    Affiliations as AffiliationsCsv,
    Journals as JournalsCsv,
    ConferenceSeries as ConferenceSeriesCsv,
    FieldsOfStudy as FieldsOfStudyCsv,
)
from wsdmcup.data.hdf5_datastore import Hdf5Datastore

__author__ = 'damirah'
__email__ = 'damirah@live.com'


class Hdf5Manager(object):

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def store_citation_matrix(self, cit_matrix):
        """
        :param cit_matrix: scipy.sparse.csr_matrix
        :return: None
        """
        ds = Hdf5Datastore()
        self.logger.info('Storing citation matrix in %s',
                         ds.get_datastore_path())
        ds.store_sparse_matrix(cit_matrix, 'citation_matrix')
        self.logger.info('Storing done!')

    def load_citation_matrix(self):
        """
        :return: scipy.sparse.csr_matrix
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading citation matrix from %s',
                         ds.get_datastore_path())
        adj_matrix = ds.load_sparse_matrix('citation_matrix')
        self.logger.info('Loading done!')
        return adj_matrix

    def store_authorship_matrix(self, auth_matrix):
        """
        :param adj_matrix: scipy.sparse.csr_matrix
        :return: None
        """
        ds = Hdf5Datastore()
        self.logger.info('Storing authorship matrix in %s',
                         ds.get_datastore_path())
        ds.store_sparse_matrix(auth_matrix, 'authorship_matrix')
        self.logger.info('Storing done!')

    def load_authorship_matrix(self):
        """
        :return: scipy.sparse.csr_matrix
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading authorship matrix from %s',
                         ds.get_datastore_path())
        auth_matrix = ds.load_sparse_matrix('authorship_matrix')
        self.logger.info('Loading done!')
        return auth_matrix

    def store_affiliation_matrix(self, aff_matrix):
        """
        :param auth_seq_m: scipy.sparse.csr_matrix
        :return: None
        """
        ds = Hdf5Datastore()
        self.logger.info('Storing paper-author-affiliation matrix in %s',
                         ds.get_datastore_path())
        ds.store_sparse_matrix(aff_matrix, 'affiliation_matrix')
        self.logger.info('Storing done!')

    def load_affiliation_matrix(self):
        """
        :return: scipy.sparse.csr_matrix
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading paper-author-affiliation matrix from %s',
                         ds.get_datastore_path())
        aff_matrix = ds.load_sparse_matrix('affiliation_matrix')
        self.logger.info('Loading done!')
        return aff_matrix

    def store_paper_affiliation_matrix(self, aff_matrix):
        """
        :param auth_seq_m: scipy.sparse.csr_matrix
        :return: None
        """
        ds = Hdf5Datastore()
        self.logger.info('Storing paper-affiliation matrix in %s',
                         ds.get_datastore_path())
        ds.store_sparse_matrix(aff_matrix, 'paper_affiliation_matrix')
        self.logger.info('Storing done!')

    def load_paper_affiliation_matrix(self):
        """
        :return: scipy.sparse.csr_matrix
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading paper-affiliation matrix from %s',
                         ds.get_datastore_path())
        aff_matrix = ds.load_sparse_matrix('paper_affiliation_matrix')
        self.logger.info('Loading done!')
        return aff_matrix

    def store_paper_journal_matrix(self, journal_m):
        """
        :param journal_m: scipy.sparse.csr_matrix
        :return: None
        """
        ds = Hdf5Datastore()
        self.logger.info('Storing paper-journal matrix in %s',
                         ds.get_datastore_path())
        ds.store_sparse_matrix(journal_m, 'paper_journal_matrix')
        self.logger.info('Storing done!')

    def load_paper_journal_matrix(self):
        """
        :return: scipy.sparse.csr_matrix
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading paper-journal matrix from %s',
                         ds.get_datastore_path())
        journal_m = ds.load_sparse_matrix('paper_journal_matrix')
        self.logger.info('Loading done!')
        return journal_m

    def store_paper_conf_series_matrix(self, conf_series_m):
        """
        :param conf_series_m: scipy.sparse.csr_matrix
        :return: None
        """
        ds = Hdf5Datastore()
        self.logger.info('Storing paper-conference series matrix in %s',
                         ds.get_datastore_path())
        ds.store_sparse_matrix(conf_series_m, 'paper_conf_series_matrix')
        self.logger.info('Storing done!')

    def load_paper_conf_series_matrix(self):
        """
        :return: scipy.sparse.csr_matrix
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading paper-conference series matrix from %s',
                         ds.get_datastore_path())
        conf_series_m = ds.load_sparse_matrix('paper_conf_series_matrix')
        self.logger.info('Loading done!')
        return conf_series_m

    def store_author_sequence_matrix(self, auth_seq_m):
        """
        :param auth_seq_m: scipy.sparse.csr_matrix
        :return: None
        """
        ds = Hdf5Datastore()
        self.logger.info('Storing author sequence number matrix in %s',
                         ds.get_datastore_path())
        ds.store_sparse_matrix(auth_seq_m, 'author_sequence_matrix')
        self.logger.info('Storing done!')

    def load_author_sequence_matrix(self):
        """
        :return: scipy.sparse.csr_matrix
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading author sequence number matrix from %s',
                         ds.get_datastore_path())
        auth_seq_m = ds.load_sparse_matrix('author_sequence_matrix')
        self.logger.info('Loading done!')
        return auth_seq_m

    def store_paper_field_of_study_matrix(self, fos_m):
        """
        :param fos_m: scipy.sparse.csr_matrix
        :return: None
        """
        ds = Hdf5Datastore()
        self.logger.info('Storing paper-field of study matrix in %s',
                         ds.get_datastore_path())
        ds.store_sparse_matrix(fos_m, 'paper_field_of_study_matrix')
        self.logger.info('Storing done!')
        return

    def load_paper_field_of_study_matrix(self):
        """
        :return: scipy.sparse.csr_matrix
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading paper-field of study matrix from %s',
                         ds.get_datastore_path())
        fos_m = ds.load_sparse_matrix('paper_field_of_study_matrix')
        self.logger.info('Loading done!')
        return fos_m

    def store_papers(self):
        """
        :return: None
        """
        papers_file = 'Papers.txt'
        papers_path = Config.get_path_to_data_file(papers_file)
        self.logger.info('Reading papers from %s', papers_path)
        rows = Hdf5Datastore().store_table('papers_table', PapersHdf5,
                                           papers_path, PapersCsv)
        self.logger.info('Rows exported: %s', rows)

    def store_authors(self):
        """
        :return: None
        """
        authors_file = 'Authors.txt'
        authors_path = Config.get_path_to_data_file(authors_file)
        self.logger.info('Reading authors from %s', authors_file)
        rows = Hdf5Datastore().store_table('authors_table', AuthorsHdf5,
                                           authors_path, AuthorsCsv)
        self.logger.info('Rows exported: %s', rows)

    def store_affiliations(self):
        """
        :return: None
        """
        affiliations_file = 'Affiliations.txt'
        affiliations_path = Config.get_path_to_data_file(affiliations_file)
        self.logger.info('Reading affiliations from %s', affiliations_path)
        rows = Hdf5Datastore().store_table('affiliations_table',
                                           AffiliationsHdf5,
                                           affiliations_path, AffiliationsCsv)
        self.logger.info('Rows exported: %s', rows)

    def store_journals(self):
        """
        :return: None
        """
        journals_file = 'Journals.txt'
        journals_path = Config.get_path_to_data_file(journals_file)
        self.logger.info('Reading journals from %s', journals_path)
        rows = Hdf5Datastore().store_table('journals_table',
                                           JournalsHdf5,
                                           journals_path, JournalsCsv)
        self.logger.info('Rows exported: %s', rows)

    def store_conference_series(self):
        """
        :return: None
        """
        conf_series_file = 'Conferences.txt'
        conf_series_path = Config.get_path_to_data_file(conf_series_file)
        self.logger.info('Reading conference series from %s', conf_series_path)
        rows = Hdf5Datastore().store_table('conference_series_table',
                                           ConferenceSeriesHdf5,
                                           conf_series_path,
                                           ConferenceSeriesCsv)
        self.logger.info('Rows exported: %s', rows)

    def store_fields_of_study(self):
        """
        :return: None
        """
        fos_file = 'FieldsOfStudy.txt'
        fos_path = Config.get_path_to_data_file(fos_file)
        self.logger.info('Reading fields of study from %s', fos_path)
        rows = Hdf5Datastore().store_table('fields_of_study_table',
                                           FieldsOfStudyHdf5,
                                           fos_path,
                                           FieldsOfStudyCsv)
        self.logger.info('Rows exported: %s', rows)
        return

    def store_author_stats(self, astats):
        """
        :param astats: pandas.DataFrame
        :return:
        """
        ds = Hdf5Datastore()
        self.logger.info('Storing author statistics in %s',
                         ds.get_datastore_path())
        ds.store_dataframe(astats, 'author_statistics', AuthorStatisticsHdf5)
        self.logger.info('Storing done!')

    def store_author_h_index(self, h_i):
        """
        :param h_i:
        :return:
        """
        ds = Hdf5Datastore()
        self.logger.info('Storing author h-index values in %s',
                         ds.get_datastore_path())
        ds.store_array(h_i, 'author_h_index')
        self.logger.info('Storing done!')

    def load_author_h_index(self):
        """
        :return:
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading author h-index values from %s',
                         ds.get_datastore_path())
        h_i = ds.load_array('author_h_index')
        self.logger.info('Loading done! Got %s author h-index values',
                         len(h_i))
        return h_i

    def load_papers(self):
        """
        :return: pandas.DataFrame
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading papers from %s', ds.get_datastore_path())
        papers = ds.load_table('papers_table')
        self.logger.info('Loading done! Got %s papers', len(papers))

        # self.logger.info('Setting index')
        # index_levels = [papers['paper_id'].tolist(),
        #                 papers['paper_index'].tolist()]
        # self.logger.info('Index size: %s', [len(l) for l in index_levels])
        # papers.index = pandas.MultiIndex.from_tuples(
        #     list(zip(*index_levels)),
        #     names=['paper_id', 'paper_index'])
        # self.logger.info('Indexing done')
        return papers

    def load_authors(self):
        """
        :return: pandas.DataFrame
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading authors from %s', ds.get_datastore_path())
        authors = ds.load_table('authors_table')
        self.logger.info('Loading done! Got %s authors', len(authors))

        # self.logger.info('Setting index')
        # index_levels = [authors['author_id'].tolist(),
        #                 authors['author_index'].tolist()]
        # self.logger.info('Index size: %s', [len(l) for l in index_levels])
        # authors.index = pandas.MultiIndex.from_tuples(
        #     list(zip(*index_levels)),
        #     names=['author_id', 'author_index'])
        # self.logger.info('Indexing done')
        return authors

    def load_affiliations(self):
        """
        :return: pandas.DataFrame
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading affiliations from %s',
                         ds.get_datastore_path())
        affiliations = ds.load_table('affiliations_table')
        self.logger.info('Loading done! Got %s affiliations', len(affiliations))
        return affiliations

    def load_journals(self):
        """
        :return: pandas.DataFrame
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading journals from %s', ds.get_datastore_path())
        journals = ds.load_table('journals_table')
        self.logger.info('Loading done! Got %s journals', len(journals))
        return journals

    def load_conference_series(self):
        """
        :return: pandas.DataFrame
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading conference series from %s',
                         ds.get_datastore_path())
        conf_series = ds.load_table('conference_series_table')
        self.logger.info('Loading done! Got %s conference series',
                         len(conf_series))
        return conf_series

    def load_fields_of_study(self):
        """
        :return: pandas.DataFrame
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading fields of study from %s',
                         ds.get_datastore_path())
        fos = ds.load_table('fields_of_study_table')
        self.logger.info('Loading done! Got %s fields of study',
                         len(fos))
        return fos

    def load_author_stats(self):
        """
        :return: pandas.DataFrame
        """
        ds = Hdf5Datastore()
        self.logger.info('Loading author statistics from %s',
                         ds.get_datastore_path())
        author_stats = ds.load_table('author_statistics')
        self.logger.info('Loading done! Got %s rows', len(author_stats))
        return author_stats
