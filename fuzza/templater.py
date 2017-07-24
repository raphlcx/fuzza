import glob
import io

from string import Template


class Templater(object):
    """
    Reponsible for applying fuzz data to template file.

    Args:
        config: A `dict` containing the configurations.
    """

    def __init__(self, config):
        self._data_path = config.get('data_path')
        self._template_path = config.get('template_path')
        self._data = []
        self._template = []

    def scan(self):
        """
        Scan data path and template path for data files and template
        files respectively, and then store the file contents to relevant
        data store.

        The contents are currently loaded eagerly when this method is
        invoked. Therefore, a large memory space may be required if
        there are numerous data or templates.
        """
        for df in glob.iglob(self._data_path):
            with io.open(df, 'rt', encoding='utf-8') as f:
                self._data += f.read().splitlines()

        for tf in glob.iglob(self._template_path):
            with io.open(tf, 'rt', encoding='utf-8') as f:
                self._template.append(f.read())

    def render(self):
        """
        Render data into templates.

        This method is a generator function.
        """
        for t in self._template:
            for d in self._data:
                yield Template(t).safe_substitute(fuzzdata=d)
