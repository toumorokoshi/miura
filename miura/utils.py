import os
import jinja2


def get_method_from_module(module_path, method_name):
    """ from a valid python module path, get the run method name passed """
    top_module = __import__(module_path)

    module = top_module
    # we tunnel down until we find the module we want
    for submodule_name in module_path.split('.')[1:]:
        module = getattr(module, submodule_name)

    assert hasattr(module, method_name), \
        "unable to find method {0} from module {1}. does the method exist?".format(method_name, module_path)
    return getattr(module, method_name)


def format_path_to_module(file_path):
    file_path = file_path.strip(" \n\t " + os.sep + os.curdir)
    return file_path.replace(os.sep, '.')


def specialize_content(content, data):
    """
    return a string from a jinja2 template <content> rendered with
    <data>
    """
    return jinja2.Template(content).render(**data)
