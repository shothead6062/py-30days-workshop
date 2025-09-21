import nox

nox.options.error_on_missing_interpreters = False


@nox.session(name="tests-3.11", venv_backend="none")
def tests_311(session: nox.Session) -> None:
    """Run tests (labelled 3.11) using current env."""
    session.run("pytest", "-q")


@nox.session(name="tests-3.12", venv_backend="none")
def tests_312(session: nox.Session) -> None:
    """Run tests (labelled 3.12) using current env."""
    session.run("pytest", "-q")


@nox.session(venv_backend="none")
def lint(session: nox.Session) -> None:
    """Run lint/type checks using the current Hatch env."""
    session.run("ruff", "check", ".")
    session.run("ruff", "format", "--check", ".")
    session.run("mypy", "src/")
