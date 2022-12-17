import nox


@nox.session(reuse_venv=True)
def lint(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "--a", *session.posargs)


@nox.session(python=["3.7", "3.8", "3.9"])
def test(session):
    session.install(".[test]")
    session.run("pytest", "--color=yes", "tests")


@nox.session(reuse_venv=True)
def docs(session):
    session.install(".[doc]")
    session.run(
        "sphinx-apidoc",
        "--force",
        "--module-first",
        "-o",
        "docs/source/_api",
        "./pygadm",
    )
    session.run("sphinx-build", "-b", "html", "docs/source", "build")


@nox.session(name="docs-live", reuse_venv=False)
def docs_live(session):
    session.install(".[doc]")
    session.run(
        "sphinx-apidoc",
        "--force",
        "--module-first",
        "-o",
        "docs/source/_api",
        "./pygadm",
    )
    session.run("sphinx-autobuild", "-b", "html", "docs/source", "build")
