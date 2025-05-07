from fastapi.testclient import TestClient
from main.main import app

def test_get_contacts_success(monkeypatch):
    # Mock data
    mock_contacts = {
        "contacts": [
            {
                "first_name": "Test",
                "last_name": "User",
                "zip_code": "00000",
                "phone_number": "555-0000",
                "last_contacted": "2024-01-01T00:00:00Z"
            }
        ]
    }
    # Mock repository
    class MockRepo:
        def load_contacts(self):
            from main.models import ContactsList
            return ContactsList(**mock_contacts)

    # Patch the repo in the app
    app.dependency_overrides = {}
    from main.main import contacts_repo
    monkeypatch.setattr(contacts_repo, "load_contacts", MockRepo().load_contacts)

    client = TestClient(app)
    response = client.get("/contacts")
    assert response.status_code == 200
    assert response.json() == mock_contacts

def test_get_contacts_file_not_found(monkeypatch):
    from main.main import contacts_repo

    def raise_file_not_found():
        raise FileNotFoundError

    monkeypatch.setattr(contacts_repo, "load_contacts", raise_file_not_found)
    client = TestClient(app)
    response = client.get("/contacts")
    assert response.status_code == 404

def test_get_contacts_value_error(monkeypatch):
    from main.main import contacts_repo

    def raise_value_error():
        raise ValueError("bad data")

    monkeypatch.setattr(contacts_repo, "load_contacts", raise_value_error)
    client = TestClient(app)
    response = client.get("/contacts")
    assert response.status_code == 400
    assert response.json()["detail"] == "bad data"

def test_get_contacts_unexpected_error(monkeypatch):
    from main.main import contacts_repo

    def raise_exception():
        raise Exception("unexpected")

    monkeypatch.setattr(contacts_repo, "load_contacts", raise_exception)
    client = TestClient(app)
    response = client.get("/contacts")
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error."