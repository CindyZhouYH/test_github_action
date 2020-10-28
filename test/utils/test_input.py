import os

import pytest
from dcmodule.utils.input import parse_from_args, load_with_args


@pytest.mark.unittest
class TestInputParse:
    def test_parse_from_args_has(self):
        file = os.path.dirname(__file__)
        """
        inputList1 = ["/testfile/test_main.py",
                      "--stdin=./testfile/input.txt",
                      "--stdout=./testfile/output.txt"]
                      """
        inputList1 = [os.path.abspath(file)+"/test_main.py",
                      "--stdin="+os.path.abspath(file)+"/input.txt",
                      "--stdout="+os.path.abspath(file)+"/output.txt"]
        (out1, out2) = parse_from_args(inputList1)
        assert out1 is not None
        assert out2 is not None

    def test_parse_from_args_null(self):
        inputList2 = [""]
        (out1, out2) = parse_from_args(inputList2)
        assert out1 is None
        assert out2 is None
