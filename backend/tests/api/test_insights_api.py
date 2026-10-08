def _create(client, **overrides):
    payload = {
        "employee_code": overrides.pop("employee_code", "EMP-INS-01"),
        "first_name": "A",
        "last_name": "One",
        "email": overrides.pop("email", "a1@acme.com"),
        "job_title": overrides.pop("job_title", "Engineer"),
        "department": "Engineering",
        "country_code": "US",
        "currency": "USD",
        "annual_salary": overrides.pop("annual_salary", 100_000),
        "hire_date": "2020-01-01",
        **overrides,
    }
    client.post("/api/employees", json=payload)


def test_insights_summary_usd(client):
    _create(client, employee_code="E1", email="s1@acme.com", annual_salary=100_000)
    _create(
        client,
        employee_code="E2",
        email="s2@acme.com",
        country_code="IN",
        currency="INR",
        annual_salary=1_000_000,
    )
    data = client.get("/api/insights/summary").json()
    assert data["headcount"] == 2
    assert data["average_salary_usd"] == 56_000.0
    assert data["median_salary_usd"] == 56_000.0


def test_insights_by_country(client):
    _create(client, employee_code="C1", email="c1@acme.com", country_code="US", annual_salary=80_000)
    _create(
        client,
        employee_code="C2",
        email="c2@acme.com",
        country_code="GB",
        currency="GBP",
        annual_salary=50_000,
    )
    rows = client.get("/api/insights/by-country").json()
    by_code = {r["country_code"]: r for r in rows}
    assert by_code["US"]["headcount"] == 1
    assert by_code["US"]["average_salary_local"] == 80_000
    assert by_code["US"]["average_salary_usd"] == 80_000.0
    assert by_code["GB"]["median_salary_usd"] == round(50_000 * 1.27, 2)


def test_insights_by_country_filter_query_param(client):
    _create(client, employee_code="CF1", email="cf1@acme.com", country_code="US", annual_salary=80_000)
    _create(
        client,
        employee_code="CF2",
        email="cf2@acme.com",
        country_code="GB",
        currency="GBP",
        annual_salary=50_000,
    )
    rows = client.get("/api/insights/by-country?country=US").json()
    assert len(rows) == 1
    assert rows[0]["country_code"] == "US"
    assert rows[0]["headcount"] == 1


def test_insights_by_job_title_filter_query_param(client):
    _create(client, employee_code="J1", email="j1@acme.com", job_title="Engineer", annual_salary=90_000)
    _create(
        client,
        employee_code="J2",
        email="j2@acme.com",
        job_title="Manager",
        annual_salary=110_000,
    )
    rows = client.get("/api/insights/by-job-title?job_title=Engineer").json()
    assert len(rows) == 1
    assert rows[0]["job_title"] == "Engineer"
    assert rows[0]["average_salary_usd"] == 90_000.0


def test_insights_by_job_title_optional_country_scope(client):
    _create(client, employee_code="JS1", email="js1@acme.com", job_title="Engineer", country_code="US", annual_salary=90_000)
    _create(
        client,
        employee_code="JS2",
        email="js2@acme.com",
        job_title="Engineer",
        country_code="GB",
        currency="GBP",
        annual_salary=60_000,
    )
    rows = client.get("/api/insights/by-job-title?job_title=Engineer&country=US").json()
    assert len(rows) == 1
    assert rows[0]["job_title"] == "Engineer"
    assert rows[0]["headcount"] == 1
    assert rows[0]["average_salary_usd"] == 90_000.0


def test_insights_distribution_buckets_sum_to_headcount(client):
    _create(client, employee_code="D1", email="d1@acme.com", annual_salary=50_000)
    _create(client, employee_code="D2", email="d2@acme.com", annual_salary=150_000)
    data = client.get("/api/insights/distribution").json()
    assert len(data["buckets"]) == 10
    assert sum(b["count"] for b in data["buckets"]) == 2


def test_insights_distribution_filtered_by_job_title(client):
    _create(client, employee_code="DF1", email="df1@acme.com", job_title="Engineer", annual_salary=50_000)
    _create(client, employee_code="DF2", email="df2@acme.com", job_title="Manager", annual_salary=150_000)
    data = client.get("/api/insights/distribution?job_title=Engineer").json()
    assert data["headcount"] == 1
    assert sum(b["count"] for b in data["buckets"]) == 1
