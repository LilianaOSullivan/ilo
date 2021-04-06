import pytest
from fastapi.testclient import TestClient
from tests import mocks
from unittest.mock import patch

@pytest.fixture
def client():
    import app
    return TestClient(app.app)

@pytest.fixture
def client_w_mock():
    p = patch('app.open', new=mocks.MOCKED_open)
    p.start()
    import app
    yield TestClient(app.app)
    p.stop()
