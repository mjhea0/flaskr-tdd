import json
from project import app, db, models


def setup_module(module):
    """Set up test client and clean DB."""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    with app.app_context():
        db.create_all()
    module.client = app.test_client()


def teardown_module(module):
    with app.app_context():
        db.drop_all()


def test_search_without_query():
    """Covers: search view without query (uncovered path)."""
    response = client.get("/search/")
    assert response.status_code == 200
    assert b"Search" in response.data  # assuming template title


def test_login_invalid_username():
    """Covers: login route with invalid username."""
    response = client.post("/login", data={
        "username": "wrong",
        "password": "admin"
    }, follow_redirects=True)
    assert b"Invalid username" in response.data


def test_login_invalid_password():
    """Covers: login route with invalid password."""
    response = client.post("/login", data={
        "username": "admin",
        "password": "wrong"
    }, follow_redirects=True)
    assert b"Invalid password" in response.data


def test_create_note_missing_json():
    """Covers: missing JSON in create_note."""
    response = client.post("/api/notes", data="not-json", content_type="application/json")
    assert response.status_code == 400
    assert response.json["error"] == "Invalid JSON"


def test_update_note_missing_json():
    """Covers: missing JSON in update_note."""
    # Add a note first
    with app.app_context():
        note = models.Note(content="sample")
        db.session.add(note)
        db.session.commit()
        note_id = note.id

    response = client.put(f"/api/notes/{note_id}", data="not-json", content_type="application/json")
    assert response.status_code == 400
    assert response.json["error"] == "Invalid JSON"


def test_delete_note_not_found():
    """Covers: trying to delete a nonexistent note."""
    response = client.delete("/api/notes/9999")
    assert response.status_code == 404
    assert response.json["error"] == "Note not found"
