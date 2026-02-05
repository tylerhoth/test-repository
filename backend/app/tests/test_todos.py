def test_create_todo(client):
    resp = client.post("/api/todos", json={"title": "Buy milk"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Buy milk"
    assert data["completed"] is False
    assert "id" in data


def test_list_todos_empty(client):
    resp = client.get("/api/todos")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["page_size"] == 20


def test_list_todos_with_items(client):
    client.post("/api/todos", json={"title": "Task 1"})
    client.post("/api/todos", json={"title": "Task 2"})
    resp = client.get("/api/todos")
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_list_todos_pagination(client):
    for i in range(5):
        client.post("/api/todos", json={"title": f"Task {i}"})
    resp = client.get("/api/todos?page=1&page_size=2")
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["page_size"] == 2


def test_list_todos_search(client):
    client.post("/api/todos", json={"title": "Buy milk"})
    client.post("/api/todos", json={"title": "Walk dog"})
    resp = client.get("/api/todos?q=milk")
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Buy milk"


def test_list_todos_sort(client):
    client.post("/api/todos", json={"title": "A task"})
    client.post("/api/todos", json={"title": "B task"})
    resp = client.get("/api/todos?sort_by=title&sort_dir=desc")
    data = resp.json()
    assert data["items"][0]["title"] == "B task"


def test_delete_todo(client):
    resp = client.post("/api/todos", json={"title": "Delete me"})
    todo_id = resp.json()["id"]
    resp = client.delete(f"/api/todos/{todo_id}")
    assert resp.status_code == 204

    resp = client.get("/api/todos")
    assert resp.json()["total"] == 0


def test_delete_todo_not_found(client):
    resp = client.delete("/api/todos/9999")
    assert resp.status_code == 404
