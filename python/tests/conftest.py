from enum import auto
from unittest.mock import patch

import app
import pytest
import yaml
from cassandra.cqlengine import connection
from cassandra.cqlengine.management import sync_table
from CassandraModels import *
from fastapi.testclient import TestClient

from tests import mocks

config = yaml.safe_load(open("general_config.yaml", "r").read())


@pytest.fixture
def client():
    return TestClient(app.app)


@pytest.fixture(scope="session", autouse=True)
def cassandra():
    connection.setup(
        [config["Cassandra_address"]], config["Cassandra_keyspace"], protocol_version=3
    )
    sync_table(users, [config["Cassandra_keyspace"]])
    sync_table(api_keys, [config["Cassandra_keyspace"]])


@pytest.fixture()
def apikey():
    key = api_keys.create()
    invalid_key = str(uuid.uuid4())
    yield dict(
        valid=str(key.key_id),
        invalid=invalid_key,
        invalid_correct_format=invalid_key,
        invalid_incorrect_format="the-weft-and-weave-of-fate-guides",
    )
    try:
        api_keys.delete(key)
    except:
        pass


# @pytest.fixture(scope="function")
# def db_cleanup():
#     to_delete = yield
#     for k, v in to_delete.items():
#         if k == "api_keys":
#             for key in v:
#                 api_keys.delete(key_id=key)


@pytest.fixture
def client_w_mock():
    p = patch("app.open", new=mocks.MOCKED_open)
    p.start()
    import app

    yield TestClient(app.app)
    p.stop()
