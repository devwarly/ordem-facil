from dataclasses import dataclass
from uuid import UUID

from fastapi import Depends, Request

from app.core.enums import UserRole
from app.core.errors import AppError


@dataclass(frozen=True, slots=True)
class AuthenticatedPrincipal:
    """Identidade validada. Na Fase 3, será preenchida pelo token de acesso."""

    user_id: UUID
    company_id: UUID
    role: UserRole
    email: str | None = None


@dataclass(frozen=True, slots=True)
class TenantContext:
    company_id: UUID
    user_id: UUID
    role: UserRole


def get_current_principal(request: Request) -> AuthenticatedPrincipal:
    """Ponto único de integração com a autenticação da Fase 3.

    Até lá, a identidade é injetada em `request.state.principal` pelos testes.
    Nenhuma rota de negócio deve aceitar `company_id` do cliente.
    """
    principal = getattr(request.state, "principal", None)
    if principal is None:
        raise AppError(401, "UNAUTHORIZED", "Autenticação necessária.")
    if not isinstance(principal, AuthenticatedPrincipal):
        raise AppError(401, "UNAUTHORIZED", "Credencial inválida.")
    return principal


def get_tenant_context(
    principal: AuthenticatedPrincipal = Depends(get_current_principal),
) -> TenantContext:
    return TenantContext(
        company_id=principal.company_id,
        user_id=principal.user_id,
        role=principal.role,
    )


def get_company_id(context: TenantContext = Depends(get_tenant_context)) -> UUID:
    return context.company_id
