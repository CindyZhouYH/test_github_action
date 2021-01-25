import pytest

from dcmodule import ExecuteDataCheckException, InvalidOutputFormatException, \
    InvalidReturnCodeException


@pytest.mark.unittest
class TestException:

    def test_execute_data_check_exception(self):
        err1 = ExecuteDataCheckException("exception message")
        assert isinstance(err1, Exception)
        assert err1.message == "exception message"

        with pytest.raises(ExecuteDataCheckException) as ei:
            raise ExecuteDataCheckException("exception message again")
        err2 = ei.value
        assert isinstance(err2, Exception)
        assert err2.message == "exception message again"

    def test_invalid_return_code_exception(self):
        err1 = InvalidReturnCodeException(1, "this is output", "this is err output")
        assert isinstance(err1, Exception)
        assert err1.return_code == 1
        assert err1.stdout == "this is output"
        assert err1.stderr == "this is err output"

        with pytest.raises(InvalidReturnCodeException) as ei:
            raise InvalidReturnCodeException(2, "this is output2", "this is err output2")
        err2 = ei.value
        assert isinstance(err2, Exception)
        assert err2.return_code == 2
        assert err2.stdout == "this is output2"
        assert err2.stderr == "this is err output2"

    def test_invalid_output_format_exception(self):
        err1 = InvalidOutputFormatException("this is output")
        assert isinstance(err1, Exception)
        assert err1.stdout == "this is output"

        with pytest.raises(InvalidOutputFormatException) as ei:
            raise InvalidOutputFormatException("this is output2")
        err2 = ei.value
        assert isinstance(err2, Exception)
        assert err2.stdout == "this is output2"
