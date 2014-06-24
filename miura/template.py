import os


class TemplateSet(object):

    def __init__(self, root_directory):
        self.root_directory = root_directory

    def get(self, template_name):
        template_path = os.path.join(self.root_directory,
                                     template_name)

        assert os.path.exists(template_path), "cannot find template {0} at {1}".format(
            template_name,
            template_path
        )
        assert not os.path.isdir(template_path), "template path {0} is a directory".format(template_path)

        with open(template_path, 'r') as template_file:
            return template_file.read()

    def __getitem__(self, name):
        return self.get(name)
