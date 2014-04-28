from .generator import generate_config_xml
from jenkinsapi.jenkins import Jenkins


class JenkinsApiCache(dict):

    def __missing__(self, key):


def parse_job(run_method, options, data, templates):
    """
    Generates and returns a job object with the following:

    * a run method, as defined in the readme
    * a list of posix-like arguments
    * a dictionary of data
    * templates: a dict-like interface of (template_name, template_body) pairs
    """
    jenkinsapi_cache = {}

    for job_dict in run_method(options, data):

        # unpackaging dict
        host = job_dict['host']
        name = job_dict['name']
        template = job_dict['template']
        job_data = job_dict['job_data']

        template_body = templates[template]
        config_xml = generate_config_xml(template_body, job_data)

        yield MiuraJenkinsJob(

class MiuraJenkinsJob(object):
    """ A representation of a jenkins job in miura """

    def __init__(self, jenkinshost, name, job_template):
        self.jenkinshost = jenkinshost
        self.name = name
        self.job_template = job_template

    def upsert_job(self):
        """ create or update the jenkins job """
