from uuid import uuid4

from fastapi import Depends
from fastapi.testclient import TestClient

from app.core.enums import UserRole
from app.core.tenant import (
    AuthenticatedPrincipal,
    TenantContext,
    get_current_principal,
    get_tenant_context,
)
from app.main import create_app


def test_company_id_comes_from_principal_not_from_request():
    company_a = uuid4()
    company_b = uuid4()
    principal = AuthenticatedPrincipal(
        user_id=uuid4(), company_id=company_a, role=UserRole.ADMIN
    )
    app = create_app()
    app.dependency_overrides[get_current_principal] = lambda: principal

    @app.get("/_test/context")
    def context(
        company_id: str, context: TenantContext = Depends(get_tenant_context)
    ) -> dict[str, str]:
        return {
            "company_id": str(context.company_id),
            "user_id": str(context.user_id),
            "role": context.role.value,
            "query_company_id": company_id,
        }

    response = TestClient(app).get(
        "/_test/context", params={"company_id": str(company_b)}
    )

    assert response.status_code == 200
    body = response.json()
    assert body["company_id"] == str(company_a)
    assert body["query_company_id"] == str(company_b)
    assert body["role"] == "ADMIN"


def test_missing_principal_returns_401():
    app = create_app()

    @app.get("/_test/protected")
    def protected(context: TenantContext = Depends(get_tenant_context)) -> dict[str, str]:
        return {"company_id": str(context.company_id)}

    response = TestClient(app).get("/_test/protected")

    assert response.status_code == 401
    assert response.json()["detail"] == {
        "code": "UNAUTHORIZED",
        "message": "Autenticação necessária.",
    }
