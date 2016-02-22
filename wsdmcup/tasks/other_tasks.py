
import logging

from azure.storage.blob import BlobService

from wsdmcup.config import Config
from wsdmcup.timing import timeit


__author__ = 'damirah'
__email__ = 'damirah@live.com'


@timeit
def upload_results():
    """
    :return: None
    """
    logger = logging.getLogger(__name__)
    results_fpath = '/data/wsdm_cup/results/results.tsv'
    logger.info('Uploading results from {0}'.format(results_fpath))
    blob_service = BlobService(account_name='wsdmcupchallenge',
                               sas_token=Config.SAS_TOKEN)
    blob_service.put_block_blob_from_path(container_name='bletchleypark',
                                          blob_name='results.tsv',
                                          file_path=results_fpath)
    logger.info('Done uploading')
    return
