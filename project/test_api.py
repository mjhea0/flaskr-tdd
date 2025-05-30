import pytest
import json
from project import app, db, models

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_create_note_success(client):
    response = client.post("/api/notes", json={"content": "Test note"})
    assert response.status_code == 201
    data = response.get_json()
    assert data["content"] == "Test note"
    assert "id" in data

def test_create_note_no_content(client):
    response = client.post("/api/notes", json={})
    assert response.status_code == 400

def test_get_notes_empty(client):
    response = client.get("/api/notes")
    assert response.status_code == 200
    data = response.get_json()
    assert data == []

def test_get_note_not_found(client):
    response = client.get("/api/notes/999")
    assert response.status_code == 404

def test_update_note_success(client):
    # Create a note first
    client.post("/api/notes", json={"content": "Old content"})
    response = client.put("/api/notes/1", json={"content": "New content"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["content"] == "New content"

def test_update_note_not_found(client):
    response = client.put("/api/notes/999", json={"content": "Test"})
    assert response.status_code == 404

def test_delete_note_success(client):
    # Create a note first
    client.post("/api/notes", json={"content": "To delete"})
    response = client.delete("/api/notes/1")
    assert response.status_code == 200
    data = response.get_json()
    assert "deleted" in data["message"].lower()

def test_delete_note_not_found(client):
    response = client.delete("/api/notes/999")
    assert response.status_code == 404
