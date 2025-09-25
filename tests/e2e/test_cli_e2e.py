import pytest

from tests.conftest import CliResult, RunCli

pytestmark = pytest.mark.e2e


def test_cli_prints_hello_world(run_cli: RunCli) -> None:
    result: CliResult = run_cli()
    assert result.code == 0
    assert "Hello World" in result.out
