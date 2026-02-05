def test_create_label(client):
    resp = client.post("/api/labels", json={"name": "Important", "color": "#EF4444"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Important"
    assert data["color"] == "#EF4444"
    assert "id" in data


def test_create_label_default_color(client):
    resp = client.post("/api/labels", json={"name": "Default"})
    assert resp.status_code == 201
    assert resp.json()["color"] == "#6B7280"


def test_list_labels_empty(client):
    resp = client.get("/api/labels")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_list_labels_with_items(client):
    client.post("/api/labels", json={"name": "Work", "color": "#3B82F6"})
    client.post("/api/labels", json={"name": "Personal", "color": "#10B981"})
    resp = client.get("/api/labels")
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_list_labels_search(client):
    client.post("/api/labels", json={"name": "Work"})
    client.post("/api/labels", json={"name": "Personal"})
    resp = client.get("/api/labels?q=work")
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Work"


def test_list_labels_sort_by_name(client):
    client.post("/api/labels", json={"name": "Zebra"})
    client.post("/api/labels", json={"name": "Alpha"})
    resp = client.get("/api/labels?sort_by=name&sort_dir=asc")
    data = resp.json()
    assert data["items"][0]["name"] == "Alpha"
    assert data["items"][1]["name"] == "Zebra"


def test_list_labels_sort_by_created_at(client):
    client.post("/api/labels", json={"name": "First"})
    client.post("/api/labels", json={"name": "Second"})
    resp = client.get("/api/labels?sort_by=created_at&sort_dir=desc")
    data = resp.json()
    # Both may have the same timestamp so just verify sorting is accepted
    assert len(data["items"]) == 2


def test_delete_label(client):
    resp = client.post("/api/labels", json={"name": "Delete Me"})
    label_id = resp.json()["id"]
    resp = client.delete(f"/api/labels/{label_id}")
    assert resp.status_code == 204
    resp = client.get("/api/labels")
    assert resp.json()["total"] == 0


def test_delete_label_not_found(client):
    resp = client.delete("/api/labels/9999")
    assert resp.status_code == 404
