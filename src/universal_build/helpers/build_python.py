import argparse
import re
import sys
from shutil import rmtree
from typing import Dict, List, Optional, Union

from universal_build import build_utils

FLAG_PYPI_TOKEN = "pypi_token"
FLAG_PYPI_REPOSITORY = "pypi_repository"


def get_sanitized_arguments(
    arguments: List[str] = None, argument_parser: argparse.ArgumentParser = None
) -> Dict[str, Union[str, bool, List[str]]]:
    """Return sanitized default arguments when they are valid.

    Sanitized means that, for example, the version is already checked and set depending on our build guidelines.
    If arguments are not valid, exit the script run.

    Args:
        arguments (List[str], optional): List of arguments that are used instead of the arguments passed to the process. Defaults to `None`.
        argument_parser (arparse.ArgumentParser, optional): An argument parser which is passed as a parents parser to the default ArgumentParser to be able to use additional flags besides the default ones. Must be initialized with `add_help=False` flag like argparse.ArgumentParser(add_help=False)!

    Returns:
        Dict[str, Union[str, bool, List[str]]]: The parsed default arguments thar are already checked for validity.
    """
    if argument_parser is None:
        argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        "--" + FLAG_PYPI_TOKEN.replace("_", "-"),
        help="Personal access token for PyPI account.",
        required=False,
        default=None,
    )
    argument_parser.add_argument(
        "--" + FLAG_PYPI_REPOSITORY.replace("_", "-"),
        help="PyPI repository for publishing artifacts.",
        required=False,
        default=None,
    )

    return build_utils.get_sanitized_arguments(
        arguments=arguments, argument_parser=argument_parser
    )


def test_with_py_version(python_version: str, exit_on_error: bool = True) -> None:
    """Run pytest in a environment wiht the specified python version.

    Args:
        python_version (str): Python version to use inside the virutal environment.
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """
    # Install pipenv environment with specific versio
    build_utils.run(
        f"pyenv install --skip-existing {python_version} && pyenv local {python_version}",
        exit_on_error=exit_on_error,
    )
    # Install pipenv environment with specific version
    build_utils.run(
        f"pipenv install --dev --python={python_version} --skip-lock",
        exit_on_error=exit_on_error,
    )
    # Run pytest in pipenv environment
    build_utils.run("pipenv run pytest", exit_on_error=exit_on_error)
    # Remove enviornment
    build_utils.run("pipenv --rm")
    # Uninstall pyenv version
    build_utils.run(f"pyenv local --unset && pyenv uninstall -f {python_version}")


def install_build_env() -> None:
    """Installs a new virtual environment via pipenv."""
    build_utils.run("pipenv --rm")
    build_utils.run(
        f"pipenv install --dev --python={sys.executable} --skip-lock",
        exit_on_error=True,
    )

    # Show current environment
    build_utils.run("pipenv graph", exit_on_error=False)


def generate_api_docs(
    github_url: str,
    main_package: str,
    command_prefix: str = "pipenv run",
    exit_on_error: bool = True,
) -> None:
    """Generates API documentation via lazydocs.

    Args:
        github_url (str): Github URL
        main_package (str): The main package name to use for docs generation.
        command_prefix (str, optional): Prefix to use for all commands. Defaults to `pipenv run`.
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """
    build_utils.run(
        f"{command_prefix} lazydocs --overview-file=README.md"
        f" --src-base-url={github_url}/blob/main {main_package}",
        exit_on_error=exit_on_error,
    )


def publish_pypi_distribution(
    pypi_token: str, pypi_user: str = "__token__", pypi_repository: Optional[str] = None
) -> None:
    """Publish distribution to pypi.

    Args:
        pypi_token (str): Token of PyPi repository.
        pypi_user (str, optional): User of PyPi repository. Defaults to "__token__".
        pypi_repository (Optional[str], optional): PyPi repository. If `None` provided, use the production instance.
    """
    if not pypi_token:
        build_utils.log("PyPI token is required for release (--pypi-token=<TOKEN>)")
        build_utils.exit_process(1)

    pypi_repository_args = ""
    if pypi_repository:
        pypi_repository_args = f'--repository-url "{pypi_repository}"'

    # Publish on pypi
    build_utils.run(
        f'twine upload --non-interactive -u "{pypi_user}" -p "{pypi_token}" {pypi_repository_args} dist/*',
        exit_on_error=True,
    )


def code_checks(
    command_prefix: str = "pipenv run",
    black: bool = True,
    isort: bool = True,
    pydocstyle: bool = True,
    mypy: bool = True,
    flake8: bool = True,
    safety: bool = True,
    exit_on_error: bool = True,
) -> None:
    """Run linting and style checks.

    Args:
        command_prefix (str, optional): Prefix to use for all check commands. Defaults to `pipenv run`.
        black (bool, optional): Activate black formatting check. Defaults to True.
        isort (bool, optional): Activate isort import sorting check. Defaults to True.
        pydocstyle (bool, optional): Activate pydocstyle docstring check. Defaults to True.
        mypy (bool, optional): Activate mypy typing check. Defaults to True.
        flake8 (bool, optional): Activate flake8 linting check. Defaults to True.
        safety (bool, optional): Activate saftey check via pipenv. Defaults to True.
        exit_on_error (bool, optional): If `True`, exit process as soon as error occures. Defaults to True.
    """
    if black:
        build_utils.run(
            f"{command_prefix} black --check src", exit_on_error=exit_on_error
        )
        build_utils.run(
            f"{command_prefix} black --check tests", exit_on_error=exit_on_error
        )

    if isort:
        build_utils.run(
            f"{command_prefix} isort --profile black --check-only src",
            exit_on_error=exit_on_error,
        )
        build_utils.run(
            f"{command_prefix} isort --profile black --check-only tests",
            exit_on_error=exit_on_error,
        )

    if pydocstyle:
        build_utils.run(f"{command_prefix} pydocstyle src", exit_on_error=exit_on_error)

        # Run linters and checks
    if mypy:
        build_utils.run(f"{command_prefix} mypy src", exit_on_error=exit_on_error)

    if flake8:
        build_utils.run(
            f"{command_prefix} flake8 --show-source --statistics src",
            exit_on_error=exit_on_error,
        )
        build_utils.run(
            f"{command_prefix} flake8 --show-source --statistics tests",
            exit_on_error=exit_on_error,
        )

    if safety:
        # Check using pipenv (runs safety check)
        build_utils.run("pipenv check", exit_on_error=exit_on_error)


def update_version(module_path: str, version: str) -> None:
    """Update version in specified module.

    Args:
        module_path (str): Python module with a `__version__` attribute.
        version (str): New version number to write into `__version__` attribute.
    """
    if not version:
        build_utils.log("Cannot update version, no version provided")
        return

    with open(module_path, "r+") as f:
        data = f.read()
        f.seek(0)
        f.write(re.sub(r"__version__ = \".+\"", f'__version__ = "{version}"', data))
        f.truncate()


def build_distribution() -> None:
    """Build python package distribution."""

    try:
        # Ensure there are no old builds
        rmtree("./dist")
    except OSError:
        pass

    try:
        # Ensure there are no old builds
        rmtree("./build")
    except OSError:
        pass

    # Build the distribution archives
    build_utils.run(
        "python setup.py sdist bdist_wheel clean --all",
        exit_on_error=True,
    )

    # Check the archives with twine
    build_utils.run("twine check dist/*", exit_on_error=True)
