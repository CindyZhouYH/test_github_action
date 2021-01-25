import os

import pytest

from dcmodule import InvalidOutputFormatException
from dcmodule import execute_dcmodule

file = os.path.dirname(__file__)
here = os.path.abspath(os.path.dirname(__file__))
testfile_dir = os.path.join(here, 'test_main.py')
input_dir = os.path.join(here, 'input.txt')
output_dir = os.path.join(here, 'output.txt')
testfile_content = """
from dcmodule import load_with_args, result_dump
if __name__ == "__main__":
    with load_with_args() as _iotuple:
        _stdin, _stdout = _iotuple
        result_dump(True, data={
            "stdin": _stdin,
            "stdout": _stdout,
        })
"""


@pytest.mark.unittest
class TestException:

    def test_execute_dcmodule_1(self):
        with open(testfile_dir, "w+") as fp:
            fp.write(testfile_content)
            fp.close()
        with open(input_dir, "w+") as fp:
            fp.write("1 2 3")
            fp.close()
        with open(output_dir, "w+") as fp:
            fp.write("4 5 6")
            fp.close()
        _success, _message, _data = execute_dcmodule(
            testfile_dir,
            stdin=input_dir,
            stdout=output_dir,
        )
        assert _success is True
        assert _message is not None
        assert _data is not None
        os.remove(testfile_dir)
        os.remove(input_dir)
        os.remove(output_dir)

    def test_execute_dcmodule_2(self):
        with open(testfile_dir, "w+") as fp:
            fp.write(testfile_content)
            fp.close()
        with open(input_dir, "w+") as fp:
            fp.write("1 2 3")
            fp.close()
        with open(output_dir, "w+") as fp:
            fp.write("4 5 6")
            fp.close()
        _success, _message, _data = execute_dcmodule(
            testfile_dir,
            stdin=None,
            stdout="",
        )
        assert _success is True
        assert _message is not None
        assert _data is not None
        os.remove(testfile_dir)
        os.remove(input_dir)
        os.remove(output_dir)

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
