"""Miura, a jenkins job management tool

Usage:
  miura docs
  miura [-d --dry-run -p <print_dir>] [-f <filter>...] <script_name> [<args>...]

Options:
  -h, --help                              Show this usage guide.
  -f <filter>..., --filter <filter>...    Filters
  -p <print_dir>, --print <print_dir>     Print the jobs out to a directory
  -d, --delete                            if set, will delete jobs
  --dry-run                               don't actually perform the operation
"""
from docopt import docopt
import logging
import os
import signal
import sys
from miura.exceptions import MiuraException

DATA_DIRECTORY = os.path.join(os.curdir, 'data')
SCRIPTS_DIRECTORY = os.path.join(os.curdir, 'scripts')
TEMPLATE_DIRECTORY = os.path.join(os.curdir, 'templates')

LOGGER = logging.getLogger(__name__)

from .script import MiuraScript


def signal_handler(signal, frame):
    print("\nShutting down miura...")
    sys.exit(0)


def main(argv=sys.argv[1:]):
    # add current directory to system path, if it's not on there already
    # this combats against buildout sandboxing sys.path
    if os.curdir not in sys.path:
        sys.path.append(os.curdir)
    signal.signal(signal.SIGINT, signal_handler)
    _create_stdout_logger()
    options = docopt(__doc__, argv=argv, options_first=True)
    try:
        filters = {}
        for filter_string in options['--filter']:
            key, value = _parse_filter_string(filter_string)
            filters[key] = value

        miura_script = MiuraScript(options['<script_name>'],
                                   DATA_DIRECTORY,
                                   SCRIPTS_DIRECTORY,
                                   TEMPLATE_DIRECTORY,
                                   data_filters=filters)
        if options['--delete']:
            miura_script.delete = True
        if options['--dry-run']:
            miura_script.dry_run = True
        if options['--print']:
            miura_script.print_directory = options['--print']
        miura_script()

    except (MiuraException, AssertionError):
        LOGGER.exception("")


def _parse_filter_string(filter_string):
    """ parse a filter string into a key-value pair """
    assert "=" in filter_string, "filter string requires an '=', got {0}".format(filter_string)
    split_values = filter_string.split('=')
    assert len(split_values) == 2, "more than one equals found in filter string {0}!".format(filter_string)
    return split_values


def _create_stdout_logger():
    """ create a logger to stdout """
    log = logging.getLogger(__name__)
    out_hdlr = logging.StreamHandler(sys.stdout)
    out_hdlr.setFormatter(logging.Formatter('%(message)s'))
    out_hdlr.setLevel(logging.INFO)
    log.addHandler(out_hdlr)
    log.setLevel(logging.INFO)
