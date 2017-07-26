import glob
import io

from string import Template


class Templater(object):
    """
    Reponsible for applying fuzz data to template file.

    Args:
        config: A `dict` containing the fuzzer configurations.

    Attributes:
        _template_path: Path to template files as specified in
            configuration.
        _template: A list of template loaded from template files.
    """

    def __init__(self, config):
        self._template_path = config.get('template_path')
        self._template = []

    def scan(self):
        """
        Scan template path for template files.
        """
        for tf in glob.iglob(self._template_path):
            with io.open(tf, 'rt', encoding='utf-8') as f:
                self._template.append(f.read())

    def render(self, data):
        """
        Render data into templates, and yield the rendered templates.
        If no template is supplied, yield the data directly.

        Args:
            data: A list containing the data.

        Returns:
            A generator yielding each of the payload.
        """
        if not self._template:
            for d in data:
                yield d

        else:

            for t in self._template:
                for d in data:
                    yield Template(t).safe_substitute(fuzzdata=d)
