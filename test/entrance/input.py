import codecs
import getopt
import sys
import click
from click.core import Option, Context
from contextlib import contextmanager

"""
@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument('--stdin', nargs=-1, type=click.File('rb'))
@click.argument('--stdout', nargs=-1, type=click.File('rb'))
def parse_from_args(stdin, stdout):
    print(stdin.read())
    print(stdout.read())
    return stdin.read(), stdout.read()


"""
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
    _stdin, _stdout = parse_from_args()
    yield _stdin, _stdout
