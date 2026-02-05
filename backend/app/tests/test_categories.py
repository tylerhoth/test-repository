def test_create_category(client):
    resp = client.post("/api/categories", json={"name": "Groceries"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Groceries"
    assert data["is_system"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_category_system(client):
    resp = client.post("/api/categories", json={"name": "Income", "is_system": True})
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Income"
    assert data["is_system"] is True


def test_list_categories_empty(client):
    resp = client.get("/api/categories")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["page_size"] == 100


def test_list_categories_with_items(client):
    client.post("/api/categories", json={"name": "Groceries"})
    client.post("/api/categories", json={"name": "Dining"})
    client.post("/api/categories", json={"name": "Transportation"})
    resp = client.get("/api/categories")
    data = resp.json()
    assert data["total"] == 3
    assert len(data["items"]) == 3


def test_list_categories_search(client):
    client.post("/api/categories", json={"name": "Groceries"})
    client.post("/api/categories", json={"name": "Dining Out"})
    client.post("/api/categories", json={"name": "Transportation"})
    resp = client.get("/api/categories?q=Groc")
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Groceries"


def test_list_categories_sort_by_name(client):
    client.post("/api/categories", json={"name": "Zebra"})
    client.post("/api/categories", json={"name": "Alpha"})
    client.post("/api/categories", json={"name": "Beta"})
    resp = client.get("/api/categories?sort_by=name&sort_dir=asc")
    data = resp.json()
    assert data["items"][0]["name"] == "Alpha"
    assert data["items"][1]["name"] == "Beta"
    assert data["items"][2]["name"] == "Zebra"


def test_list_categories_sort_descending(client):
    client.post("/api/categories", json={"name": "Alpha"})
    client.post("/api/categories", json={"name": "Beta"})
    resp = client.get("/api/categories?sort_by=name&sort_dir=desc")
    data = resp.json()
    assert data["items"][0]["name"] == "Beta"
    assert data["items"][1]["name"] == "Alpha"


def test_list_categories_pagination(client):
    for i in range(5):
        client.post("/api/categories", json={"name": f"Category {i}"})
    resp = client.get("/api/categories?page=1&page_size=2")
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["page_size"] == 2
