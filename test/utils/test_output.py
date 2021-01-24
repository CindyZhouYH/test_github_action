from dcmodule.utils.output import result_dump, result_generate

import pytest


@pytest.mark.unittest
class TestOutput:
    def test_result_generate(self):
        _json = result_generate(True, "this is message", "this is data")
        assert len(_json) == 3

    def test_result_dump(self):
        result = result_dump(True, "this is message", "this is data", None)
