# noxfile.py
import nox

# 我們用 Hatch 當單一環境來源，所以不要求系統一定要有多版本直譯器
nox.options.error_on_missing_interpreters = False


@nox.session(name="fmt", venv_backend="none")
def fmt(session: nox.Session) -> None:
    """
    Auto-format code using the *current* Hatch env.
    - Black: format
    - Ruff:  auto-fix (含 import 排序 I 規則，若你改用 isort，這裡請調整)
    """
    session.run("ruff", "check", "--fix", ".")
    session.run("black", ".")


@nox.session(name="style", venv_backend="none")
def style(session: nox.Session) -> None:
    """
    Style-only checks (no mutation) using current Hatch env.
    - Black: --check
    - Ruff:  check (不自動修)
    """
    session.run("black", "--check", ".")
    session.run("ruff", "check", ".")


@nox.session(name="lint", venv_backend="none")
def lint(session: nox.Session) -> None:
    """
    Full static checks (style + type) using current Hatch env.
    - Black: --check
    - Ruff:  check
    - mypy:  type checks (可依專案調整路徑)
    """
    session.run("black", "--check", ".")
    session.run("ruff", "check", ".")
    session.run("mypy", "src/")


@nox.session(name="typecheck", venv_backend="none")
def typecheck(session: nox.Session) -> None:
    """Run static type checks (basedpyright + mypy) using current Hatch env."""
    session.run("pyright", ".")
    session.run("mypy", "src/")


@nox.session(name="contracts", venv_backend="none")
def contracts(session: nox.Session) -> None:
    """Run contract tests (Pydantic models)."""
    session.run("pytest", "-q", "tests/contracts")


@nox.session(name="tests-3.11", venv_backend="none")
def tests_311(session: nox.Session) -> None:
    """
    Run tests (labelled 3.11) using the CURRENT env.
    建議在 CI job 裡用 setup-python matrix 指定 3.11 再呼叫此 session。
    """
    session.run("pytest", "-q")


@nox.session(name="tests-3.12", venv_backend="none")
def tests_312(session: nox.Session) -> None:
    """
    Run tests (labelled 3.12) using the CURRENT env.
    建議在 CI job 裡用 setup-python matrix 指定 3.12 再呼叫此 session。
    """
    session.run("pytest", "-q")
