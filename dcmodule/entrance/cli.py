import click
from click.core import Context, Option

from dcmodule import execute_dcmodule, result_dump
from dcmodule.configs.meta import __TITLE__, __VERSION__


# noinspection PyUnusedLocal
def print_version(ctx: Context, param: Option, value: bool):
    if not value or ctx.resilient_parsing:
        return
    click.echo('{title}, version {version}.'.format(title=__TITLE__.capitalize(), version=__VERSION__))
    ctx.exit()


_LINE_SEPARATOR_FOR_PRETTY_TABLE = "\n"

CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)


@click.command(context_settings=CONTEXT_SETTINGS, help="Run dcmodule to help check data validity.")
@click.option('-v', '--version', is_flag=True,
              callback=print_version, expose_value=False, is_eager=True, help="Show package's version information.")
@click.option('-i', '--input', default=None, type=str, help="Input content (Priority above input_file)")
@click.option('-o', '--output', default=None, type=str,
              help="Output content (Priority above output_file)")
@click.option('-if', '--input_file', default=None, type=click.File(), help="Input file")
@click.option('-of', '--output_file', default=None, type=click.File(), help="Output file")
@click.option('-tf', '--testfile', default=None, type=str, help="data test file")
def cli(input, output, input_file, output_file, testfile):
    in_content = ""
    out_content = ""
    if input is not None:
        in_content = input
    else:
        in_content = input_file.read()
    if output is not None:
        out_content = output
    else:
        out_content = output_file.read()
    if testfile is None:
        result_dump(True, data={
            "input": in_content,
            "output": out_content,
        })
    else:
        _success, _message, _data = execute_dcmodule(
            testfile,
            stdin=in_content,
            stdout=out_content,
        )
        click.echo(_success)
        click.echo(_message)
        click.echo(_data)
