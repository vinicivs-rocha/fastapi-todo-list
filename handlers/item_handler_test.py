import os
import uuid
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer

from db.pg import run_migrations
from main import app

postgres = PostgresContainer()


@pytest.fixture(scope="module", autouse=True)
def setup(request):
    postgres.start()

    def stop_container():
        postgres.stop()

    request.addfinalizer(stop_container)

    os.environ["DATABASE_URL"] = postgres.get_connection_url()

    run_migrations()


test_client = TestClient(app=app)


def test_create_item():
    response = test_client.post(
        "/items/",
        json={
            "title": "created title",
            "description": "created description",
            "resolved": False,
        },
    )
    assert response.status_code == 201
    response_data = response.json()
    try:
        uuid.UUID(response_data["id"], version=4)
    except ValueError:
        assert False, "id is not a valid UUID"
    assert response_data["message"] == "Item created successfully"


def test_list_items():
    response = test_client.get("/items/")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    for item in response_data:
        try:
            uuid.UUID(item["id"], version=4)
        except ValueError:
            assert False, "id is not a valid UUID"
        assert isinstance(item["title"], str)
        assert isinstance(item["description"], str) or item["description"] is None
        assert isinstance(item["resolved"], bool)
        assert isinstance(item["created_at"], str)
        try:
            datetime.fromisoformat(item["created_at"])
        except ValueError:
            assert False, "created_at is not a valid datetime"


def test_list_items_query():
    test_client.post(
        "/items/",
        json={
            "title": "some different title",
            "description": "some different description",
            "resolved": False,
        },
    )
    response = test_client.get("/items/", params={"query": "created title"})
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    item = response_data[0]
    try:
        uuid.UUID(item["id"], version=4)
    except ValueError:
        assert False, "id is not a valid UUID"
    assert item["title"] == "created title"
    assert item["description"] == "created description"
    assert item["resolved"] == False
    try:
        datetime.fromisoformat(item["created_at"])
    except ValueError:
        assert False, "created_at is not a valid datetime"


def test_items_count():
    response = test_client.get("/items/count")
    assert response.status_code == 200
    response_data = response.json()
    assert isinstance(response_data, dict)
    assert isinstance(response_data["count"], int)
    assert response_data["count"] >= 0


def test_update_item():
    list_response = test_client.get("/items/")
    assert list_response.status_code == 200, "Failed to list items"
    list_response_data: list = list_response.json()
    update_item: dict = list_response_data.pop(0)
    assert update_item is not None, "No items found"
    update_item.update(
        {
            "title": "updated title",
            "description": "updated description",
            "resolved": True,
        }
    )
    response = test_client.put(f"/items/{update_item['id']}", json=update_item)
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data["message"] == "Item updated successfully"
    updated_list_response = test_client.get("/items/", params={"resolved": True})
    updated_list_response_data: list = updated_list_response.json()
    updated_item = next(
        (
            item
            for item in updated_list_response_data
            if item["id"] == update_item["id"]
        ),
        None,
    )
    assert updated_item is not None, "Item not found in updated list"
    assert updated_item["title"] == "updated title"
    assert updated_item["description"] == "updated description"
    assert updated_item["resolved"] == True


def test_delete_item():
    list_response = test_client.get("/items/")
    assert list_response.status_code == 200, "Failed to list items"
    list_response_data: list = list_response.json()
    delete_item: dict = list_response_data.pop(0)
    response = test_client.delete(f"/items/{delete_item['id']}")
    assert response.status_code == 200, response.text
    response_data = response.json()
    assert response_data["message"] == "Item deleted successfully"
    updated_list_response = test_client.get("/items/")
    updated_list_response_data: list = updated_list_response.json()
    updated_item = next(
        (
            item
            for item in updated_list_response_data
            if item["id"] == delete_item["id"]
        ),
        None,
    )
    assert updated_item is None, "Item not deleted"
