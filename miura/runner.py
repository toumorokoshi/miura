import os
import logging
from utils import specialize_content
from jenkinsapi import jenkins

LOGGER = logging.getLogger(__name__)


class JenkinsApiCache(dict):

    def __missing__(self, key):
        self[key] = jenkins.Jenkins(key)
        return self[key]


class JobParser(object):

    def __init__(self, data, templates):
        self._data = data
        self._templates = templates
        self._jenkinsapi_cache = JenkinsApiCache()

    def parse_job(self, run_method, options):
        """
        Generates and returns a job object with the following:

        * a run method, as defined in the readme
        * a list of posix-like arguments
        * a dictionary of data
        * templates: a dict-like interface of (template_name, template_body) pairs
        """

        for job_dict in run_method(options, self._data):

            # unpackaging dict
            host = job_dict['host']
            name = job_dict['name']
            template = job_dict['template']
            job_data = {
                'name': name,
                'host': host,
                'job_data': job_dict['job_data']
            }

            template_body = self._templates[template]
            config_xml = specialize_content(template_body, job_data)

            yield MiuraJenkinsJob(
                self._jenkinsapi_cache[host],
                name,
                config_xml
            )


class MiuraJenkinsJob(object):
    """
    A representation of a jenkins job in miura

    jenkins_host: jenkinsapi.Jenkins instance
    name: name of the job
    config_xml: body of the config.xml
    """

    def __init__(self, jenkins_host, name, config_xml):
        self.jenkins_host = jenkins_host
        self.name = name
        self.config_xml = config_xml

    def upsert(self):
        """ create or update the jenkins job """
        if not self.jenkins_host.has_job(self.name):
            LOGGER.info("creating {0}...".format(self.name))
            self.jenkins_host.create_job(self.name, self.config_xml)
        else:
            jenkins_job = self.jenkins_host[self.name]
            LOGGER.info("updating {0}...".format(self.name))
            jenkins_job.update_config(self.config_xml)

    def delete(self):
        """ delete the jenkins job, if it exists """
        if self.jenkins_host.has_job(self.name):
            LOGGER.info("deleting {0}...".format(self.name))
            self.jenkins_host.delete_job(self.name)

    @staticmethod
    def _escape_string(string):
        return string.replace('/', '')

    def print_job(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

        job_filename = "{0}-{1}.xml".format(
            self._escape_string(self.jenkins_host.baseurl), self.name
        )

        with open(os.path.join(directory, job_filename), 'w+') as fh:
            fh.write(self.config_xml)

    def dry_run(self):
        """ print information about the jenkins job """
        LOGGER.info("Job Info: {name} -> {host}".format(
            name=self.name,
            host=self.jenkins_host.baseurl
        ))
