from pathlib import Path
import subprocess
import sys
from typing import NamedTuple, Protocol

import pytest


class CliResult(NamedTuple):
    code: int
    out: str
    err: str


class RunCli(Protocol):
    def __call__(self, args: list[str] | None = ...) -> CliResult: ...


@pytest.fixture
def run_cli(tmp_path: Path) -> RunCli:

    def _run(args: list[str] | None = None) -> CliResult:
        cmd = [sys.executable, "-m", "demo_app.main"]
        if args:
            cmd.extend(args)
        proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(tmp_path))
        return CliResult(proc.returncode, proc.stdout, proc.stderr)

    return _run
