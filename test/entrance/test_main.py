from dcmodule import result_dump, execute_dcmodule
from dcmodule.configs.version import version

import codecs
import getopt
import sys
import click
from click.core import Option, Context
from contextlib import contextmanager

__TITLE__ = "dcmodule"
__VERSION__ = version


# noinspection PyUnusedLocal
def print_version(ctx: Context, param: Option, value: bool):
    if not value or ctx.resilient_parsing:
        return
    click.echo('{title}, version {version}.'.format(title=__TITLE__.capitalize(), version=__VERSION__))
    ctx.exit()


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)

_LINE_SEPARATOR_FOR_PRETTY_TABLE = "\n"


@click.command(context_settings=CONTEXT_SETTINGS)
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


def parse_from_args(args=None):
    args = args or sys.argv
    opts, args = getopt.getopt(args[1:], "", ["stdin_file=", "stdout_file="])

    _stdin = None
    _stdout = None
    for _key, _value in opts:
        if _key == "--stdin_file":
            with codecs.open(_value, "r") as _file:
                _stdin = _file.read()

        elif _key == "--stdout_file":
            with codecs.open(_value, "r") as _file:
                _stdout = _file.read()
    return _stdin, _stdout


@contextmanager
def load_with_args(args=None):
    """
    with形式加载输入参数
    :param args: 命令行参数列表（缺省为自动获取）
    """
    cli()
    yield _stdin, _stdout


def print_version(ctx: Context, param: Option, value: bool):
    if not value or ctx.resilient_parsing:
        return
    click.echo(version)


CONTEXT_SETTINGS = dict(
    help_option_names=['-h', '--help']
)

if __name__ == "__main__":
    with load_with_args() as _iotuple:
        _stdin, _stdout = _iotuple
        result_dump(True, data={
            "stdin": _stdin,
            "stdout": _stdout,
        })
