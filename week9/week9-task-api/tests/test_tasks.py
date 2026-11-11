def test_task_crud_and_pagination(client, auth_headers):
    url = "/api/v1/tasks"
    created = client.post(url, headers=auth_headers, json={
        "title": "Build REST API", "priority": "high", "status": "in_progress"
    })
    assert created.status_code == 201
    task_id = created.get_json()["data"]["task"]["id"]
    assert client.get(url, headers=auth_headers).get_json()["data"]["pagination"]["total_items"] == 1
    assert client.get(f"{url}/{task_id}", headers=auth_headers).status_code == 200
    assert client.patch(f"{url}/{task_id}", headers=auth_headers,
                        json={"status": "completed"}).status_code == 200
    assert client.delete(f"{url}/{task_id}", headers=auth_headers).status_code == 204

def test_validation_and_auth(client, auth_headers):
    assert client.post("/api/v1/tasks", json={"title": "No token"}).status_code == 401
    assert client.post("/api/v1/tasks", headers=auth_headers, json={"title": "x"}).status_code == 400

def test_filter_search(client, auth_headers):
    client.post("/api/v1/tasks", headers=auth_headers, json={"title": "Learn Flask", "priority": "high"})
    response = client.get("/api/v1/tasks?priority=high&search=Flask", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.get_json()["data"]["tasks"]) == 1
