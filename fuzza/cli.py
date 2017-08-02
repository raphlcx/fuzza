"""
fuzza.cli
---------

Entry point to the application.
"""
import click

from . import __prog__
from . import __version__
from .configuration import Configuration
from .data_broker import DataBroker
from .dispatcher import Dispatcher
from .encoder import Encoder
from .protocol import Protocol
from .templater import Templater


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
@click.option('--host',
              type=str,
              metavar='<host>',
              prompt='Target hostname or IP',
              help='The hostname of target to fuzz.')
@click.option('--port',
              type=int,
              metavar='<port>',
              prompt='Target port',
              help='The port of target to fuzz.')
@click.option('--data-path',
              type=str,
              metavar='<path>',
              prompt='Path to fuzz data',
              help='Path containing fuzz data. Support glob patterns.')
@click.option('--template-path',
              type=str,
              metavar='[path]',
              help='Path containing template files. Support glob patterns.')
@click.option('--encoder',
              type=str,
              metavar='[encoder[, ...]]',
              callback=validate_comma_separated,
              help='List of encoding to be sequentially applied to fuzz data.')
@click.option('--protocol',
              type=click.Choice(Protocol.ACCEPTED_PROTOCOL),
              help='Type of communication protocol.')
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

    databrk = DataBroker(Configuration.CONFIG)
    databrk.scan()

    templater = Templater(Configuration.CONFIG)
    templater.scan()

    encoder = Encoder(Configuration.CONFIG)
    data = encoder.encode(databrk.data)

    dispatcher = Dispatcher(Configuration.CONFIG)
    protocol = Protocol(Configuration.CONFIG)

    for payload in templater.render(data):
        dispatcher.connect()
        dispatcher.dispatch(protocol.convert(payload))
        dispatcher.close()


if __name__ == '__main__':
    cli()
