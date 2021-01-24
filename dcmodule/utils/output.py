import json
import sys


def result_generate(success, message=None, data=None):
    """
    生成输出json
    :param success: 是否成功
    :param message: 输出信息
    :param data: 数据信息
    :return: 返回json数据
    """
    return {
        "success": success,
        "message": message or ("Success!" if success else "Failed!"),
        "data": data,
    }


def result_dump(success, message=None, data=None, file=None):
    """
    结果输出
    :param success: 是否成功
    :param message: 输出信息
    :param data: 数据信息
    :param file: 输出的目标文件
    """
    file = file or sys.stdout
    print(json.dumps(
        result_generate(
            success=success,
            message=message,
            data=data
        ),
        sort_keys=True,
        indent=4,
    ), file=file)
