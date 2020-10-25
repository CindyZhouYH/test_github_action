import codecs
import getopt
import sys
from contextlib import contextmanager


def parse_from_args(args=None):
    """
    从命令行参数中解析输入输出值
    :param args: 命令行参数列表（缺省为自动获取）
    :return: stdin, stdout
    """
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
    _stdin, _stdout = parse_from_args(args)
    yield _stdin, _stdout
