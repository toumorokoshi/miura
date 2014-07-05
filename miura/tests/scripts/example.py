def run(options, data):
    for job_name in data['foo']:
        yield {
            'host': 'host',
            'name': job_name,
            'template': 'test.xml',
            'job_data': {
                'test': 'test'
            }
        }
