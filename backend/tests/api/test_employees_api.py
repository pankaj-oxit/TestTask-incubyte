import pytest

SAMPLE = {
    "employee_code": "EMP-000001",
    "first_name": "Jane",
    "last_name": "Doe",
    "email": "jane.doe@acme.com",
    "job_title": "Engineer",
    "department": "Engineering",
    "country_code": "US",
    "currency": "USD",
    "annual_salary": 95000,
    "hire_date": "2020-01-15",
}


def test_create_employee_returns_201(client):
    response = client.post("/api/employees", json=SAMPLE)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == SAMPLE["email"]
    assert data["id"] is not None


def test_get_employee(client):
    created = client.post("/api/employees", json=SAMPLE).json()
    response = client.get(f"/api/employees/{created['id']}")
    assert response.status_code == 200
    assert response.json()["employee_code"] == SAMPLE["employee_code"]


def test_get_employee_not_found(client):
    assert client.get("/api/employees/99999").status_code == 404


def test_duplicate_email_returns_409(client):
    client.post("/api/employees", json=SAMPLE)
    dup = {**SAMPLE, "employee_code": "EMP-000002"}
    assert client.post("/api/employees", json=dup).status_code == 409


def test_update_employee(client):
    created = client.post("/api/employees", json=SAMPLE).json()
    updated = {**SAMPLE, "annual_salary": 100000, "email": created["email"]}
    response = client.put(f"/api/employees/{created['id']}", json=updated)
    assert response.status_code == 200
    assert response.json()["annual_salary"] == 100000


def test_delete_employee(client):
    created = client.post("/api/employees", json=SAMPLE).json()
    assert client.delete(f"/api/employees/{created['id']}").status_code == 204
    assert client.get(f"/api/employees/{created['id']}").status_code == 404


def test_list_pagination(client):
    for i in range(3):
        payload = {**SAMPLE, "employee_code": f"EMP-{i:06d}", "email": f"user{i}@acme.com"}
        client.post("/api/employees", json=payload)
    data = client.get("/api/employees?page=1&page_size=2").json()
    assert data["total"] == 3
    assert len(data["items"]) == 2
    assert data["page"] == 1


def test_list_search_by_name(client):
    client.post("/api/employees", json=SAMPLE)
    other = {**SAMPLE, "employee_code": "EMP-000002", "email": "bob@acme.com", "first_name": "Bob"}
    client.post("/api/employees", json=other)
    data = client.get("/api/employees?search=jane").json()
    assert data["total"] == 1
    assert data["items"][0]["first_name"] == "Jane"


def test_list_filter_country(client):
    client.post("/api/employees", json=SAMPLE)
    uk = {**SAMPLE, "employee_code": "EMP-UK-01", "email": "uk@acme.com", "country_code": "GB", "currency": "GBP"}
    client.post("/api/employees", json=uk)
    data = client.get("/api/employees?country=US").json()
    assert data["total"] == 1
    assert data["items"][0]["country_code"] == "US"


def test_invalid_sort_by_rejected(client):
    assert client.get("/api/employees?sort_by=invalid_column").status_code == 422


def test_page_size_over_max_rejected(client):
    assert client.get("/api/employees?page_size=101").status_code == 422


def test_negative_salary_rejected(client):
    bad = {**SAMPLE, "annual_salary": 0}
    assert client.post("/api/employees", json=bad).status_code == 422


def test_currency_country_mismatch_rejected(client):
    bad = {**SAMPLE, "country_code": "US", "currency": "EUR"}
    assert client.post("/api/employees", json=bad).status_code == 422
