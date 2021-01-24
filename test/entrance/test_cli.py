import pytest
import os
from click.testing import CliRunner
from dcmodule.entrance.cli import cli
from dcmodule.configs.meta import __VERSION__
from dcmodule.configs.meta import __TITLE__

_INPUT_CONTENT_ = "1 2 3"
_OUTPUT_CONTENT_ = "4 5 6"
file = os.path.dirname(__file__)

inputFile = os.path.abspath(file) + "/input.txt"
outputFile = os.path.abspath(file) + "/output.txt"
testfile = os.path.abspath(file) + "/test_main.py"


@pytest.mark.unittest
class TestCli:
    def test_cli_version(self):
        runner = CliRunner()
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert __VERSION__ in result.stdout
        assert __TITLE__.capitalize()  in result.stdout
        assert not result.stderr_bytes

    def test_cli_stdin_and_stdout(self):
        fp = open(os.path.abspath(file) + "/input.txt", "w+")
        fp.write("1 2 3")
        fp.close()
        fp = open(os.path.abspath(file) + "/output.txt", "w+")
        fp.write("4 5 6")
        fp.close()
        runner = CliRunner()
        print(inputFile)
        print(outputFile)
        result = runner.invoke(cli, ["--stdin=" + inputFile, "--stdout=" + outputFile])
        assert result.exit_code == 0
        assert _INPUT_CONTENT_ in result.stdout
        assert _OUTPUT_CONTENT_ in result.stdout
        assert "stdin" in result.stdout
        assert "stdout" in result.stdout

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
        result = runner.invoke(cli, ["--testfile=" + testfile])
        assert result.exit_code == 0
        assert "True" in result.stdout
        assert "Success!" in result.stdout
        assert "This is stdin" in result.stdout
        os.remove(os.path.abspath(file) + "/input.txt")
        os.remove(os.path.abspath(file) + "/output.txt")
        os.remove(os.path.abspath(file) + "/test_main.py")