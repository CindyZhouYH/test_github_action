import os

import pytest
from click.testing import CliRunner

from dcmodule.configs.meta import __TITLE__
from dcmodule.configs.meta import __VERSION__
from dcmodule.entrance.cli import cli

_INPUT_CONTENT_ = "1 2 3"
_OUTPUT_CONTENT_ = "4 5 6"
file = os.path.dirname(__file__)

testfile = os.path.abspath(file) + "/test_main.py"


@pytest.mark.unittest
class TestCli:
    def test_cli_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert __VERSION__ in result.stdout
        assert __TITLE__.capitalize() in result.stdout
        assert not result.stderr_bytes

    def test_cli_stdin_and_stdout(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--stdin=" + _INPUT_CONTENT_, "--stdout=" + _OUTPUT_CONTENT_])
        assert result.exit_code == 0
        assert _INPUT_CONTENT_ in result.stdout
        assert _OUTPUT_CONTENT_ in result.stdout

    def test_cli_testfile(self):
        fp = open(os.path.abspath(file) + "/test_main.py", "w+")
        fp.write("from dcmodule import load_with_args, result_dump\nif __name__ == \"__main__\":" +
                 "\n\twith load_with_args() as _iotuple:\n" +
                 "\t\t_stdin, _stdout = _iotuple\n" +
                 "\t\tresult_dump(True, data={\n" +
                 "\t\t\t\"stdin\": _stdin,\n" +
                 "\t\t\t\"stdout\": _stdout,\n" +
                 "\t\t})\n")
        fp.close()
        runner = CliRunner()
        result = runner.invoke(cli,
                               ["--testfile=" + testfile, "--stdin=" + _INPUT_CONTENT_, "--stdout=" + _OUTPUT_CONTENT_])
        assert result.exit_code == 0
        assert "True" in result.stdout
        assert "Success!" in result.stdout
        assert _INPUT_CONTENT_ in result.stdout
        os.remove(os.path.abspath(file) + "/test_main.py")
