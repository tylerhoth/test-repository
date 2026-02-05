def test_create_account(client):
    resp = client.post(
        "/api/accounts",
        json={
            "name": "Everyday Checking",
            "institution": "Wells Fargo",
            "account_type": "checking",
            "last_four": "2820",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Everyday Checking"
    assert data["institution"] == "Wells Fargo"
    assert data["account_type"] == "checking"
    assert data["last_four"] == "2820"
    assert "id" in data
    assert "created_at" in data


def test_create_account_minimal(client):
    resp = client.post(
        "/api/accounts",
        json={
            "name": "Savings",
            "institution": "Chase",
            "account_type": "savings",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Savings"
    assert data["last_four"] is None


def test_list_accounts_empty(client):
    resp = client.get("/api/accounts")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["page_size"] == 20


def test_list_accounts_with_items(client):
    client.post(
        "/api/accounts",
        json={
            "name": "Checking",
            "institution": "Bank A",
            "account_type": "checking",
        },
    )
    client.post(
        "/api/accounts",
        json={
            "name": "Savings",
            "institution": "Bank B",
            "account_type": "savings",
        },
    )
    resp = client.get("/api/accounts")
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_list_accounts_pagination(client):
    for i in range(5):
        client.post(
            "/api/accounts",
            json={
                "name": f"Account {i}",
                "institution": "Bank",
                "account_type": "checking",
            },
        )
    resp = client.get("/api/accounts?page=1&page_size=2")
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["page_size"] == 2


def test_list_accounts_search(client):
    client.post(
        "/api/accounts",
        json={
            "name": "Wells Fargo Checking",
            "institution": "Wells Fargo",
            "account_type": "checking",
        },
    )
    client.post(
        "/api/accounts",
        json={
            "name": "Chase Savings",
            "institution": "Chase",
            "account_type": "savings",
        },
    )
    resp = client.get("/api/accounts?q=Wells")
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["name"] == "Wells Fargo Checking"


def test_list_accounts_sort_by_name(client):
    client.post(
        "/api/accounts",
        json={
            "name": "Zebra Account",
            "institution": "Bank",
            "account_type": "checking",
        },
    )
    client.post(
        "/api/accounts",
        json={
            "name": "Alpha Account",
            "institution": "Bank",
            "account_type": "savings",
        },
    )
    resp = client.get("/api/accounts?sort_by=name&sort_dir=asc")
    data = resp.json()
    assert data["items"][0]["name"] == "Alpha Account"
    assert data["items"][1]["name"] == "Zebra Account"


def test_list_accounts_sort_descending(client):
    client.post(
        "/api/accounts",
        json={
            "name": "First",
            "institution": "Bank",
            "account_type": "checking",
        },
    )
    client.post(
        "/api/accounts",
        json={
            "name": "Second",
            "institution": "Bank",
            "account_type": "savings",
        },
    )
    resp = client.get("/api/accounts?sort_by=name&sort_dir=desc")
    data = resp.json()
    assert data["items"][0]["name"] == "Second"
    assert data["items"][1]["name"] == "First"
