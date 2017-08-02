"""
fuzza.templater
---------------

This module is used to handle the reading of template file and its
rendering with fuzz data.
"""
import glob
import io
import logging

from .logger import Logger

LOGGER = Logger.get_logger(__name__)
IS_DEBUG = LOGGER.isEnabledFor(logging.DEBUG)


def read(config):
    """
    Read template from template files.

    Args:
        config (dict): The fuzzer configuration.

    Returns:
        list: The list of templates.
    """
    template_path = config.get('template_path')
    templates = []

    if template_path is not None:

        for tfile in glob.iglob(template_path):
            with io.open(tfile, 'rb') as f:
                templates.append(f.read())

    LOGGER.info(
        'Found %d templates from %s',
        len(templates),
        template_path
    )

    return templates


def render(templates, data):
    """
    Render data into template to generate payload. This is a generator
    and yields the payload in each iteration.

    Args:
        templates (list): A list containing the templates.
        data (list): A list containing the data.

    Returns:
        str: The payload in bytes literals.
    """
    if not templates:
        for d in data:
            yield d

    else:

        for template in templates:
            for d in data:
                yield template.replace(b'$fuzzdata', d)
