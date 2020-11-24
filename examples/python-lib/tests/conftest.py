import pytest
from fastapi import FastAPI
from typer import Typer


@pytest.fixture(scope="session")
def cli_app() -> Typer:
    from template_package import _cli

    print("Create cli_app fixture")
    return _cli.app


@pytest.fixture(scope="session")
def api_app() -> FastAPI:
    from template_package import api

    print("Create api_app fixture")
    return api.app


class Utils:
    def super_useful_helper(self):
        return "This really helped me"


@pytest.fixture(scope="session")
def test_utils() -> Utils:
    return Utils()
