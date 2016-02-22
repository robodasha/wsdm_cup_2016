"""
Mappings for reading Microsoft Academic Graph dataset files
"""

from enum import Enum

__author__ = 'damirah'
__email__ = 'damirah@live.com'


class Affiliations(Enum):
    """
    Affiliations.txt
    """
    affiliation_id = 0
    affiliation_name = 1


class Authors(Enum):
    """
    Authors.txt
    """
    author_id = 0
    author_name = 1


class ConferenceSeries(Enum):
    """
    ConferenceSeries.txt
    """
    conference_series_id = 0
    conference_series_abbreviation = 1
    conference_series_name = 2


class ConferenceInstances(Enum):
    """
    Conferences.txt
    """
    id = 0
    abbreviation = 1
    full_name = 2
    location = 3
    url = 4
    start_date = 5
    end_date = 6
    abstract_date = 7
    submission_date = 8
    notification_date = 9
    final_version_date = 10


class FieldsOfStudy(Enum):
    """
    FieldsOfStudy.txt
    """
    field_id = 0
    field_name = 1


class Journals(Enum):
    """
    Journals.txt
    """
    journal_id = 0
    journal_name = 1


class Papers(Enum):
    """
    Papers.txt
    """
    paper_id = 0
    title_original = 1
    title_normalized = 2
    publish_year = 3
    publish_date = 4
    doi = 5
    venue_original = 6
    venue_normalized = 7
    journal_id = 8
    conference_series_id = 9
    paper_rank = 10


class PaperAuthorAffiliations(Enum):
    """
    PaperAuthorAffiliations.txt
    """
    paper_id = 0
    author_id = 1
    affiliation_id = 2
    affiliation_original = 3
    affiliation_normalized = 4
    author_seq_number = 5


class PaperKeywords(Enum):
    """
    PaperKeywords.txt
    """
    paper_id = 0
    keyword = 1
    field_id = 2


class PaperReferences(Enum):
    """
    PaperReferences.txt
    """
    paper_id = 0
    reference_id = 1


class PaperUrls(Enum):
    """
    PaperUrls.txt
    """
    paper_id = 0
    url = 1
