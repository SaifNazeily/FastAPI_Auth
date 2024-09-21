from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_user():
    response = client.get("/users/sampleuser")
    assert response.status_code ==200
    assert response.json()["username"] == "sampleuser"

def test_user_not_found():
    response = client.get("/users/nonexistent")
    assert response.status_code == 404