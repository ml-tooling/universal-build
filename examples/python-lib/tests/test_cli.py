#!/usr/bin/env python
from typing import Generator

import pytest
from typer import Typer
from typer.testing import CliRunner

from .conftest import Utils


@pytest.fixture(scope="module")
def runner() -> Generator:
    print("Create runner fixture")
    # Artifical usage of yiel to show possible setup / teardown
    # - return would be sufficient here
    yield CliRunner()
    print("Teardown runner fixture")


def test_cli(runner: CliRunner, cli_app: Typer) -> None:
    """Test the CLI."""
    print(f"Execute {test_cli.__name__}")
    result = runner.invoke(cli_app, ["hello", "foo"])
    assert result.exit_code == 0
    assert "foo" in result.stdout


def test_cli_2(runner: CliRunner, cli_app: Typer) -> None:
    """Test the CLI."""
    print(f"Execute {test_cli_2.__name__}")
    result = runner.invoke(cli_app, ["hello", "bar"])
    assert result.exit_code == 0
    assert "bar" in result.stdout


def test_use_shared_helpers(test_utils: Utils) -> None:
    print(test_utils.super_useful_helper())
    assert True
