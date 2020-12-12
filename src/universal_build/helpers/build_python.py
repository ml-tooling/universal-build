"""Utilities to help building Python libraries."""

import argparse
import os
import re
import sys
from shutil import rmtree
from typing import List, Optional

from universal_build import build_utils

FLAG_PYPI_TOKEN = "pypi_token"
FLAG_PYPI_REPOSITORY = "pypi_repository"


def parse_arguments(
    input_args: List[str] = None, argument_parser: argparse.ArgumentParser = None
) -> dict:
    """Parses all arguments and returns a sanitized & augmented list of arguments.

    Sanitized means that, for example, the version is already checked and set depending on our build guidelines.
    If arguments are not valid, exit the script run.

    Args:
        input_args (List[str], optional): List of arguments that are used instead of the arguments passed to the process. Defaults to `None`.
        argument_parser (arparse.ArgumentParser, optional): An argument parser which is passed as a parents parser to the default ArgumentParser to be able to use additional flags besides the default ones.

    Returns:
        dict: The parsed default arguments thar are already checked for validity.
    """
    if argument_parser is None:
        argument_parser = argparse.ArgumentParser()

    argument_parser.add_argument(
        "--" + FLAG_PYPI_TOKEN.replace("_", "-"),
        help="Personal access token for PyPI account.",
        required=False,
        default="",
    )
    argument_parser.add_argument(
        "--" + FLAG_PYPI_REPOSITORY.replace("_", "-"),
        help="PyPI repository for publishing artifacts.",
        required=False,
        default="",
    )

    return build_utils.parse_arguments(
        input_args=input_args, argument_parser=argument_parser
    )


def is_pipenv_environment() -> bool:
    """Check if current working directory is a valid pipenv environment."""

    if not os.path.exists("Pipfile"):
        return False

    if not build_utils.command_exists("pipenv"):
        return False

    return (
        build_utils.run(
            "pipenv --venv",
            disable_stderr_logging=True,
            disable_stdout_logging=True,
            exit_on_error=False,
        ).returncode
        == 0
    )


def test_with_py_version(python_version: str, exit_on_error: bool = True) -> None:
    """Run pytest in a environment wiht the specified python version.

    Args:
        python_version (str): Python version to use inside the virutal environment.
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """
    if not os.path.exists("Pipfile"):
        build_utils.log(
            "No Pipfile discovered. Testing with specific python version only works with pipenv."
        )
        return

    # Check if pyenv command exists
    build_utils.command_exists("pyenv", exit_on_error=exit_on_error)

    # Check if pipenv command exists
    build_utils.command_exists("pipenv", exit_on_error=exit_on_error)

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
    build_utils.run("pipenv --rm", exit_on_error=False)
    # Uninstall pyenv version
    build_utils.run(
        f"pyenv local --unset && pyenv uninstall -f {python_version}",
        exit_on_error=False,
    )


def install_build_env(exit_on_error: bool = True) -> None:
    """Installs a new virtual environment via pipenv.

    Args:
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """
    if not os.path.exists("Pipfile"):
        build_utils.log("No Pipfile discovered, cannot install pipenv environemnt")
        if exit_on_error:
            build_utils.exit_process(1)
        return

    # Check if pipenv command exists
    build_utils.command_exists("pipenv", exit_on_error=exit_on_error)

    build_utils.run("pipenv --rm", exit_on_error=False)
    build_utils.run(
        f"pipenv install --dev --python={sys.executable} --skip-lock",
        exit_on_error=exit_on_error,
    )

    # Show current environment
    build_utils.run("pipenv graph", exit_on_error=False)


def generate_api_docs(
    github_url: str,
    main_package: str,
    exit_on_error: bool = True,
) -> None:
    """Generates API documentation via lazydocs.

    Args:
        github_url (str): Github URL
        main_package (str): The main package name to use for docs generation.
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """

    command_prefix = ""
    if is_pipenv_environment():
        command_prefix = "pipenv run"
    else:
        # Check lazydocs command
        build_utils.command_exists("lazydocs", exit_on_error=exit_on_error)

    build_utils.run(
        f"{command_prefix} lazydocs --overview-file=README.md"
        f" --src-base-url={github_url}/blob/main {main_package}",
        exit_on_error=exit_on_error,
    )


def publish_pypi_distribution(
    pypi_token: str,
    pypi_user: str = "__token__",
    pypi_repository: Optional[str] = None,
    exit_on_error: bool = True,
) -> None:
    """Publish distribution to pypi.

    Args:
        pypi_token (str): Token of PyPi repository.
        pypi_user (str, optional): User of PyPi repository. Defaults to "__token__".
        pypi_repository (Optional[str], optional): PyPi repository. If `None` provided, use the production instance.
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """
    if not pypi_token:
        build_utils.log("PyPI token is required for release (--pypi-token=<TOKEN>)")
        if exit_on_error:
            build_utils.exit_process(1)
        return

    pypi_repository_args = ""
    if pypi_repository:
        pypi_repository_args = f'--repository-url "{pypi_repository}"'

    # Check twine command
    build_utils.command_exists("twine", exit_on_error=exit_on_error)

    # Publish on pypi
    build_utils.run(
        f'twine upload --non-interactive -u "{pypi_user}" -p "{pypi_token}" {pypi_repository_args} dist/*',
        exit_on_error=exit_on_error,
    )


def code_checks(
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
        black (bool, optional): Activate black formatting check. Defaults to True.
        isort (bool, optional): Activate isort import sorting check. Defaults to True.
        pydocstyle (bool, optional): Activate pydocstyle docstring check. Defaults to True.
        mypy (bool, optional): Activate mypy typing check. Defaults to True.
        flake8 (bool, optional): Activate flake8 linting check. Defaults to True.
        safety (bool, optional): Activate saftey check via pipenv. Defaults to True.
        exit_on_error (bool, optional): If `True`, exit process as soon as error occures. Defaults to True.
    """

    command_prefix = ""
    if is_pipenv_environment():
        command_prefix = "pipenv run"

    if black:
        if not command_prefix:
            # Check twine command
            build_utils.command_exists("black", exit_on_error=exit_on_error)

        build_utils.run(
            f"{command_prefix} black --check src", exit_on_error=exit_on_error
        )
        build_utils.run(
            f"{command_prefix} black --check tests", exit_on_error=exit_on_error
        )

    if isort:
        if not command_prefix:
            # Check twine command
            build_utils.command_exists("isort", exit_on_error=exit_on_error)

        build_utils.run(
            f"{command_prefix} isort --profile black --check-only src",
            exit_on_error=exit_on_error,
        )
        build_utils.run(
            f"{command_prefix} isort --profile black --check-only tests",
            exit_on_error=exit_on_error,
        )

    if pydocstyle:
        if not command_prefix:
            # Check twine command
            build_utils.command_exists("pydocstyle", exit_on_error=exit_on_error)

        build_utils.run(f"{command_prefix} pydocstyle src", exit_on_error=exit_on_error)

        # Run linters and checks
    if mypy:
        if not command_prefix:
            # Check twine command
            build_utils.command_exists("mypy", exit_on_error=exit_on_error)

        build_utils.run(f"{command_prefix} mypy src", exit_on_error=exit_on_error)

    if flake8:
        if not command_prefix:
            # Check twine command
            build_utils.command_exists("flake8", exit_on_error=exit_on_error)

        build_utils.run(
            f"{command_prefix} flake8 --show-source --statistics src",
            exit_on_error=exit_on_error,
        )
        build_utils.run(
            f"{command_prefix} flake8 --show-source --statistics tests",
            exit_on_error=exit_on_error,
        )

    if safety:
        # Check pipenv command
        build_utils.command_exists("pipenv", exit_on_error=exit_on_error)

        # Check using pipenv (runs safety check)
        build_utils.run("pipenv check", exit_on_error=exit_on_error)


def update_version(module_path: str, version: str, exit_on_error: bool = True) -> None:
    """Update version in specified module.

    Args:
        module_path (str): Python module with a `__version__` attribute.
        version (str): New version number to write into `__version__` attribute.
        exit_on_error (bool, optional): If `True`, exit process as soon as error occures. Defaults to True.
    """
    if not version:
        build_utils.log("Cannot update version, no version provided")
        if exit_on_error:
            build_utils.exit_process(1)
        return

    if not os.path.exists(module_path):
        build_utils.log("Couldn't find file: " + module_path)
        if exit_on_error:
            build_utils.exit_process(1)
        return

    with open(module_path, "r+") as f:
        data = f.read()
        f.seek(0)
        f.write(re.sub(r"__version__ = \".+\"", f'__version__ = "{version}"', data))
        f.truncate()


def build_distribution(exit_on_error: bool = True) -> None:
    """Build python package distribution.

    Args:
        exit_on_error (bool, optional): If `True`, exit process as soon as error occures. Defaults to True.
    """

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
        "python setup.py sdist bdist_wheel clean --all", exit_on_error=exit_on_error
    )

    # Check twine command
    build_utils.command_exists("twine", exit_on_error=exit_on_error)

    # Check the archives with twine
    build_utils.run("twine check dist/*", exit_on_error=exit_on_error)
