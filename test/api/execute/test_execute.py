import os

import pytest

from dcmodule.api.execute.exception import InvalidOutputFormatException
from dcmodule.api.execute.execute import execute_dcmodule

file = os.path.dirname(__file__)


@pytest.mark.unittest
class TestException:

    def test_execute_dcmodule_1(self):
        with open(os.path.abspath(file) + "/test_main.py", "w+") as fp:
            fp.write("""from dcmodule import load_with_args, result_dump\nif __name__ == \"__main__\":
                     \n\twith load_with_args() as _iotuple:\n
                     \t\t_stdin, _stdout = _iotuple\n
                     \t\tresult_dump(True, data={\n
                     \t\t\t\"stdin\": _stdin,\n
                     \t\t\t\"stdout\": _stdout,\n
                     \t\t})\n""")
            fp.close()
            fp = open(os.path.abspath(file) + "/input.txt", "w+")
            fp.write("1 2 3")
            fp.close()
            fp = open(os.path.abspath(file) + "/output.txt", "w+")
            fp.write("4 5 6")
            fp.close()
            _success, _message, _data = execute_dcmodule(
                os.path.abspath(file) + "/test_main.py",
                stdin=os.path.abspath(file) + "/input.txt",
                stdout=os.path.abspath(file) + "/output.txt",
            )
            assert _success is True
            assert _message is not None
            assert _data is not None
            os.remove(os.path.abspath(file) + "/input.txt")
            os.remove(os.path.abspath(file) + "/output.txt")
            os.remove(os.path.abspath(file) + "/test_main.py")

    def test_execute_dcmodule_2(self):
        with open(os.path.abspath(file) + "/test_main.py", "w+") as fp:
            fp.write("from dcmodule import load_with_args, result_dump\nif __name__ == \"__main__\":" +
                     "\n\twith load_with_args() as _iotuple:\n" +
                     "\t\t_stdin, _stdout = _iotuple\n" +
                     "\t\tresult_dump(True, data={\n" +
                     "\t\t\t\"stdin\": _stdin,\n" +
                     "\t\t\t\"stdout\": _stdout,\n" +
                     "\t\t})\n")
            fp.close()
            fp = open(os.path.abspath(file) + "/input.txt", "w+")
            fp.write("1 2 3")
            fp.close()
            fp = open(os.path.abspath(file) + "/output.txt", "w+")
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
            os.remove(os.path.abspath(file) + "/input.txt")
            os.remove(os.path.abspath(file) + "/output.txt")
            os.remove(os.path.abspath(file) + "/test_main.py")

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
