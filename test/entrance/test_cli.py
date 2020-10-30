import pytest
import os
from click.testing import CliRunner
from dcmodule.entrance.cli import cli
from dcmodule.configs.version import version

_TITLE_ = "Dcmodule"
_INPUT_CONTENT_ = "1 2 3"
_OUTPUT_CONTENT_ = "4 5 6"
file = os.path.dirname(__file__)

inputFile = os.path.abspath(file)+"/input.txt"
outputFile = os.path.abspath(file)+"/output.txt"
testfile = os.path.abspath(file)+"/testfile.py"



@pytest.mark.unittest
class TestCli:
    def test_cli_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert version in result.stdout
        assert _TITLE_ in result.stdout
        assert not result.stderr_bytes

    def test_cli_stdin_and_stdout(self):
        runner = CliRunner()
        print(inputFile)
        print(outputFile)
        result = runner.invoke(cli, ["--stdin="+inputFile, "--stdout="+outputFile])
        assert result.exit_code == 0
        assert _INPUT_CONTENT_ in result.stdout
        assert _OUTPUT_CONTENT_ in result.stdout
        assert "stdin" in result.stdout
        assert "stdout" in result.stdout

    def test_cli_testfile(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--testfile="+testfile])
        assert result.exit_code == 0
        assert "True" in result.stdout
        assert "Success!" in result.stdout
        assert "This is stdin" in result.stdout
