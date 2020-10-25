import pytest
from dcmodule.configs.version import version


@pytest.mark.unittest
class TestConfigVersion:
    def test_title(self):
        assert version == "0.2.2"
