import os
from miura.template import TemplateSet
from nose.tools import raises

FILE_DIRECTORY = os.path.dirname(__file__)
TEMPLATE_DIRECTORY = os.path.join(FILE_DIRECTORY, 'templates')


class TestTemplateSet(object):

    def setUp(self):
        self.template_set = TemplateSet(TEMPLATE_DIRECTORY)

    def test_get_template(self):
        assert self.template_set.get('test.xml').strip() == "{{ test }}"

    def test_get_template_key_getitem(self):
        assert self.template_set['test.xml'].strip() == "{{ test }}"

    @raises(AssertionError)
    def test_get_nonexistent_template(self):
        """ retrieving a non-existent template should return an exception """
        self.template_set.get('nonexistenttemplate.xml')

    @raises(AssertionError)
    def test_get_template_directory(self):
        """ when a directory is requested, an exception should be thrown """
        self.template_set.get('directory')
