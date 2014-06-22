import os
from miura import data
from miura.exceptions import MiuraException
from nose.tools import raises


FILE_DIRECTORY = os.path.dirname(__file__)
DATA_DIRECTORY = os.path.join(FILE_DIRECTORY, 'data')
BAD_DATA_DIRECTORY = os.path.join(FILE_DIRECTORY, 'bad_data')


def test_load_file_or_directory():
    results = list(data.load_file_or_directory(DATA_DIRECTORY))
    assert set(results) == set([
        os.path.abspath(os.path.join(DATA_DIRECTORY, 'test.yaml')),
        os.path.abspath(os.path.join(DATA_DIRECTORY, 'directory', 'foo.yaml')),
        os.path.abspath(os.path.join(DATA_DIRECTORY, 'directory', 'bar.yaml'))
    ])


def test_load_file_or_directory_file():
    file_path = os.path.join(DATA_DIRECTORY, 'test.yaml')
    results = list(data.load_file_or_directory(file_path))
    assert set(results) == set([
        os.path.abspath(os.path.join(DATA_DIRECTORY, 'test.yaml')),
    ])


def test_retrieve_data():
    """ retrieve data should load and merge files """
    file_paths = [
        os.path.abspath(os.path.join(DATA_DIRECTORY, 'directory', 'foo.yaml')),
        os.path.abspath(os.path.join(DATA_DIRECTORY, 'directory', 'bar.yaml'))
    ]
    assert data.retrieve_data(file_paths) == {
        'foo': ['test', 'foo'],
        'bar': ['test', 'bar']
    }


@raises(MiuraException)
def test_retrieve_data_bad_yaml():
    """ bad yaml should raise a miura exception """
    bad_yaml_path = os.path.join(BAD_DATA_DIRECTORY, 'bad.yaml')
    data.retrieve_data([bad_yaml_path])


@raises(MiuraException)
def test_retrieve_data_list_yaml():
    """ yaml that evaluates to a list should raise a miura exception """
    list_yaml_path = os.path.join(BAD_DATA_DIRECTORY, 'list.yaml')
    data.retrieve_data([list_yaml_path])


def test_load_data_from_path():
    directory = os.path.join(FILE_DIRECTORY, 'data', 'directory')
    assert data.load_data_from_path(directory) == {
        'foo': ['test', 'foo'],
        'bar': ['test', 'bar']
    }
