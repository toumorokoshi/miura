from miura import runner
from mock import patch, Mock
from collections import defaultdict
from nose.tools import eq_, ok_
import os
import shutil
import tempfile


def test_jenkins_api_cache():
    with patch('jenkinsapi.jenkins.Jenkins') as Jenkins:
        return_value = object()
        Jenkins.return_value = return_value
        cache = runner.JenkinsApiCache()
        assert cache['foo'] is return_value


class TestJobParser(object):

    def setUp(self):
        self.template = "{{ job_data.foo }}"
        self.templates = defaultdict(lambda: self.template)
        self.job_runner = runner.JobParser(
            {},
            self.templates
        )

        self.jenkins = object()
        self.job_runner._jenkinsapi_cache = defaultdict(lambda: self.jenkins)

    def test_parse_job(self):
        yield_dict = {
            'host': 'host',
            'name': 'foo',
            'template': 'null',
            'job_data': {
                'foo': 'bar'
            }
        }

        def run_method(option, data):
            yield yield_dict

        result = self.job_runner.parse_job(
            run_method, []
        )

        result = next(result)

        assert isinstance(result, runner.MiuraJenkinsJob)
        assert result.jenkins_host is self.jenkins
        assert result.name == "foo"
        assert result.config_xml == "bar"


class TestMiuraJenkinsJob(object):

    def setUp(self):
        self.jenkins_host = Mock()
        self.jenkins_host.has_job.return_value = True
        self.jenkins_host.baseurl = "baseurl"
        self.name = "foo"
        self.config_xml = "bar"
        self.job = runner.MiuraJenkinsJob(
            self.jenkins_host,
            self.name,
            self.config_xml
        )

    def test_insert(self):
        with patch.object(self.jenkins_host, 'create_job') as create_job:
            self.jenkins_host.has_job.return_value = False
            self.job.upsert()
            create_job.assert_called_with(
                self.name,
                self.config_xml
            )

    def test_update(self):
        jenkins_job = Mock()
        jenkins_job.update_config = Mock()
        self.jenkins_host.__getitem__ = lambda k, d: jenkins_job
        self.job.upsert()
        jenkins_job.update_config.assert_called_once_with(
            self.config_xml
        )

    def test_delete(self):
        with patch.object(self.jenkins_host, 'delete_job') as delete_job:
            self.job.delete()
            delete_job.assert_called_once_with(self.name)

    def test_print_job(self):
        temp_dir = tempfile.mkdtemp()
        try:
            jenkins_job = Mock()
            jenkins_job.update_config = Mock()
            self.jenkins_host.__getitem__ = lambda k, d: jenkins_job
            self.job.print_job(temp_dir)
            file_name = "baseurl-foo.xml"
            target_pom = os.path.join(temp_dir, file_name)
            ok_(os.path.exists(target_pom))
            contents = None
            with open(target_pom) as fh:
                contents = fh.read()
            eq_(contents, "bar")
        finally:
            shutil.rmtree(temp_dir)

    def test_print_job_no_directory(self):
        temp_dir_root = tempfile.mkdtemp()
        temp_dir = os.path.join(temp_dir_root, "temp2")
        try:
            jenkins_job = Mock()
            jenkins_job.update_config = Mock()
            self.jenkins_host.__getitem__ = lambda k, d: jenkins_job
            self.job.print_job(temp_dir)
            ok_(os.path.exists(temp_dir))
        finally:
            shutil.rmtree(temp_dir_root)

    def test_dry_run(self):
        with patch.object(self.jenkins_host, 'delete_job') as delete_job:
            self.job.dry_run()
            assert not delete_job.called
