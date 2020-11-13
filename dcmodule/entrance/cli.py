from dcmodule import result_dump, execute_dcmodule
from dcmodule.configs.meta import __VERSION__, __TITLE__

import click
from click.core import Option, Context


# noinspection PyUnusedLocal
def print_version(ctx: Context, param: Option, value: bool):
    if not value or ctx.resilient_parsing:
        return
    click.echo('{title}, version {version}.'.format(title=__TITLE__.capitalize(), version=__VERSION__))
    ctx.exit()


_LINE_SEPARATOR_FOR_PRETTY_TABLE = "\n"


@click.command()
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True,
              help="Show package's version information.")
@click.option('--stdin', default=None, type=click.File())
@click.option('--stdout', default=None, type=click.File())
@click.option('--testfile', default=None, type=str)
def cli(stdin, stdout, testfile):
    if stdin is not None and stdout is not None:
        click.echo("stdin:" + stdin.read())
        click.echo("stdout:" + stdout.read())
    if testfile is not None:
        _success, _message, _data = execute_dcmodule(
            testfile,
            stdin="This is stdin.\r\nThis is next line!",
            stdout="This is \t\t stdout.",
        )
        click.echo(_success)
        click.echo(_message)
        click.echo(_data)
