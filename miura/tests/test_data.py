import os
from miura import data


FILE_DIRECTORY = os.path.dirname(__file__)
TEST_DATA_DIRECTORY = os.path.join(FILE_DIRECTORY, 'data')


def test_load_file_or_directory():
    results = list(data.load_file_or_directory(TEST_DATA_DIRECTORY))
    assert set(results) == set([
        os.path.abspath(os.path.join(TEST_DATA_DIRECTORY, 'test.yaml')),
        os.path.abspath(os.path.join(TEST_DATA_DIRECTORY, 'directory', 'foo.yaml')),
        os.path.abspath(os.path.join(TEST_DATA_DIRECTORY, 'directory', 'bar.yaml'))
    ])
