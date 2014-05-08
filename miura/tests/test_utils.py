from miura import utils


class TestSpecializeContent(object):

    def test_specialize_content(self):
        template = "{{ name }}, {{ foo }}"
        job_data = {
            "foo": "foojob, hello world",
            "name": "foojob"
        }
        output = utils.specialize_content(
            template,
            job_data
        )
        assert output == "foojob, hello world"
