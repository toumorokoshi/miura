from miura import generator


class GeneratorTests(object):

    def test_generator(self):
        template = "{{ name }}, {{ job_data.foo }}"
        name = "foojob"
        job_data = {
            "foo": "foojob, hello world"
        }
        output = generator.generate_config_xml(
            template,
            name,
            job_data
        )
        assert output == "hello world"
