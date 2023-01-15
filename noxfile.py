"""Test process to run in isolated environments."""

import nox


@nox.session(reuse_venv=True)
def lint(session):
    """Apply the pre-commit linting operation."""
    session.install("pre-commit")
    session.run("pre-commit", "run", "--a", *session.posargs)


@nox.session(python=["3.7", "3.8", "3.9"], reuse_venv=True)
def test(session):
    """Apply the tests on the lib."""
    session.install(".[test]")
    session.run("pytest", "--color=yes", "--cov", "--cov-report=html", "tests")


@nox.session(reuse_venv=True)
def docs(session):
    """Build the documentation."""
    session.install(".[doc]")
    session.run(
        "sphinx-apidoc",
        "--force",
        "--module-first",
        "-o",
        "docs/source/_api",
        "./pygadm",
    )
    session.run("sphinx-build", "-b", "html", "docs/source", "docs/build/html")


@nox.session(name="mypy", reuse_venv=True)
def mypy(session):
    """Run the mypy evaluation of the lib."""
    session.install(".[dev]")
    test_files = session.posargs or ["pygadm"]
    session.run(
        "mypy",
        "--ignore-missing-imports",
        "--install-types",
        "--non-interactive",
        *test_files,
    )
