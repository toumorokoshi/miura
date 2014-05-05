"""Miura, a jenkins job management tool

Usage:
  miura docs
  miura [-d] [-f <filter>...] <script_name> [<args>...]

Options:
  -h, --help                              Show this usage guide.
  -f <filter>..., --filter <filter>...    Filters
  -d, --delete                            if set, will delete jobs
"""
import docopt
import logging
import os
import signal
import sys

DATA_DIRECTORY = os.path.join(os.curdir, 'data')
SCRIPTS_DIRECTORY = os.path.join(os.curdir, 'scripts')
TEMPLATE_DIRECTORY = os.path.join(os.curdir, 'templates')

LOGGER = logging.getLogger(__name__)

from .script import MiuraScript

def signal_handler(signal, frame):
    print("\nShutting down miura...")
    sys.exit(0)


def main(argv=sys.argv[1:]):
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
                                   TEMPLATE_DIRECTORY)
        if options['--delete']:
            miura_script.delete = True
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
