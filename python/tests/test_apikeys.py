from uuid import UUID

from cassandra.cqlengine.query import DoesNotExist
from CassandraModels import *
from pytest import fail, mark


@mark.apikeys
def test_create_key_format(client):
    """Ensures a UUID is returned"""
    response = client.post("/key/")
    json = response.json()
    key = json["detail"]
    try:
        UUID(key)
    except ValueError:
        fail("A none-UUID was returned")
    try:
        key = api_keys.get(key_id=key)
    except DoesNotExist:
        fail("Failed to write to database")


@mark.apikeys
def test_create_key_written_to_db(client):
    """Ensures the key is written to the database"""
    response = client.post("/key/")
    json = response.json()
    key = json["detail"]
    try:
        key = api_keys.get(key_id=key)
    except DoesNotExist:
        fail("Failed to write to database")


@mark.apikeys
def test_create_key_general(client):
    """Ensures the returns are of the correct format"""
    response = client.post("/key/")
    assert response.status_code == 201
    json = response.json()
    assert "detail" in json

    # db_cleanup.send(None)
    # db_cleanup.send({"api_keys":[key]})


@mark.apikeys
def test_create_validate_UUID_version(client):
    """Validates a UUID4 is used"""
    response = client.post("/key/")
    try:
        assert (
            UUID(response.json()["detail"]).version == 4
        ), "4 was not the UUID version being used."
    except ValueError:
        fail("A none-UUID was returned")


@mark.apikeys
def test_delete_removed_from_database(client, apikey):
    """Ensures a key is deleted from a database"""
    response = client.delete(f"/key/{apikey['valid']}")
    assert response.status_code == 200
    json = response.json()
    assert "detail" in json
    assert f"Successfully deleted {str(apikey['valid'])}" in json["detail"]
    try:
        key = api_keys.get(key_id=apikey["valid"])
    except DoesNotExist:
        return
    fail("API Key was not removed from the database")


@mark.apikeys
def test_delete_invalid_key_incorrect_format(client):
    """Sends a none-valid UUID formatted string"""
    key = "Mittens"
    response = client.delete(f"/key/{key}")
    json = response.json()
    assert response.status_code == 400
    assert "detail" in json
    assert json["detail"] == f"The key {key} is not a valid key"


@mark.apikeys
def test_delete_invalid_key_correct_format(client, apikey):
    """Sends a valid UUID that does not exist as a key"""
    response = client.delete(f"/key/{apikey['invalid_correct_format']}")
    json = response.json()
    assert response.status_code == 404
    assert "detail" in json
    assert (
        json["detail"] == f"The key {apikey['invalid_correct_format']} does not exist"
    )
