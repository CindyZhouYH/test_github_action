import os

import pytest

from dcmodule import parse_from_args

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
class TestInputParse:
    def test_parse_from_args_has(self):
        with open(testfile_dir, "w+") as fp:
            fp.write(testfile_content)
            fp.close()
        with open(input_dir, "w+") as fp:
            fp.write("1 2 3")
            fp.close()
        with open(output_dir, "w+") as fp:
            fp.write("4 5 6")
            fp.close()
        inputList1 = [testfile_dir,
                      "--stdin=" + input_dir,
                      "--stdout=" + output_dir]
        (out1, out2) = parse_from_args(inputList1)
        assert out1 is not None
        assert out2 is not None
        os.remove(testfile_dir)
        os.remove(input_dir)
        os.remove(output_dir)

    def test_parse_from_args_null(self):
        inputList2 = [""]
        (out1, out2) = parse_from_args(inputList2)
        assert out1 is None
        assert out2 is None
