from miura import runner

class RunTests(object):
    """ Run Tests in Miura """

    def test_create_single_job(self):
        host = 'http://localhost:9000'
        name = 'foo'
        template = 'base.xml'
        job_data = {}

        def run(options, data):
            yield {
                'host': host,
                'name': name,
                'template': template,
                'job_data': job_data
            }

        runner.run(run, {})
