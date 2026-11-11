def test_profile_read_update_delete(client, auth_headers):
    assert client.get("/api/v1/users/me", headers=auth_headers).status_code == 200
    update = client.patch("/api/v1/users/me", headers=auth_headers, json={"username": "updated"})
    assert update.status_code == 200
    assert update.get_json()["data"]["user"]["username"] == "updated"
    assert client.delete("/api/v1/users/me", headers=auth_headers).status_code == 200
