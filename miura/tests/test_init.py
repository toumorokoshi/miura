from miura import _parse_filter_string


class TestParseFilterString(object):

    def parse_filter_string_no_equals(self):
        """ _parse_filter_string with no equals should raise an exception """
