def test_create_budget(client):
    # Create category
    cat_resp = client.post("/api/categories", json={"name": "Groceries"})
    category_id = cat_resp.json()["id"]

    # Create budget
    resp = client.post(
        "/api/budgets",
        json={
            "category_id": category_id,
            "amount_limit": 500.00,
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["category_id"] == category_id
    assert data["amount_limit"] == 500.00
    assert "id" in data
    assert "created_at" in data


def test_create_budget_updates_existing(client):
    # Create category
    cat_resp = client.post("/api/categories", json={"name": "Groceries"})
    category_id = cat_resp.json()["id"]

    # Create initial budget
    resp1 = client.post(
        "/api/budgets",
        json={
            "category_id": category_id,
            "amount_limit": 500.00,
        },
    )
    assert resp1.status_code == 201
    budget1_id = resp1.json()["id"]

    # Create budget for same category (should update)
    resp2 = client.post(
        "/api/budgets",
        json={
            "category_id": category_id,
            "amount_limit": 600.00,
        },
    )
    assert resp2.status_code == 201
    data = resp2.json()
    assert data["category_id"] == category_id
    assert data["amount_limit"] == 600.00
    # Should be the same budget (upsert)
    assert data["id"] == budget1_id

    # Verify only one budget exists
    resp = client.get("/api/budgets")
    assert resp.json()["total"] == 1


def test_list_budgets_empty(client):
    resp = client.get("/api/budgets")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["page_size"] == 20


def test_list_budgets_with_items(client):
    # Create categories
    cat1_resp = client.post("/api/categories", json={"name": "Groceries"})
    cat2_resp = client.post("/api/categories", json={"name": "Dining"})
    category1_id = cat1_resp.json()["id"]
    category2_id = cat2_resp.json()["id"]

    # Create budgets
    client.post(
        "/api/budgets",
        json={
            "category_id": category1_id,
            "amount_limit": 500.00,
        },
    )
    client.post(
        "/api/budgets",
        json={
            "category_id": category2_id,
            "amount_limit": 300.00,
        },
    )

    resp = client.get("/api/budgets")
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_list_budgets_pagination(client):
    # Create categories and budgets
    for i in range(5):
        cat_resp = client.post("/api/categories", json={"name": f"Category {i}"})
        category_id = cat_resp.json()["id"]
        client.post(
            "/api/budgets",
            json={
                "category_id": category_id,
                "amount_limit": 100.00 * (i + 1),
            },
        )

    resp = client.get("/api/budgets?page=1&page_size=2")
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["page_size"] == 2


def test_list_budgets_sort(client):
    # Create categories
    cat1_resp = client.post("/api/categories", json={"name": "Groceries"})
    cat2_resp = client.post("/api/categories", json={"name": "Dining"})
    category1_id = cat1_resp.json()["id"]
    category2_id = cat2_resp.json()["id"]

    # Create budgets
    client.post(
        "/api/budgets",
        json={
            "category_id": category1_id,
            "amount_limit": 500.00,
        },
    )
    client.post(
        "/api/budgets",
        json={
            "category_id": category2_id,
            "amount_limit": 300.00,
        },
    )

    resp = client.get("/api/budgets?sort_by=id&sort_dir=desc")
    data = resp.json()
    assert len(data["items"]) == 2
    # Most recent first
    assert data["items"][0]["category_id"] == category2_id


def test_delete_budget(client):
    # Create category and budget
    cat_resp = client.post("/api/categories", json={"name": "Groceries"})
    category_id = cat_resp.json()["id"]

    resp = client.post(
        "/api/budgets",
        json={
            "category_id": category_id,
            "amount_limit": 500.00,
        },
    )
    budget_id = resp.json()["id"]

    # Delete budget
    resp = client.delete(f"/api/budgets/{budget_id}")
    assert resp.status_code == 204

    # Verify deleted
    resp = client.get("/api/budgets")
    assert resp.json()["total"] == 0


def test_delete_budget_not_found(client):
    resp = client.delete("/api/budgets/9999")
    assert resp.status_code == 404
