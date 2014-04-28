import yaml
import os


def load_file_or_directory(path):
    """
    given a path, determine if the path is a file or directory, and
    yield a list of absolute file paths
    """
    assert os.path.exists(path), "{0} does not exist!".format(path)
    absolute_path = os.path.abspath(path)
    if not os.path.isdir(path):
        yield absolute_path
    else:
        for root, dirs, file_paths in os.walk(path):
            for file_path in file_paths:
                yield os.path.join(root, file_path)


def retrieve_data(file_paths):

    """
    passed an iterable list of file_paths, loop through all of them and
    generate a dictionary containing all the context
    """
    data_dict = {}
    for file_path in file_paths:
        content = yaml.load(file_path)
        assert isinstance(content, dict), \
            "{0} is does not translate to a dictionary!".format(file_path)
        data_dict.update(content)
    return data_dict
