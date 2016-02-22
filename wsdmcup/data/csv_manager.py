"""
Class providing methods for loading/storing specific data.
"""

import logging

from wsdmcup.config import Config

from wsdmcup.data.csv_datastore import CsvDatastore
from wsdmcup.data.csv_mappings import (
    PaperAuthorAffiliations as PapAuthAff,
    PaperReferences as PapRef,
    Papers as PapersCsv,
    PaperKeywords as PaperKeywordsCsv,
)

__author__ = 'damirah'
__email__ = 'damirah@live.com'


class CsvManager(object):
    """
    Class for reading MAG data files
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def load_citation_matrix(self, papers):
        """
        Build adjacency matrix from list of edges in PaperReferences.txt file
        :param papers: dictionary of {id: index}
        :return: scipy.sparse.csr_matrix
        """
        fpath = Config.get_path_to_data_file('PaperReferences.txt')
        return CsvDatastore().csv_to_relation_matrix(fpath,
                                                     PapRef.paper_id.value,
                                                     papers,
                                                     PapRef.reference_id.value,
                                                     papers)

    def load_authorship_matrix(self, papers, authors):
        """
        Build authorship matrix from list of paper-author relations in
        PaperAuthorAffiliations.txt file
        :param papers: dictionary of {id: index}
        :param authors: dictionary of {id: index}
        :return: scipy.sparse.csr_matrix
        """
        fpath = Config.get_path_to_data_file('PaperAuthorAffiliations.txt')
        return CsvDatastore().csv_to_relation_matrix(fpath,
                                                     PapAuthAff.paper_id.value,
                                                     papers,
                                                     PapAuthAff.author_id.value,
                                                     authors)

    def load_affiliation_matrix(self, papers, authors, affiliations):
        """
        Build matrix of papers, authors and affiliations from list of
        paper-author-affiliation relations in PaperAuthorAffiliations.txt file
        :param papers: dictionary of {id: index}
        :param authors: dictionary of {id: index}
        :param affiliations: dictionary of {id: index}
        :return: scipy.sparse.csr_matrix
        """
        fpath = Config.get_path_to_data_file('PaperAuthorAffiliations.txt')
        return CsvDatastore().csv_to_relation_matrix(
            fpath, PapAuthAff.paper_id.value, papers,
            PapAuthAff.author_id.value, authors,
            PapAuthAff.affiliation_id.value, affiliations)

    def load_paper_affiliation_matrix(self, papers, affiliations):
        """
        Build matrix of papers and affiliations from list of
        paper-affiliation relations in PaperAuthorAffiliations.txt file
        :param papers: dictionary of {id: index}
        :param affiliations: dictionary of {id: index}
        :return: scipy.sparse.csr_matrix
        """
        fpath = Config.get_path_to_data_file('PaperAuthorAffiliations.txt')
        return CsvDatastore().csv_to_relation_matrix(
            fpath, PapAuthAff.paper_id.value, papers,
            PapAuthAff.affiliation_id.value, affiliations)

    def load_author_sequence_matrix(self, papers, authors):
        """
        :param papers: dictionary of {id: index}
        :param authors: dictionary of {id: index}
        :return:
        """
        fpath = Config.get_path_to_data_file('PaperAuthorAffiliations.txt')
        return CsvDatastore().csv_to_relation_matrix(
            fpath, PapAuthAff.paper_id.value, papers,
            PapAuthAff.author_id.value, authors,
            PapAuthAff.author_seq_number.value)

    def load_paper_journal_matrix(self, papers, journals):
        """
        :param papers: dictionary of {id: index}
        :param journals: dictionary of {id: index}
        :return:
        """
        fpath = Config.get_path_to_data_file('Papers.txt')
        return CsvDatastore().csv_to_relation_matrix(
            fpath, PapersCsv.paper_id.value, papers,
            PapersCsv.journal_id.value, journals)

    def load_paper_conf_series_matrix(self, papers, conf_series):
        """
        :param papers: dictionary of {id: index}
        :param conf_series: dictionary of {id: index}
        :return:
        """
        fpath = Config.get_path_to_data_file('Papers.txt')
        return CsvDatastore().csv_to_relation_matrix(
            fpath, PapersCsv.paper_id.value, papers,
            PapersCsv.conference_series_id.value, conf_series)

    def load_paper_field_of_study_matrix(self, papers, fos):
        """
        :param papers: dictionary of {id: index}
        :param fos: fields of study, dictionary of {id: index}
        :return:
        """
        fpath = Config.get_path_to_data_file('PaperKeywords.txt')
        return CsvDatastore().csv_to_relation_matrix(
            fpath, PaperKeywordsCsv.paper_id.value, papers,
            PaperKeywordsCsv.field_id.value, fos)
