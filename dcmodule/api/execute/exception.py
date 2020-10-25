class ExecuteDataCheckException(Exception):
    """
    执行测试异常类
    """

    def __init__(self, message):
        """
        构造函数
        :param message: 错误信息
        """
        Exception.__init__(self, message)
        self.__message = message

    @property
    def message(self):
        """
        获取错误信息
        :return: 错误信息
        """
        return self.__message


class InvalidReturnCodeException(ExecuteDataCheckException):
    """
    非法返回值异常
    """

    def __init__(self, return_code, stdout=None, stderr=None):
        """
        构造函数
        :param return_code: 返回值
        :param stdout: 标准输出内容
        :param stderr: 标准异常内容
        """
        self.__return_code = return_code
        self.__stdout = stdout
        self.__stderr = stderr
        super().__init__("Invalid return code - %s." % self.__return_code)

    @property
    def return_code(self):
        """
        获取返回值
        :return: 返回值
        """
        return self.__return_code

    @property
    def stdout(self):
        """
        获取输出信息
        :return: 输出信息
        """
        return self.__stdout

    @property
    def stderr(self):
        """
        获取异常信息
        :return: 异常信息
        """
        return self.__stderr


class InvalidOutputFormatException(ExecuteDataCheckException):
    """
    输出结果不可解析异常
    """

    def __init__(self, stdout):
        """
        构造函数
        :param stdout: 标准输出结果
        """
        self.__stdout = stdout
        ExecuteDataCheckException.__init__(self, "Invalid output format.")

    @property
    def stdout(self):
        """
        获取标准输出内容
        :return: 标准输出内容
        """
        return self.__stdout
