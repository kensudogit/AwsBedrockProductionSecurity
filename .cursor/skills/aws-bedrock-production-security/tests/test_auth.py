"""Basic denial tests; run with PYTHONPATH=templates/backend pytest tests."""
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)


def test_missing_token_denied():
    assert client.post('/api/generate', json={'prompt': 'hello'}).status_code == 401


def test_health():
    assert client.get('/health').status_code == 200


def test_invalid_token_denied():
    assert client.post('/api/generate', headers={'Authorization': 'Bearer malformed'}, json={'prompt': 'hello'}).status_code == 401
