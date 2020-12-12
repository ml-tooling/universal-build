"""Utilities to help building MkDocs documentations."""

import os
import sys

from universal_build import build_utils
from universal_build.helpers.build_python import is_pipenv_environment

_PIPENV_RUN = "pipenv run"


def install_build_env(exit_on_error: bool = True) -> None:
    """Installs a new virtual environment via pipenv.

    Args:
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """
    # Check if pipenv exists
    build_utils.command_exists("pipenv", exit_on_error=exit_on_error)

    if not os.path.exists("Pipfile"):
        build_utils.log("No Pipfile discovered, cannot install pipenv environemnt")
        if exit_on_error:
            build_utils.exit_process(1)
        return

    build_utils.run("pipenv --rm", exit_on_error=False)
    build_utils.run(
        f"pipenv install --dev --python={sys.executable} --skip-lock --site-packages",
        exit_on_error=exit_on_error,
    )


def lint_markdown(markdownlint: bool = True, exit_on_error: bool = True) -> None:
    """Run markdownlint on markdown documentation.

    Args:
        markdownlint (bool, optional): Activate markdown linting via `markdownlint`. Defaults to `True`.
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """
    build_utils.log("Run linters and style checks:")

    if markdownlint and build_utils.command_exists(
        "markdownlint", exit_on_error=exit_on_error
    ):
        config_file_arg = ""
        if os.path.exists(".markdown-lint.yml"):
            config_file_arg = "--config='.markdown-lint.yml'"

        build_utils.run(
            f"markdownlint {config_file_arg} ./docs", exit_on_error=exit_on_error
        )


def build_mkdocs(exit_on_error: bool = True) -> None:
    """Build mkdocs markdown documentation.

    Args:
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """

    command_prefix = ""
    if is_pipenv_environment():
        command_prefix = _PIPENV_RUN
    else:
        # Check mkdocs command
        build_utils.command_exists("mkdocs", exit_on_error=exit_on_error)

    build_utils.run(f"{command_prefix} mkdocs build", exit_on_error=exit_on_error)


def deploy_gh_pages(exit_on_error: bool = True) -> None:
    """Deploy mkdocs documentation to Github pages.

    Args:
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """
    build_utils.log("Deploy documentation to Github pages:")

    command_prefix = ""
    if is_pipenv_environment():
        command_prefix = _PIPENV_RUN
    else:
        # Check mkdocs command
        build_utils.command_exists("mkdocs", exit_on_error=exit_on_error)

    build_utils.run(
        f"{command_prefix} mkdocs gh-deploy --clean",
        exit_on_error=exit_on_error,
        timeout=120,
    )


def run_dev_mode(port: int = 8001, exit_on_error: bool = True) -> None:
    """Run mkdocs development server.

    Args:
        port (int, optional): Port to use for mkdocs development server. Defaults to 8001.
        exit_on_error (bool, optional): Exit process if an error occurs. Defaults to `True`.
    """
    build_utils.log(f"Run docs in development mode (http://localhost:{port}):")

    command_prefix = ""
    if is_pipenv_environment():
        command_prefix = _PIPENV_RUN
    else:
        # Check mkdocs command
        build_utils.command_exists("mkdocs", exit_on_error=exit_on_error)

    build_utils.run(
        f"{command_prefix} mkdocs serve --dev-addr 0.0.0.0:{port}",
        exit_on_error=exit_on_error,
    )
