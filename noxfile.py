"""Test process to run in isolated environments."""

import nox


@nox.session(reuse_venv=True)
def lint(session):
    """Apply the pre-commit linting operation."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--a", *session.posargs)


@nox.session(reuse_venv=True)
def test(session):
    """Apply the tests on the lib."""
    session.install(".[test]")
    test_files = session.posargs or ["tests"]
    session.run("pytest", "--color=yes", "--cov", "--cov-report=xml", *test_files)


@nox.session(reuse_venv=True)
def docs(session):
    """Build the documentation."""
    build = session.posargs.pop() if session.posargs else "html"
    session.install(".[doc]")
    dst, warn = f"docs/_build/{build}", "warnings.txt"
    session.run("sphinx-build", "-v", "-b", build, "docs", dst, "-w", warn)
    session.run("python", "tests/check_warnings.py")


@nox.session(reuse_venv=True)
def mypy(session):
    """Run the mypy evaluation of the lib."""
    session.install("mypy")
    test_files = session.posargs or ["pygadm"]
    session.run("mypy", *test_files)
