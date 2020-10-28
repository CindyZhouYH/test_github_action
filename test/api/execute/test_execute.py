import os
from dcmodule.api.execute.exception import InvalidReturnCodeException,InvalidOutputFormatException
import pytest
from dcmodule.api.execute.execute import execute_dcmodule,_execute


@pytest.mark.unittest
class TestException:

    def test_execute_dcmodule(self):
        file = os.path.dirname(__file__)
        _success, _message, _data = execute_dcmodule(
            "test_main.py",
            stdin="input.txt",
            stdout="output.txt",
        )
        assert _success is True
        assert _message is not None
        assert _data is not None

        _success, _message, _data = execute_dcmodule(
            os.path.abspath(file) + "/test_main.py",
            stdin = None,
            stdout = "",
        )
        assert _success is True
        assert _message is not None
        assert _data is not None

        try:
            _success, _message, _data = execute_dcmodule(
                "not_exist.py",
                stdin = "",
                stdout="",
            )
        except (Exception,) as e1:
            assert isinstance(e1, InvalidOutputFormatException)
            assert e1.stdout is not None
            #assert isinstance(e2, InvalidReturnCodeException)
            #assert e2.return_code == -2
            #assert "InvalidReturnCodeException" in e2.stderr
        else:
            assert False, "Should not reach here."

