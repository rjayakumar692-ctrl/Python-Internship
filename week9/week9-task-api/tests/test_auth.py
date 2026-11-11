def test_register_and_login(client):
    response = client.post("/api/v1/auth/register", json={
        "username": "alice", "email": "alice@example.com", "password": "Password123"
    })
    assert response.status_code == 201
    assert "access_token" in response.get_json()["data"]
    login = client.post("/api/v1/auth/login", json={
        "email": "alice@example.com", "password": "Password123"
    })
    assert login.status_code == 200

def test_duplicate_registration(client):
    payload = {"username": "alice", "email": "alice@example.com", "password": "Password123"}
    client.post("/api/v1/auth/register", json=payload)
    assert client.post("/api/v1/auth/register", json=payload).status_code == 409

def test_invalid_login(client):
    assert client.post("/api/v1/auth/login", json={
        "email": "none@example.com", "password": "wrong"
    }).status_code == 401
