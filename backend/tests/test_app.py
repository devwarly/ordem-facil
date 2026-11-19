def test_health_returns_ok(client, fake_db):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert fake_db.executed == ["SELECT 1"]


def test_openapi_available_in_development(client):
    response = client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"]["title"] == "OrdemFacil"


def test_cors_allows_configured_origin(client):
    response = client.get("/health", headers={"Origin": "http://localhost:5500"})

    assert response.headers["access-control-allow-origin"] == "http://localhost:5500"


def test_cors_rejects_unknown_origin(client):
    response = client.get("/health", headers={"Origin": "https://externo.example"})

    assert "access-control-allow-origin" not in response.headers
