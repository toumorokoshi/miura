from .constants import JENKINS_HOST_URL

# scripts/example.py
def run(options, data):
    yield {
        'host': JENKINS_HOST_URL
        'name': 'foo'
        'template': 'base.xml'
        'job_data': {}
    }
