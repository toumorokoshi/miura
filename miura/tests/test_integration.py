"""
This file tests the whole stack of the miura tool.
"""
import os
import shlex
import miura
from jenkinsapi import jenkins
from mock import Mock, patch, call
from nose.tools import eq_


class TestMiura():

    def setUp(self):
        self.old_dir = os.path.abspath(os.curdir)
        self.test_dir = os.path.dirname(__file__)
        os.chdir(self.test_dir)
        self._jenkins = jenkins.Jenkins
        self.jenkinsapi_job = Mock()
        self.jenkinsapi_jenkins = Mock()
        self.jenkinsapi_jenkins.__getitem__ = Mock(return_value=self.jenkinsapi_job)
        jenkins.Jenkins = lambda *_: self.jenkinsapi_jenkins
        self._create_stdout_logger = miura._create_stdout_logger
        miura._create_stdout_logger = Mock()

    def tearDown(self):
        os.chdir(self.old_dir)
        jenkins.Jenkins = self._jenkins
        miura._create_stdout_logger = self._create_stdout_logger

    def test_base_case(self):
        miura.main(shlex.split('example'))
        assert self.jenkinsapi_job.update_config.called

    def test_delete(self):
        miura.main(shlex.split('-d example'))
        assert self.jenkinsapi_jenkins.delete_job.called

    def test_bad_script(self):
        with patch.object(miura, 'LOGGER') as logger:
            miura.main(shlex.split('boogyboogy'))
            logger.exception.assert_called_once_with("")

    def test_filter(self):
        miura.main(shlex.split('-f "foo=ba[r|z]" example'))
        eq_(self.jenkinsapi_jenkins.__getitem__.mock_calls,
            [call('bar'), call('baz')])
