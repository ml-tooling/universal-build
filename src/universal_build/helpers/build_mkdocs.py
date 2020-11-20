import sys

from universal_build import build_utils

PIPENV_RUN = "pipenv run"


def install_build_env() -> None:
    """Installs a new virtual environment via pipenv."""
    build_utils.run("pipenv --rm")
    build_utils.run(
        f"pipenv install --dev --python={sys.executable} --skip-lock --site-packages",
        exit_on_error=True,
    )


def lint_markdown() -> None:
    """Run markdownlint on markdown documentation."""
    build_utils.log("Run linters and style checks:")
    build_utils.run(
        "markdownlint --config='.markdown-lint.yml' ./docs", exit_on_error=True
    )


def build_mkdocs(command_prefix: str = PIPENV_RUN) -> None:
    """Build mkdocs markdown documentation.

    Args:
        command_prefix (str, optional): Prefix to use for all commands. Defaults to `pipenv run`.
    """
    build_utils.run(f"{command_prefix} mkdocs build", exit_on_error=True)


def deploy_gh_pages(command_prefix: str = PIPENV_RUN) -> None:
    """Deploy mkdocs documentation to Github pages.

    Args:
        command_prefix (str, optional): Prefix to use for all commands. Defaults to `pipenv run`.
    """
    build_utils.log("Deploy documentation to Github pages:")
    build_utils.run(
        f"{command_prefix} mkdocs gh-deploy --clean", exit_on_error=True, timeout=120
    )


def run_dev_mode(port: int = 8001, command_prefix: str = PIPENV_RUN) -> None:
    """Run mkdocs development server.

    Args:
        port (int, optional): Port to use for mkdocs development server. Defaults to 8001.
        command_prefix (str, optional): Prefix to use for all commands. Defaults to `pipenv run`.
    """
    build_utils.log(f"Run docs in development mode (http://localhost:{port}):")
    build_utils.run(
        f"{command_prefix} mkdocs serve --dev-addr 0.0.0.0:{port}", exit_on_error=True
    )
