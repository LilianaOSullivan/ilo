from unittest.mock import patch

import pytest
from Config import Config

from tests import mocks


@pytest.mark.startup
def test_config_no_empty(client_w_mock):
    config_vars = {key:value for key, value in Config.__dict__.items() if not key.startswith('__') and not callable(key)}
    assert all(i for i in config_vars.values())

def test_config_uses_defaults(client_w_mock):
    with open('general_config.yaml', 'r') as f:
        s = f.read()
        print(s)
    config_vars = {key:value for key, value in Config.__dict__.items() if not key.startswith('__') and not callable(key)}
    assert config_vars["MongoDB_address"] == "mongodb://127.0.0.1:27017/"
    assert config_vars["MongoDB_database"] == "ilo_mock"
    assert config_vars["MongoDB_user_collection"] == "users"
    assert config_vars["MongoDB_apiKey_collection"] == "api_keys"
    assert config_vars["Potion_IP"] == "0.0.0.0:4000"
