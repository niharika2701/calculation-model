def test_create_user_success(client):
    response = client.post("/users", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "securepass123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert "password_hash" not in data
    assert "id" in data

def test_create_duplicate_username(client):
    client.post("/users", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "securepass123"
    })
    response = client.post("/users", json={
        "username": "alice",
        "email": "different@example.com",
        "password": "securepass123"
    })
    assert response.status_code == 400
    assert "Username already taken" in response.json()["error"]

def test_create_duplicate_email(client):
    client.post("/users", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "securepass123"
    })
    response = client.post("/users", json={
        "username": "bob",
        "email": "alice@example.com",
        "password": "securepass123"
    })
    assert response.status_code == 400
    assert "Email already registered" in response.json()["error"]

def test_get_user_success(client):
    client.post("/users", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "securepass123"
    })
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["username"] == "alice"

def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404

def test_create_user_invalid_email(client):
    response = client.post("/users", json={
        "username": "alice",
        "email": "not-valid-email",
        "password": "securepass123"
    })
    assert response.status_code == 400
    assert "email" in response.json()["error"].lower()