"""
fuzza.cli
---------

Entry point to the application.
"""
import click

from . import __description__
from . import __prog__
from . import __version__
from . import configuration as Configuration
from . import data as Data
from . import dispatcher as Dispatcher
from . import transformer as Transformer
from . import protocol as Protocol
from . import templater as Templater


def validate_comma_separated(ctx, param, value):
    """
    Validate multiple string input values are comma-separated. Each of
    the value is put into a list, which is returned after validation.
    """
    if value is None:
        return

    return value.split(',')


@click.group(help=__description__)
@click.version_option(version=__version__, prog_name=__prog__)
def cli():
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
    '-c',
    '--data-chunk',
    is_flag=True,
    help='Read each fuzz data file in chunk, instead of line-by-line. [False]'
)
@click.option(
    '--template-path',
    type=str,
    metavar='[path]',
    help='Path containing template files. Support glob patterns. []'
)
@click.option(
    '--dispatcher',
    type=str,
    metavar='[dispatcher]',
    help='Type of dispatcher to use. [tcp]'
)
@click.option(
    '-r',
    '--dispatcher-reuse',
    is_flag=True,
    help='Enable dispatcher connection reuse. [False]'
)
@click.option(
    '--transformer',
    type=str,
    metavar='[transformer[, ...]]',
    callback=validate_comma_separated,
    help='List of transformations to be sequentially applied to fuzz data. []'
)
@click.option(
    '--protocol',
    type=str,
    metavar='[protocol]',
    help='Type of communication protocol. [textual]'
)
def init(**kwargs):
    """
    Create a fuzzer configuration file.
    """
    # Store configuration to file
    conf = Configuration.load(kwargs)
    Configuration.to_file(conf)


@cli.command()
def fuzz():
    """
    Execute the fuzzer.
    """
    # Read configuration from file
    conf = Configuration.from_file()
    conf = Configuration.load(conf)

    # Load fuzz data and template
    data = Data.read(conf)
    templates = Templater.read(conf)

    # Transform the data using transformer
    transform = Transformer.init(conf)
    data = transform(data)

    # Initialize a dispatcher
    dispatch = Dispatcher.init(conf)

    # Initialize a protocol adapter
    adapt = Protocol.init(conf)

    # Dispatch the payloads
    payload = b''
    for payload in Templater.render(templates, data):
        dispatch(adapt(payload))

    # Hack: Ensure connection is closed by re-sending the last payload
    dispatch(adapt(payload), True)

if __name__ == '__main__':
    cli()
