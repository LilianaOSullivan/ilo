from routers.Potion import loggedIn
import Helper
import pytest
from Config import Config
from CassandraModels import users


@pytest.mark.helper_validate_keys
def test_blacklist_enforced(client, apikey):
    """Ensure potion IP blacklisting is working as intended"""
    response = client.post("/potion", data={"address": "127.0.0.1"})
    assert response.status_code == 401


@pytest.mark.helper_validate_keys
def test_no_logged_in_users(client):
    """Ensure FastAPI returns false for no logged in users"""
    from cassandra.cluster import Cluster

    c = Cluster()
    s = c.connect("ilo")
    s.execute("TRUNCATE users")
    Config.Potion_IP = "testclient"
    response = client.post("/potion", data={"address": "127.0.0.1"})
    assert response.text == "false"


@pytest.mark.helper_validate_keys
def test_logged_in_users(client):
    """Ensure the helper returns True for a valid key"""
    user = users.create(
        username="mittens",
        password="password",
        public_key="pk",
        logged_in="127.0.0.1",
        api_key="123-123-123",
    )
    Config.Potion_IP = "testclient"
    response = client.post("/potion", data={"address": "127.0.0.1"})
    assert response.text == "true"
    users.delete(user)
