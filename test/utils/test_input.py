import os

import pytest
from dcmodule.utils.input import parse_from_args, load_with_args

file = os.path.dirname(__file__)
@pytest.mark.unittest
class TestInputParse:
    def test_parse_from_args_has(self):
        fp = open(os.path.abspath(file) + "/test_main.py", "w+")
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
        inputList1 = [os.path.abspath(file)+"/test_main.py",
                      "--stdin="+os.path.abspath(file)+"/input.txt",
                      "--stdout="+os.path.abspath(file)+"/output.txt"]
        (out1, out2) = parse_from_args(inputList1)
        assert out1 is not None
        assert out2 is not None
        os.remove(os.path.abspath(file) + "/input.txt")
        os.remove(os.path.abspath(file) + "/output.txt")
        os.remove(os.path.abspath(file) + "/test_main.py")

    def test_parse_from_args_null(self):
        inputList2 = [""]
        (out1, out2) = parse_from_args(inputList2)
        assert out1 is None
        assert out2 is None
