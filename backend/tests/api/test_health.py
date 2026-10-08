def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200


def test_health_returns_employee_count(client):
    response = client.get("/health")
    data = response.json()
    assert data["status"] == "ok"
    assert data["employee_count"] == 0
