import os
from dcmodule.api.execute.exception import InvalidReturnCodeException, InvalidOutputFormatException
import pytest
from dcmodule.api.execute.execute import execute_dcmodule, _execute

file = os.path.dirname(__file__)


@pytest.mark.unittest
class TestException:

    def test_execute_dcmodule_1(self):
        fp = open("test_main.py", "w+")
        fp.write("from dcmodule import load_with_args, result_dump\nif __name__ == \"__main__\":" +
                 "\n\twith load_with_args() as _iotuple:\n" +
                 "\t\t_stdin, _stdout = _iotuple\n" +
                 "\t\tresult_dump(True, data={\n" +
                 "\t\t\t\"stdin\": _stdin,\n" +
                 "\t\t\t\"stdout\": _stdout,\n" +
                 "\t\t})\n")
        fp.close()
        fp = open("input.txt", "w+")
        fp.write("1 2 3")
        fp.close()
        fp = open("output.txt", "w+")
        fp.write("4 5 6")
        fp.close()
        _success, _message, _data = execute_dcmodule(
            os.path.abspath(file) + "/test_main.py",
            stdin="input.txt",
            stdout="output.txt",
        )
        assert _success is True
        assert _message is not None
        assert _data is not None
        os.remove("input.txt")
        os.remove("output.txt")
        os.remove("test_main.py")

    def test_execute_dcmodule_2(self):
        fp = open("test_main.py", "w+")
        fp.write("from dcmodule import load_with_args, result_dump\nif __name__ == \"__main__\":" +
                 "\n\twith load_with_args() as _iotuple:\n" +
                 "\t\t_stdin, _stdout = _iotuple\n" +
                 "\t\tresult_dump(True, data={\n" +
                 "\t\t\t\"stdin\": _stdin,\n" +
                 "\t\t\t\"stdout\": _stdout,\n" +
                 "\t\t})\n")
        fp.close()
        fp = open("input.txt", "w+")
        fp.write("1 2 3")
        fp.close()
        fp = open("output.txt", "w+")
        fp.write("4 5 6")
        fp.close()
        _success, _message, _data = execute_dcmodule(
            os.path.abspath(file) + "/test_main.py",
            stdin=None,
            stdout="",
        )
        assert _success is True
        assert _message is not None
        assert _data is not None
        os.remove("input.txt")
        os.remove("output.txt")
        os.remove("test_main.py")

    def test_execute_dcmodule_3(self):
        try:
            _success, _message, _data = execute_dcmodule(
                "not_exist.py",
                stdin="",
                stdout="",
            )
        except (Exception,) as e1:
            assert isinstance(e1, InvalidOutputFormatException)
            assert e1.stdout is not None
        else:
            assert False, "Should not reach here."
