import nox

MAIN_PACKAGE = "universal_build"


@nox.session(python=["3.8", "3.7", "3.6"])
def test(session):
    session.run(
        "pip",
        "install",
        "-e" ".[dev]",
    )
    # Execute tests with coverage check
    session.run(
        "python",
        "-m",
        "pytest",
        "-s",
        f"--cov={MAIN_PACKAGE}",
        "--cov-report=xml",
        "--cov-report",
        "term",
        "--cov-report=html",
        "tests",
    )
