import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pytest_mock import MockerFixture

from .conftest import Utils


@pytest.fixture(scope="function")
def client(api_app: FastAPI) -> TestClient:
    print("Create client fixture")
    return TestClient(api_app)


@pytest.mark.parametrize("item_id", [123, 124, 125])
def test_api(client: TestClient, item_id: int) -> None:
    print(f"Execute {test_api.__name__}")
    response = client.get(f"/items/{item_id}", params={"q": "foo"})
    assert response.status_code == 200
    assert response.json() == {"item_id": item_id, "q": "foo"}


# This function uses the pytest-mock fixture,
# which is injected when pytest-mock was installed
def test_with_mock(client: TestClient, mocker: MockerFixture) -> None:
    print(f"Execute {test_with_mock.__name__}")
    mocker.patch(
        "template_package.api.slow_call_to_external_url", return_value={"duration": 1}
    )
    response = client.get("/ext-call")
    assert response.status_code == 200
    assert response.json() == {"duration": 1}


@pytest.mark.slow
def slow_test():
    response = client.get("/ext-call")
    assert response.status_code == 200
    assert response.json() == {"duration": 10}


def test_use_shared_helpers(test_utils: Utils) -> None:
    print(test_utils.super_useful_helper())
    assert True
