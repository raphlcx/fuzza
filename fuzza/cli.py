import click

from . import __version__
from . import __prog__
from .configuration import Configuration
from .encoder import Encoder


def validate_encoder(ctx, param, value):
    """
    Validate the encoder input. Input should consist only of the
    accepted type of encoding. Multiple values are comma-separated.
    """
    encoders = value.split(',')
    for enc in encoders:
        if enc not in Encoder.ACCEPTED_ENCODING:
            raise click.BadParameter(
                'invalid encoder: {encoder}. '
                '(choose from {choices})'
                .format(
                    encoder=value,
                    choices=', '.join(Encoder.ACCEPTED_ENCODING)
                )
            )
    return encoders


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
              metavar=(
                  '[{enc}[, ...]]'
                  .format(enc='|'.join(Encoder.ACCEPTED_ENCODING))
              ),
              callback=validate_encoder,
              help='List of encoding to be sequentially applied to fuzz data.')
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


if __name__ == '__main__':
    cli()
