
import os.path


__author__ = 'damirah'
__email__ = 'damirah@live.com'


class Config(object):

    SAS_TOKEN = ('sas_token_here')

    APP_ROOT = '/data/wsdm_cup/'

    MAG_DIR = 'mag_20151106/'
    HDF5_DIR = 'hdf5/'
    TEMP_DIR = 'temp_files/'
    OUT_DIR = 'out/'
    LOG_DIR = 'log/'
    RESULTS_DIR = 'results/'

    OPCIT_ROOT = '/data/opcit/'

    DATASTORE_FNAME = 'data.h5'
    RESULTS_FNAME_PATTERN = 'results_s%03d.tsv'
    RESULTS_UPLOAD_FNAME = 'results.tsv'

    @staticmethod
    def get_path_to_data_file(file_name):
        return os.path.join(Config.APP_ROOT, Config.MAG_DIR, file_name)

    @staticmethod
    def get_path_to_results_file(file_name):
        return os.path.join(Config.APP_ROOT, Config.RESULTS_DIR, file_name)

    @staticmethod
    def get_path_to_hdf5_file(file_name):
        return os.path.join(Config.APP_ROOT, Config.HDF5_DIR, file_name)

    @staticmethod
    def get_path_to_out_file(file_name):
        return os.path.join(Config.APP_ROOT, Config.OUT_DIR, file_name)

    @staticmethod
    def get_path_to_log_file(file_name):
        return os.path.join(Config.APP_ROOT, Config.LOG_DIR, file_name)

    @staticmethod
    def get_path_to_opcit_file(file_name):
        return os.path.join(Config.APP_ROOT, Config.OPCIT_ROOT, file_name)

    @staticmethod
    def get_next_results_file_path():
        i = 1
        while os.path.exists(Config.get_path_to_results_file(
                Config.RESULTS_FNAME_PATTERN) % i):
            i += 1
        return Config.get_path_to_results_file(Config.RESULTS_FNAME_PATTERN) % i

    @staticmethod
    def get_results_upload_path():
        return Config.get_path_to_results_file(Config.RESULTS_UPLOAD_FNAME)
