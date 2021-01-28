import pytest

from dcmodule.configs.meta import __TITLE__, __VERSION__


@pytest.mark.unittest
class TestConfigVersion:
    def test_title(self):
        assert __VERSION__ == "0.2.3"
        assert __TITLE__ == "dcmodule"
