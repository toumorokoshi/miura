import os
from miura import script
from mock import patch, Mock

FILE_DIRECTORY = os.path.dirname(__file__)
DATA_DIRECTORY = os.path.join(os.curdir, 'data')
TEMPLATE_DIRECTORY = os.path.join(os.curdir, 'templates')
SCRIPTS_DIRECTORY = os.path.join(os.curdir, 'scripts')


class TestMiuraScript(object):

    def setUp(self):
        self._directory = os.path.abspath(os.curdir)
        os.chdir(os.path.dirname(__file__))
        self.miura_script = script.MiuraScript(
            'example',
            DATA_DIRECTORY,
            SCRIPTS_DIRECTORY,
            TEMPLATE_DIRECTORY
        )

    def tearDown(self):
        os.chdir(self._directory)

    def test_script(self):
        with patch('miura.runner.JobParser.parse_job') as jobs:
            job = Mock()
            job.upsert = Mock()
            jobs.return_value = [job]
            self.miura_script()
            assert job.upsert.called

    def test_script_delete(self):
        with patch('miura.runner.JobParser.parse_job') as jobs:
            job = Mock()
            job.delete = Mock()
            jobs.return_value = [job]
            self.miura_script.delete = True
            self.miura_script()
            assert job.delete.called
