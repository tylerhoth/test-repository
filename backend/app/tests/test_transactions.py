import io


def test_create_transaction(client):
    resp = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Grocery Store",
            "amount": -45.67,
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["date"] == "2026-01-15"
    assert data["description"] == "Grocery Store"
    assert data["amount"] == -45.67
    assert data["is_recurring"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_transaction_with_category_and_account(client):
    # Create category and account
    cat_resp = client.post("/api/categories", json={"name": "Groceries"})
    category_id = cat_resp.json()["id"]

    acc_resp = client.post(
        "/api/accounts",
        json={
            "name": "Checking",
            "institution": "Bank",
            "account_type": "checking",
        },
    )
    account_id = acc_resp.json()["id"]

    # Create transaction
    resp = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Grocery Store",
            "amount": -45.67,
            "category_id": category_id,
            "account_id": account_id,
            "tags": "food",
            "notes": "Weekly shopping",
        },
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["category_id"] == category_id
    assert data["account_id"] == account_id
    assert data["tags"] == "food"
    assert data["notes"] == "Weekly shopping"


def test_list_transactions_empty(client):
    resp = client.get("/api/transactions")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total"] == 0
    assert data["page"] == 1
    assert data["page_size"] == 20


def test_list_transactions_with_items(client):
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Transaction 1",
            "amount": -10.00,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-16",
            "description": "Transaction 2",
            "amount": -20.00,
        },
    )
    resp = client.get("/api/transactions")
    data = resp.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_list_transactions_pagination(client):
    for i in range(5):
        client.post(
            "/api/transactions",
            json={
                "date": "2026-01-15",
                "description": f"Transaction {i}",
                "amount": -10.00,
            },
        )
    resp = client.get("/api/transactions?page=1&page_size=2")
    data = resp.json()
    assert data["total"] == 5
    assert len(data["items"]) == 2
    assert data["page"] == 1
    assert data["page_size"] == 2


def test_list_transactions_search(client):
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Grocery Store",
            "amount": -45.67,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-16",
            "description": "Gas Station",
            "amount": -30.00,
        },
    )
    resp = client.get("/api/transactions?q=Grocery")
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["description"] == "Grocery Store"


def test_list_transactions_sort_by_date(client):
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-20",
            "description": "Later",
            "amount": -10.00,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-10",
            "description": "Earlier",
            "amount": -10.00,
        },
    )
    # Default sort is date desc
    resp = client.get("/api/transactions?sort_by=date&sort_dir=desc")
    data = resp.json()
    assert data["items"][0]["description"] == "Later"
    assert data["items"][1]["description"] == "Earlier"


def test_list_transactions_sort_ascending(client):
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-20",
            "description": "Later",
            "amount": -10.00,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-10",
            "description": "Earlier",
            "amount": -10.00,
        },
    )
    resp = client.get("/api/transactions?sort_by=date&sort_dir=asc")
    data = resp.json()
    assert data["items"][0]["description"] == "Earlier"
    assert data["items"][1]["description"] == "Later"


def test_list_transactions_filter_by_account(client):
    acc1_resp = client.post(
        "/api/accounts",
        json={
            "name": "Account 1",
            "institution": "Bank",
            "account_type": "checking",
        },
    )
    acc2_resp = client.post(
        "/api/accounts",
        json={
            "name": "Account 2",
            "institution": "Bank",
            "account_type": "savings",
        },
    )
    account1_id = acc1_resp.json()["id"]
    account2_id = acc2_resp.json()["id"]

    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Txn 1",
            "amount": -10.00,
            "account_id": account1_id,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-16",
            "description": "Txn 2",
            "amount": -20.00,
            "account_id": account2_id,
        },
    )

    resp = client.get(f"/api/transactions?account_id={account1_id}")
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["description"] == "Txn 1"


def test_list_transactions_filter_by_category(client):
    cat1_resp = client.post("/api/categories", json={"name": "Groceries"})
    cat2_resp = client.post("/api/categories", json={"name": "Dining"})
    category1_id = cat1_resp.json()["id"]
    category2_id = cat2_resp.json()["id"]

    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Grocery Store",
            "amount": -45.67,
            "category_id": category1_id,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-16",
            "description": "Restaurant",
            "amount": -30.00,
            "category_id": category2_id,
        },
    )

    resp = client.get(f"/api/transactions?category_id={category1_id}")
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["description"] == "Grocery Store"


def test_list_transactions_filter_by_date_range(client):
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-10",
            "description": "Early",
            "amount": -10.00,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Middle",
            "amount": -20.00,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-20",
            "description": "Late",
            "amount": -30.00,
        },
    )

    resp = client.get("/api/transactions?date_from=2026-01-12&date_to=2026-01-18")
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["description"] == "Middle"


def test_update_transaction(client):
    # Create category
    cat_resp = client.post("/api/categories", json={"name": "Groceries"})
    category_id = cat_resp.json()["id"]

    # Create transaction
    resp = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Store",
            "amount": -45.67,
        },
    )
    txn_id = resp.json()["id"]

    # Update transaction
    resp = client.put(
        f"/api/transactions/{txn_id}",
        json={
            "category_id": category_id,
            "tags": "food,weekly",
            "notes": "Updated notes",
            "is_recurring": True,
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["category_id"] == category_id
    assert data["tags"] == "food,weekly"
    assert data["notes"] == "Updated notes"
    assert data["is_recurring"] is True


def test_update_transaction_not_found(client):
    resp = client.put(
        "/api/transactions/9999",
        json={"category_id": 1},
    )
    assert resp.status_code == 404


def test_delete_transaction(client):
    resp = client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Delete me",
            "amount": -10.00,
        },
    )
    txn_id = resp.json()["id"]

    resp = client.delete(f"/api/transactions/{txn_id}")
    assert resp.status_code == 204

    resp = client.get("/api/transactions")
    assert resp.json()["total"] == 0


def test_delete_transaction_not_found(client):
    resp = client.delete("/api/transactions/9999")
    assert resp.status_code == 404


def test_import_transactions_csv(client):
    csv_content = (
        "Date,Description,Category,Firm Name,Account Name,Amount,Tags\n"
        '"2026-01-15","Grocery Store","Groceries","Wells Fargo",'
        '"Everyday Checking - Ending in 2820","-$45.67",""\n'
        '"2026-01-15","Payroll","Paychecks/Salary","Wells Fargo",'
        '"Everyday Checking - Ending in 2820","$5,700.00",""\n'
        '"2026-01-16","Coffee Shop","Dining Out","Chase",'
        '"Credit Card - Ending in 1234","-$5.50","coffee"\n'
    )

    resp = client.post(
        "/api/transactions/import",
        files={
            "file": (
                "transactions.csv",
                io.BytesIO(csv_content.encode()),
                "text/csv",
            )
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["imported"] == 3
    assert data["skipped"] == 0
    assert data["accounts_created"] >= 0
    assert data["categories_created"] >= 0

    # Verify transactions were created
    resp = client.get("/api/transactions")
    assert resp.json()["total"] == 3


def test_import_transactions_csv_with_header_line(client):
    # Some CSV exports have a header line before the column names
    csv_content = """Transactions For All Accounts
Date,Description,Category,Firm Name,Account Name,Amount,Tags
"2026-01-15","Grocery Store","Groceries","Wells Fargo","Checking","-$45.67",""
"""

    resp = client.post(
        "/api/transactions/import",
        files={
            "file": (
                "transactions.csv",
                io.BytesIO(csv_content.encode()),
                "text/csv",
            )
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["imported"] == 1
