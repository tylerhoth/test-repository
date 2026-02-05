def test_dashboard_summary_empty(client):
    resp = client.get("/api/dashboard/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_income"] == 0.0
    assert data["total_expenses"] == 0.0
    assert data["net_savings"] == 0.0
    assert data["savings_rate"] == 0.0
    assert data["transaction_count"] == 0
    assert data["account_count"] == 0


def test_dashboard_summary_with_transactions(client):
    # Create income and expense transactions
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Payroll",
            "amount": 5000.00,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-16",
            "description": "Rent",
            "amount": -1500.00,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-17",
            "description": "Groceries",
            "amount": -200.00,
        },
    )

    resp = client.get("/api/dashboard/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_income"] == 5000.00
    assert data["total_expenses"] == 1700.00
    assert data["net_savings"] == 3300.00
    assert data["savings_rate"] == 66.0
    assert data["transaction_count"] == 3


def test_dashboard_summary_with_account(client):
    # Create account
    client.post(
        "/api/accounts",
        json={
            "name": "Checking",
            "institution": "Bank",
            "account_type": "checking",
        },
    )

    resp = client.get("/api/dashboard/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["account_count"] == 1


def test_spending_by_category_empty(client):
    resp = client.get("/api/dashboard/spending-by-category")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total_expenses"] == 0.0


def test_spending_by_category_with_transactions(client):
    # Create categories
    cat1_resp = client.post("/api/categories", json={"name": "Groceries"})
    cat2_resp = client.post("/api/categories", json={"name": "Dining"})
    category1_id = cat1_resp.json()["id"]
    category2_id = cat2_resp.json()["id"]

    # Create expense transactions
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Grocery Store",
            "amount": -100.00,
            "category_id": category1_id,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-16",
            "description": "Another Grocery",
            "amount": -50.00,
            "category_id": category1_id,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-17",
            "description": "Restaurant",
            "amount": -75.00,
            "category_id": category2_id,
        },
    )

    resp = client.get("/api/dashboard/spending-by-category")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_expenses"] == 225.00
    assert len(data["items"]) == 2

    # Check Groceries category
    groceries = next(item for item in data["items"] if item["category_name"] == "Groceries")
    assert groceries["total"] == 150.00
    assert groceries["transaction_count"] == 2
    assert groceries["percentage"] > 0

    # Check Dining category
    dining = next(item for item in data["items"] if item["category_name"] == "Dining")
    assert dining["total"] == 75.00
    assert dining["transaction_count"] == 1


def test_spending_by_category_uncategorized(client):
    # Create transaction without category
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "Uncategorized",
            "amount": -50.00,
        },
    )

    resp = client.get("/api/dashboard/spending-by-category")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 1
    assert data["items"][0]["category_name"] == "Uncategorized"
    assert data["items"][0]["category_id"] is None
    assert data["items"][0]["total"] == 50.00


def test_income_vs_expenses_empty(client):
    resp = client.get("/api/dashboard/income-vs-expenses")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []


def test_income_vs_expenses_with_transactions(client):
    # Create transactions in different months
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-15",
            "description": "January Income",
            "amount": 5000.00,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-01-16",
            "description": "January Expense",
            "amount": -1000.00,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-02-15",
            "description": "February Income",
            "amount": 5500.00,
        },
    )
    client.post(
        "/api/transactions",
        json={
            "date": "2026-02-16",
            "description": "February Expense",
            "amount": -1200.00,
        },
    )

    resp = client.get("/api/dashboard/income-vs-expenses")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) == 2

    # Check January
    jan = next(item for item in data["items"] if item["month"] == "2026-01")
    assert jan["income"] == 5000.00
    assert jan["expenses"] == 1000.00
    assert jan["net"] == 4000.00

    # Check February
    feb = next(item for item in data["items"] if item["month"] == "2026-02")
    assert feb["income"] == 5500.00
    assert feb["expenses"] == 1200.00
    assert feb["net"] == 4300.00


def test_recurring_charges_empty(client):
    resp = client.get("/api/dashboard/recurring")
    assert resp.status_code == 200
    data = resp.json()
    assert data["items"] == []
    assert data["total_monthly_recurring"] == 0.0


def test_recurring_charges_with_recurring_transactions(client):
    # Create category
    cat_resp = client.post("/api/categories", json={"name": "Subscriptions"})
    category_id = cat_resp.json()["id"]

    # Create recurring transactions (Netflix example)
    for i in range(3):
        txn_resp = client.post(
            "/api/transactions",
            json={
                "date": f"2026-0{i + 1}-15",
                "description": "Netflix Subscription",
                "amount": -15.99,
                "category_id": category_id,
            },
        )
        # Mark as recurring
        txn_id = txn_resp.json()["id"]
        client.put(
            f"/api/transactions/{txn_id}",
            json={"is_recurring": True},
        )

    resp = client.get("/api/dashboard/recurring")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["items"]) >= 1
    assert data["total_monthly_recurring"] > 0.0

    # Check for Netflix
    netflix = next((item for item in data["items"] if "Netflix" in item["description"]), None)
    if netflix:
        assert netflix["occurrences"] == 3
        assert netflix["average_amount"] == 15.99
        assert netflix["category_name"] == "Subscriptions"


def test_recurring_charges_detection(client):
    # Create multiple similar transactions to test auto-detection
    for i in range(4):
        client.post(
            "/api/transactions",
            json={
                "date": f"2026-0{i + 1}-15",
                "description": "Spotify Premium",
                "amount": -9.99,
            },
        )

    resp = client.get("/api/dashboard/recurring")
    assert resp.status_code == 200
    data = resp.json()
    # Should detect Spotify as recurring
    spotify = next((item for item in data["items"] if "Spotify" in item["description"]), None)
    if spotify:
        assert spotify["occurrences"] >= 4
        assert spotify["frequency"] in ["monthly", "weekly", "yearly"]
