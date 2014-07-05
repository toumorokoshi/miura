import miura
from mock import patch
from nose.tools import eq_, raises


def test_create_stdout_logger():
    with patch('logging.getLogger'):
        miura._create_stdout_logger()


def test_signal_handler():
    with patch('sys.exit') as exit:
        miura.signal_handler(None, None)
        assert exit.called


def test_parse_filter_string():
    filter_string_tests = {
        'foo=bar': ('foo', 'bar')
    }

    def assert_output(filter_string, output):
        key, value = miura._parse_filter_string(filter_string)
        eq_(key, output[0])
        eq_(value, output[1])

    for filter_string, output in filter_string_tests.items():
        yield assert_output, filter_string, output


@raises(AssertionError)
def test_multiple_equals_string():
    miura._parse_filter_string("foo===bar")


@raises(AssertionError)
def test_no_equals_string():
    miura._parse_filter_string("foobarbaz")
