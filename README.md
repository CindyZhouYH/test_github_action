# dcmodule

针对数据有效性检查的封装库。

用于进行互测时输入数据合法性的检查。

## 安装

### 准备工作

在正式开始安装之前，首先需要一些准备：

* 完整的python环境（推荐使用`python 3.5+`）
* 【推荐】完整的pip3环境（推荐使用`pip 19.0`或更高版本）
* `pysystem`包，gitlab地址：https://gitlab.buaaoo.top/oo_course_2019/pysystem

### 安装dcmodule

接下来安装dcmodule包

```bash
git clone -b release git@gitlab.buaaoo.top:oo_course_2019/dcmodule.git
cd dcmodule
sudo pip3 install .
```

注意：这步操作需要sudo权限

类似的，卸载dcmodule

```bash
sudo pip3 uninstall -y dcmodule
```

在安装和卸载的过程中，推荐使用pip进行操作，可以省去很多不必要的麻烦。

## 开始使用

### 程序范例

数据测试程序`test_main.py`：

```python
from dcmodule import load_with_args, result_dump

if __name__ == "__main__":
    with load_with_args() as _iotuple:
        _stdin, _stdout = _iotuple
        result_dump(True, data={
            "stdin": _stdin,
            "stdout": _stdout,
        })

```

数据测试程序的调用`test_main2.py`：

```python
from dcmodule import execute_dcmodule

if __name__ == "__main__":
    _success, _message, _data = execute_dcmodule(
        "test_main.py",
        stdin="This is stdin.\r\nThis is next line!",
        stdout="This is \t\t stdout.",
    )
    print(_success)
    print(_message)
    print(_data)

```

### 范例测试

#### 调用测试文件

运行命令

```bash
python3 test_main2.py
```

输出结果

```
True
Success!
{'stdout': 'This is \t\t stdout.', 'stdin': 'This is stdin.\r\nThis is next line!'}
```

该命令可以用于快速调用配置文件。其中stdin、stdout参数均支持任意字符串。

更多关于函数execute_dcmodule的细节，可以查看源代码中的文档。

#### 测试文件使用

运行命令

```bash
python3 test_main.py --stdin="This is stdin." --stdout="This is stdout."
```

输出结果

```
{
    "data": {
        "stdin": "This is stdin.",
        "stdout": "This is stdout."
    },
    "message": "Success!",
    "success": true
}
```

该命令可用来手动测试测试文件。

更多关于load_with_args、result_dump的技术细节，可以查看源代码中的文档。

