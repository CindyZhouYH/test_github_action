import json
import subprocess

from pysystem import SystemGroup, SystemUser

from .exception import InvalidReturnCodeException, InvalidOutputFormatException

DEFAULT_ENCODING = "utf8"


def _execute(args: list, encoding=None, workdir=None, user=None, group=None):
    """
    执行命令
    :param args: 参数列表
    :param encoding: 编码格式（用于解析输出，缺省为utf8）
    :param workdir: 工作路径（缺省为使用当前工作路径）
    :param user: 使用的用户名（缺省为不指定）
    :param group: 使用的用户组（缺省为不指定）
    :return: 输出的文本内容
    """

    def _user_switch():
        """
        切换用户
        """
        if group is not None:
            SystemGroup.loads(group).apply()
        if user is not None:
            SystemUser.loads(user).apply(include_group=not group)

    def _pre_execute_method():
        """
        预执行方法
        """
        _user_switch()

    args = args or []
    _process = subprocess.Popen(
        args=args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=workdir,
        preexec_fn=_pre_execute_method,
    )
    _stdout, _stderr = _process.communicate()
    _return_code = _process.returncode
    if _return_code == 0:
        return _stdout.decode(encoding or DEFAULT_ENCODING)
    else:
        raise InvalidReturnCodeException(_return_code)


DEFAULT_PREFIX = ["python3"]
DEFAULT_SUFFIX = []


def execute_dcmodule(script: str, stdin: str, stdout: str,
                     prefix: list = None, suffix: list = None,
                     encoding=None, workdir=None, user=None, group=None):
    """
    执行dcmodule python脚本
    :param script: 脚本文件名
    :param stdin: 标准输入内容
    :param stdout: 标准输出内容
    :param prefix: 前缀命令行内容（默认为["python3"]）
    :param suffix: 后缀命令行内容（默认为[]）
    :param encoding: 编码格式（用于解析输出的json，默认为utf8）
    :param workdir: 工作路径（缺省为使用当前工作路径）
    :param user: 运行使用的用户名（缺省为不指定）
    :param group: 运行使用的用户组名（缺省为不指定）
    :return: 解析得出的success, message, data
    """
    prefix = [str(_item) for _item in (prefix or DEFAULT_PREFIX)]
    suffix = [str(_item) for _item in (suffix or DEFAULT_SUFFIX)]
    args = prefix + [str(script)] + suffix
    if stdin is not None:
        args += ["--stdin", str(stdin)]
    if stdout is not None:
        args += ["--stdout", str(stdout)]
    _stdout = _execute(
        args=args,
        encoding=encoding,
        workdir=workdir,
        user=user,
        group=group
    )

    try:
        _json = json.loads(_stdout)
    except Exception:
        raise InvalidOutputFormatException(_stdout)
    _success = _json.get("success", False)
    _message = _json.get("message", None)
    _data = _json.get("data", None)

    return _success, _message, _data