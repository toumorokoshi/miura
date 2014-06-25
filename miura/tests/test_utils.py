from miura import utils


class TestSpecializeContent(object):

    def test_specialize_content(self):
        template = "{{ name }}, {{ foo }}"
        job_data = {
            "foo": "hello world",
            "name": "foojob"
        }
        output = utils.specialize_content(
            template,
            job_data
        )
        assert output == "foojob, hello world"


def test_format_path_to_module():
    test_path = "./foo.py"
    assert utils.format_path_to_module(test_path) == "foo.py"


def test_get_method_from_module():
    method = utils.get_method_from_module(
        'miura.utils',
        'format_path_to_module'
    )
    assert method is utils.format_path_to_module
