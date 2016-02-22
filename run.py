"""
Main file for running everything
"""

import sys
import logging
import logging.config

import wsdmcup.logging as wsdmlog
from wsdmcup.tasks.data_tasks import (
    papers_to_hdf5,
    citation_matrix_to_hdf5,
    authors_to_hdf5,
    authorship_matrix_to_hdf5,
    affiliations_to_hdf5,
    author_sequence_matrix_to_hdf5,
    journals_to_hdf5,
    conference_series_to_hdf5,
    fields_of_study_to_hdf5,
    h_index_to_hdf5,
)
from wsdmcup.tasks.ranking_tasks import (
    rank,
)
from wsdmcup.tasks.other_tasks import (
    upload_results,
)

__author__ = 'damirah'
__email__ = 'damirah@live.com'


# =======================
#     MENUS FUNCTIONS
# =======================

def exit_app(logger):
    logger.info('Exiting')
    exit()


def menu(logger):
    """
    Just print help
    :return: None
    """
    print('Possible actions:')
    print('=================')
    for key in sorted(menu_actions):
        print('{0}: {1}'.format(key, menu_actions[key].__name__))
    print('Please select option(s)')
    actions = [i.lower() for i in list(sys.stdin.readline().strip())]
    exec_action(actions, logger)
    return


def exec_action(actions, logger):
    """
    Execute selected action
    :param actions:
    :param logger:
    :return: None
    """
    if not actions:
        menu_actions['x'](logger)
    else:
        # try:
            logger.info('Selected the following options: {0}'.format(
                [(key, menu_actions[key].__name__) for key in actions]))
            for action in actions:
                menu_actions[action]()
        # except KeyError:
        #     print("Invalid selection, please try again.\n")
        #     menu_actions['x'](logger)
    return


# =======================
#    MENUS DEFINITIONS
# =======================

menu_actions = {
    '0': papers_to_hdf5,
    '1': citation_matrix_to_hdf5,
    '2': authors_to_hdf5,
    '3': authorship_matrix_to_hdf5,
    '4': affiliations_to_hdf5,
    '5': author_sequence_matrix_to_hdf5,
    '6': journals_to_hdf5,
    '7': conference_series_to_hdf5,
    '8': fields_of_study_to_hdf5,
    '9': h_index_to_hdf5,
    # =====================================
    'a': rank,
    # =====================================
    'w': exit_app,
    'x': menu,
    'y': upload_results,
}


# =======================
#      MAIN PROGRAM
# =======================

if __name__ == '__main__':
    wsdmlog.setup_logging()
    main_logger = logging.getLogger(__name__)
    try:
        menu(main_logger)
    except Exception as e:
        main_logger.exception(e, exc_info=True)
