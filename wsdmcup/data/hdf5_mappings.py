"""
Mappings for storing and loading data from HDF5 data store
"""

import tables

__author__ = 'damirah'
__email__ = 'damirah@live.com'


class Papers(tables.IsDescription):
    paper_index = tables.Int32Col()
    paper_id = tables.StringCol(8)
    # title_original = tables.StringCol(2048)
    # title_normalized = tables.StringCol(2048)
    publish_year = tables.Int16Col()
    # publish_date = tables.StringCol(64)
    doi = tables.StringCol(256)
    # venue_original = tables.StringCol(3072)
    # venue_normalized = tables.StringCol(3072)
    journal_id = tables.StringCol(8)
    conference_series_id = tables.StringCol(8)
    paper_rank = tables.Int32Col()


class Authors(tables.IsDescription):
    author_index = tables.Int32Col()
    author_id = tables.StringCol(8)
    # author_name = tables.StringCol(256)


class Affiliations(tables.IsDescription):
    affiliation_index = tables.Int32Col()
    affiliation_id = tables.StringCol(8)
    # affiliation name = tables.StringCol(256)


class AuthorStatistics(tables.IsDescription):
    author_id = tables.StringCol(8)
    author_index = tables.Int32Col()
    h_index = tables.Int32Col()
    total_documents = tables.Int32Col()
    total_references = tables.Int32Col()
    total_citations = tables.Int32Col()
    references_per_document = tables.Float64Col()
    citations_per_document = tables.Float64Col()


class Journals(tables.IsDescription):
    journal_index = tables.Int32Col()
    journal_id = tables.StringCol(8)
    # journal name = tables.StringCol(256)


class ConferenceSeries(tables.IsDescription):
    conference_series_index = tables.Int32Col()
    conference_series_id = tables.StringCol(8)
    # short name = tables.StringCol(256)
    # full name = tables.StringCol(256)


class FieldsOfStudy(tables.IsDescription):
    field_index = tables.Int32Col()
    field_id = tables.StringCol(8)
    # field_name = tables.StringCol(256)
