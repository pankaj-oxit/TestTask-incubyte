from tests.api.test_employees_api import SAMPLE


def test_meta_filters_lists_distinct_values(client):
    client.post("/api/employees", json=SAMPLE)
    data = client.get("/api/meta/filters").json()
    assert "US" in data["countries"]
    assert "Engineering" in data["departments"]
    assert "Engineer" in data["job_titles"]
