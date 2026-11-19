from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.core.errors import AppError
from app.database.session import get_db
from app.main import create_app


def build_client() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_db] = lambda: object()

    @app.get("/_test/validation")
    def validation(q: int):
        return {"q": q}

    @app.get("/_test/not-found")
    def not_found():
        raise HTTPException(status_code=404, detail="Recurso não encontrado")

    @app.get("/_test/conflict")
    def conflict():
        raise AppError(status_code=409, code="CONFLICT", message="Já existe um registro.")

    @app.get("/_test/boom")
    def boom():
        raise RuntimeError("detalhe interno sigiloso")

    return TestClient(app, raise_server_exceptions=False)


def test_validation_error_format():
    response = build_client().get("/_test/validation", params={"q": "abc"})

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert detail["code"] == "VALIDATION_ERROR"
    assert "q" in detail["fields"]


def test_http_error_format():
    response = build_client().get("/_test/not-found")

    assert response.status_code == 404
    assert response.json()["detail"] == {
        "code": "NOT_FOUND",
        "message": "Recurso não encontrado",
    }


def test_app_error_format():
    response = build_client().get("/_test/conflict")

    assert response.status_code == 409
    assert response.json()["detail"]["code"] == "CONFLICT"


def test_unexpected_error_does_not_leak_details():
    response = build_client().get("/_test/boom")

    assert response.status_code == 500
    assert response.json()["detail"]["code"] == "INTERNAL_ERROR"
    assert "detalhe interno sigiloso" not in response.text
