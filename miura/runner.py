from utils import specialize_content
from jenkinsapi.jenkins import Jenkins


class JenkinsApiCache(dict):

    def __missing__(self, key):
        self[key] = Jenkins(key)
        return self[key]


def parse_job(run_method, options, data, templates):
    """
    Generates and returns a job object with the following:

    * a run method, as defined in the readme
    * a list of posix-like arguments
    * a dictionary of data
    * templates: a dict-like interface of (template_name, template_body) pairs
    """
    jenkinsapi_cache = JenkinsApiCache()

    for job_dict in run_method(options, data):

        # unpackaging dict
        host = job_dict['host']
        name = job_dict['name']
        template = job_dict['template']
        job_data = job_dict['job_data']

        template_body = templates[template]
        config_xml = generate_config_xml(template_body, job_data)

        yield MiuraJenkinsJob(
            jenkinsapi_cache[host],
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
            self.jenkins_host.create_job(self.name, self.config_xml)
        else:
            jenkins_job = self.jenkins_host[self.name]
            jenkins_job.update_config(self.config_xml)

    def delete(self):
        """ delete the jenkins job, if it exists """
        if self.jenkins_host.has_job(self.name):
            self.jenkins_host.delete_job(self.name)
