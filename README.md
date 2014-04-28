miura
=====

a Jenkins job management tool. Miura can create, update, and delete on
mass for multiple jobs that vary slightly in configuration.

Usage
-----

to create jobs with miura, the following is needed:

* a job template, providing a template for a job
* a directory, containing one or more files storing data with yaml
* a python file, contaning

Tutorial
--------

### Getting Started

Let's start with the most basic example. Create a directory scripts,
and a file called example.py with the following:

    # scripts/example.py
    def run(options, data):
        yield {
            'host': JENKINS_HOST_URL
            'name': 'foo'
            'template': 'base.xml'
            'job_data': {}
        }

And choose a job you want to copy off of, and download it to templates/base.xml:

    # with wget (Linux)
    mkdir -p templates && wget $JENKS_JOB_URL/config.xml -O templates/base.xml
    # with curl (OSX)
    mkdir -p templates && curl $JENKINS_JOB_URL/config.xml -o templates/base.xml

And you're done! You can now create the foo job with:

    miura scripts/example.py

Or the shorthand:

    miura example

You can delete the jobs by passing in the script

    # delete jobs
    miura -d example

See miura -h for a full explanation.

### Using templates

Of course, this is not very helpful by itself. The real power of miura
comes from not just generating one job, but generating multiple. Let's
make a series of jobs that echo different messages to the console.

Jenkins configurations can change over time, so this tutorial isn't
going to include any examples of the xml that underlies jenkins
jobs. It's a good idea to get familiar with config.xml files yourself:
miura doesn't create these from scratch for you. Instead, miura
specializies templates you write based off a job you want to
replicate.

* create a freestyle jenkins job "template" that echos 'foo' from the command line.
* copy that job's config.xml file into templates/echo_template.xml.
    * you can access any job's config.xml file by hitting $JOB_URL/config.xml
* replace the 'foo' in the config.xml with '{{ message }}', so it looks like the following:

    <!-- your markup may vary -->
    <hudson.tasks.Shell>
      <command>echo &apos;{{ job_data.message }}&apos;</command>
    </hudson.tasks.Shell>

miura uses the [jinja2](http://jinja.pocoo.org/docs/) templating
language to specialize it's templates. In the example above, we're
going to pass into the template a different message of each job, which
will substitute {{message}} with a real value.

Modify the script.py from before with the following:

    # scripts/example.py
    def run(options, data):
        for echo_message in ('bar', 'baz', 'bat'):
            yield {
                'host': JENKINS_HOST_URL
                'name': 'echo-' + echo_message
                'template': 'echo_template.xml'
                'job_data': {
                    'message': echo_message
                }
            }

And you're done! if you run the job now, you'll make three jobs: 'echo-bar', 'echo-baz', and 'echo-bat'.

the run method in each script should yield a dictionary for each job
to generate. our example yields through each message we want to create
a job for, which miura in turn generates.

### Using data

So now we've covered how to generate multiple jobs. But storing all
our data with the script file is not very practical: we can't share
data among our scripts, and we can't share data filtering code

miura solves this problem by storing data in a separate format all
together, and passing an aggregate dictionary of values into each method.

Create a yaml file known as echo.yaml and add it to a directory data:

    # data/echo.yaml
    echo_messages:
      - 'bar'
      - 'baz'
      - 'bat'

Now we have a separation of data and function. We can now remove the data from our script:

    # scripts/example.py
    def run(options, data):
        for echo_message in data.get('echo_messages'):
            yield {
                'host': JENKINS_HOST_URL
                'name': 'echo-' + echo_message
                'template': 'echo_template.xml'
                'data': {
                    'message': echo_message
                }
            }

And you're done!

### filtering data

Now that we have our data in a format all our scripts can use, we can
share filtering logic as well. If you want to filter your data, you
can filter data with one or more filters:

    miura -f "echo_messages:ba[z|t]"

### Conclusion

We've covered:

* that miura runs commands through scripts (under scripts/)
* that miura uses jinja to render templates (under templates/)
* that miura can store data in a common location (under data/)

Ultimately, our folder structure looks like:

* /
    * data/
        * echo.yaml
    * scripts/
        * example.py
    * templates/
        * echo_template.xml
