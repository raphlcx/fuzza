"""
fuzza.cli
---------

Entry point to the application.
"""
import click

from . import __prog__
from . import __version__
from . import data as Data
from . import dispatcher as Dispatcher
from . import encoder as Encoder
from . import protocol as Protocol
from . import templater as Templater
from .configuration import Configuration


def validate_comma_separated(ctx, param, value):
    """
    Validate multiple string input values are comma-separated. Each of
    the value is put into a list, which is returned after validation.
    """
    if value is None:
        return

    return value.split(',')


@click.group()
@click.version_option(version=__version__, prog_name=__prog__)
def cli():
    """
    A generic template-based fuzzer.
    """
    pass


@cli.command()
@click.option(
    '--host',
    type=str,
    metavar='<host>',
    prompt='Target hostname or IP',
    help='The hostname of target to fuzz.'
)
@click.option(
    '--port',
    type=int,
    metavar='<port>',
    prompt='Target port',
    help='The port of target to fuzz.'
)
@click.option(
    '--data-path',
    type=str,
    metavar='<path>',
    prompt='Path to fuzz data',
    help='Path containing fuzz data. Support glob patterns.'
)
@click.option(
    '--template-path',
    type=str,
    metavar='[path]',
    help='Path containing template files. Support glob patterns.'
)
@click.option(
    '--dispatcher',
    type=str,
    metavar='[dispatcher]',
    help='Dispatcher module to use.'
)
@click.option(
    '-r',
    '--reuse',
    is_flag=True,
    help='Enable dispatcher connection reuse.'
)
@click.option(
    '--encoder',
    type=str,
    metavar='[encoder[, ...]]',
    callback=validate_comma_separated,
    help='List of encoder modules to be sequentially applied to fuzz data.'
)
@click.option(
    '--protocol',
    type=str,
    metavar='[protocol]',
    help='Type of communication protocol.'
)
def init(**kwargs):
    """
    Create a fuzzer configuration file.
    """
    Configuration.load(kwargs)
    Configuration.to_file()


@cli.command()
def fuzz():
    """
    Execute the fuzzer.
    """
    conf = Configuration.from_file()
    Configuration.load(conf)

    # Load fuzz data and template
    data = Data.read(Configuration.CONFIG)
    templates = Templater.read(Configuration.CONFIG)

    # Encode the data using encoder
    encode = Encoder.init(Configuration.CONFIG)
    data = encode(data)

    # Initialize a dispatcher
    dispatch = Dispatcher.init(Configuration.CONFIG)

    # Initialize a protocol adapter
    adapt = Protocol.init(Configuration.CONFIG)

    # Dispatch the payloads
    for payload in Templater.render(templates, data):
        dispatch(adapt(payload))

    # Hack: Ensure connection is closed by re-sending the last payload
    dispatch(adapt(payload), True)

if __name__ == '__main__':
    cli()
