import os
import jinja2


def get_method_from_file(file_path, method_name):
    """ from a valid python file, get the run method name passed """
    module_path = os.path.splitext(file_path)[0].replace(os.sep, '.')
    module = __import__(module_path)
    assert hasattr(module, 'method_name'), \
        "unable to find method {0} from module {1}. does the method exist?".format(method_name, module_path)
    return getattr(module, method_name)

def specialize_content(content, data):
    """ 
    return a string from a jinja2 template <content> rendered with
    <data>
    """
    return jinja2.Template(content).render(**data)
