import os

from miura import runner
from .utils import get_method_from_module, format_path_to_module
from .data import load_data_from_path
from .template import TemplateSet

DEFAULT_DATA_DIRECTORY = os.path.join(os.curdir, 'data')
DEFAULT_TEMPLATE_DIRECTORY = os.path.join(os.curdir, 'templates')
DEFAULT_SCRIPTS_DIRECTORY = os.path.join(os.curdir, 'scripts')


class MiuraScript(object):

    delete = False  # if true, delete the jobs instead of upserting them

    def __init__(self, script_name,
                 data_directory,
                 scripts_directory,
                 template_directory
                 ):
        self.script_name = script_name
        self.data_directory = data_directory
        self.scripts_directory = scripts_directory
        self.template_directory = template_directory
        self.method_options = {}

    def __call__(self):
        target_module = "{0}.{1}".format(
            format_path_to_module(self.scripts_directory),
            self.script_name
        )

        run_method = get_method_from_module(target_module, 'run')
        data = load_data_from_path(self.data_directory)
        templates = TemplateSet(self.template_directory)

        if self.delete:
            target_method = 'delete'
        else:
            target_method = 'upsert'

        job_parser = runner.JobParser(
            self.method_options,
            templates,
        )

        for job in job_parser.parse_job(run_method, self.method_options,
                                        data, templates):
            getattr(job, target_method)()
