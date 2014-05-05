import os


def get_method_from_file(file_path, method_name):
    """ from a valid python file, get the method name passed """
    module_name = os.path.splitext(file_path)
    module = __import__(module_name, [0])
    assert hasattr(module, 'method_name'), \
        "unable to find method {0} from module {1}. does the method exist?".format(method_name, module_name)
