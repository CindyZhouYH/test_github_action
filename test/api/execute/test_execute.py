import pytest
from dcmodule.api.execute.execute import execute_dcmodule,_execute


@pytest.mark.unittest
class TestException:

    def test_execute(self):
        _execute()