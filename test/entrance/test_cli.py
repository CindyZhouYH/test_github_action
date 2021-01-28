import os

import pytest
from click.testing import CliRunner

from dcmodule.configs.meta import __TITLE__, __VERSION__
from dcmodule.entrance.cli import cli

_INPUT_CONTENT_ = "1 2 3"
_OUTPUT_CONTENT_ = "4 5 6"
_INPUT_FILE_ = "input.txt"
_OUTPUT_FILE_ = "output.txt"

here = os.path.abspath(os.path.dirname(__file__))
testfile = os.path.join(here, 'test_main.py')
inputfile = os.path.join(here, _INPUT_FILE_)
outputfile = os.path.join(here, _OUTPUT_FILE_)
testfile_content = """
from dcmodule import load_with_args, result_dump
if __name__ == "__main__":
    with load_with_args() as _iotuple:
        _stdin, _stdout = _iotuple
        result_dump(True, data={
            "stdin": _stdin,
            "stdout": _stdout,
        })
"""


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
        result = runner.invoke(cli, ["--input=" + _INPUT_CONTENT_, "--output=" + _OUTPUT_CONTENT_])
        assert result.exit_code == 0
        assert _INPUT_CONTENT_ in result.stdout
        assert _OUTPUT_CONTENT_ in result.stdout

    def test_cli_testfile(self):
        with open(testfile, "w+") as fp:
            fp.write(testfile_content)
            fp.close()
        with open(inputfile, "w+") as fp:
            fp.write(_INPUT_CONTENT_)
            fp.close()
        with open(outputfile, "w+") as fp:
            fp.write(_OUTPUT_CONTENT_)
            fp.close()
        runner = CliRunner()
        result = runner.invoke(cli,
                               ["--testfile=" + testfile, "--input_file=" + inputfile,
                                "--output_file=" + outputfile])
        assert result.exit_code == 0
        assert "True" in result.stdout
        assert "Success!" in result.stdout
        assert _INPUT_CONTENT_ in result.stdout
        os.remove(testfile)
        os.remove(inputfile)
        os.remove(outputfile)
