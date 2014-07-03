import os
import re
import yaml
from .exceptions import MiuraException
import logging

logger = logging.getLogger(__name__)


def load_data_from_path(path):
    file_paths = load_file_or_directory(path)
    return retrieve_data(file_paths)


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
        with open(file_path) as fh:
            try:
                content = yaml.load(fh.read())
            except yaml.YAMLError as e:
                raise MiuraException(
                    "Unable to parse yaml at {0}: \n {1}".format(
                        file_path,
                        str(e)
                    ))
            if not isinstance(content, dict):
                raise MiuraException(
                    "{0} is does not translate to a dictionary!".format(file_path)
                )
            data_dict.update(content)
    return data_dict


def filter_data(data, filter_dict):
    """ filter a data dictionary for values only matching the filter """
    for key, match_string in filter_dict.items():
        if key not in data:
            logger.warning("{0} doesn't match a top level key".format(key))
            continue
        values = data[key]
        matcher = re.compile(match_string)
        if isinstance(values, list):
            values = [v for v in values if matcher.search(v)]
        elif isinstance(values, dict):
            values = dict((k, v) for k, v in values.items() if matcher.search(k))
        else:
            raise MiuraException("cannot filter a {0}".format(type(values)))
        data[key] = values
