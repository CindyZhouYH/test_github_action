import json
import os
import subprocess
from tempfile import NamedTemporaryFile

#from pysystem import SystemGroup, SystemUser, chown

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
        """
        if group is not None:
            SystemGroup.loads(group).apply()
        if user is not None:
            SystemUser.loads(user).apply(include_group=not group)

        """
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
        raise InvalidReturnCodeException(
            return_code=_return_code,
            stdout=_stdout.decode(encoding or DEFAULT_ENCODING),
            stderr=_stderr.decode(encoding or DEFAULT_ENCODING),
        )


DEFAULT_PREFIX = ["python3"]
DEFAULT_SUFFIX = []


def execute_dcmodule(script: str, stdin: str, stdout: str or None,
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
        with NamedTemporaryFile(delete=False) as _file:
            _file.write((str(stdin)).encode())
            _stdin_filename = os.path.abspath(_file.name)
            if user or group:
                _user = str(user) if user else None
                _group = str(group) if group else None
                #chown(_stdin_filename, _user, _group)
        args += ["--stdin_file", _stdin_filename]
    else:
        _stdin_filename = None

    if stdout is not None:
        with NamedTemporaryFile(delete=False) as _file:
            _file.write((str(stdout)).encode())
            _stdout_filename = os.path.abspath(_file.name)
            if user or group:
                _user = str(user) if user else None
                _group = str(group) if group else None
                #chown(_stdout_filename, _user, _group)
        args += ["--stdout_file", _stdout_filename]
    else:
        _stdout_filename = None

    _stdout = _execute(
        args=args,
        encoding=encoding,
        workdir=workdir,
        user=user,
        group=group
    )

    if _stdin_filename and os.path.exists(_stdin_filename):  # 清除输入临时文件
        #chown(_stdin_filename, SystemUser.current().name, SystemGroup.current().name)
        os.remove(_stdin_filename)
    if _stdout_filename and os.path.exists(_stdout_filename):  # 清除输出临时文件
        #chown(_stdout_filename, SystemUser.current().name, SystemGroup.current().name)
        os.remove(_stdout_filename)

    try:
        _json = json.loads(_stdout)
    except Exception:
        raise InvalidOutputFormatException(_stdout)
    _success = _json.get("success", False)
    _message = _json.get("message", None)
    _data = _json.get("data", None)

    return _success, _message, _data
