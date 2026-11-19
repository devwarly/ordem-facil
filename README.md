# OrdemFácil

Sistema web multiempresa de gerenciamento de ordens de serviço (MVP).

## Status

Fases 0, 1 e 2 concluídas: base da API FastAPI e fundação multiempresa com `companies`, `users`, contexto autenticado, repositório escopado e testes negativos de isolamento. Implantação documentada na Fase 13 (TASK-115…120).

## Documentação

- `docs/requirements.md` — requisitos funcionais, regras de negócio e decisões de produto.
- `docs/spec.md` — arquitetura, modelo de dados, API e decisões técnicas (§20).
- `docs/design.md` — UX/UI, componentes e padrões de interface.
- `docs/tasks.md` — backlog ordenado por fases e Definition of Done (§19).
- `docs/acceptance.md` — critérios de aceite e massa de teste (§3).
- `AGENTS.md` — orientações para sessões de agente neste repositório.

## Estrutura

```text
backend/
  app/{core,database,models,schemas,routes,services,repositories}/
  alembic/versions/
  tests/
  .env.example
  requirements.txt
frontend/
  assets/{css,js,images}/
  pages/
  components/
docs/
```

## Execução local (backend)

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\alembic.exe upgrade head
.\.venv\Scripts\uvicorn.exe app.main:app --reload
```

Ajuste `DATABASE_URL` e `SECRET_KEY` no `.env` antes de rodar as migrations.

- Health check: `GET http://127.0.0.1:8000/health`.
- OpenAPI: `http://127.0.0.1:8000/docs` (disponível com `APP_DEBUG=true`).
- Testes: `.\.venv\Scripts\python.exe -m pytest`.
- Teste de conexão com PostgreSQL: configure `DATABASE_TEST_URL`, rode `.\.venv\Scripts\alembic.exe upgrade head` nesse banco e execute `$env:RUN_DB_TESTS="1"; .\.venv\Scripts\python.exe -m pytest -m integration`. Esse grupo valida migrations, índice de e-mail e FK composta entre empresas; sem PostgreSQL/Docker ativo, permanece ignorado.

## Isolamento multiempresa

- `company_id` é sempre obtido da identidade autenticada (`app/core/tenant.py`); valores enviados pelo cliente são ignorados.
- Consultas e alterações passam por `app/repositories/base.py`, que filtra por `company_id` e responde `404` genérico para registros de outras empresas.
- `app/database/base.py` fornece FKs compostas `(company_id, id)` para impedir associações entre empresas.
- Testes unitários usam SQLite apenas para lógica de escopo; testes de integração com constraints e migrations exigem PostgreSQL real (marker `integration`).

## Decisões fechadas no MVP

- Multiempresa com isolamento lógico por `company_id`; um usuário pertence a uma única empresa.
- Backend valida permissões e regras de negócio; Perfis: `ADMIN`, `ATTENDANT` e `TECHNICIAN`.
- Autenticação: JWT de 30 minutos + refresh token opaco e revogável; senhas com Argon2id.
- Frontend em HTML, CSS e JavaScript puro, sem framework.
- Auto cadastro de empresas habilitado, com limite de requisições por IP.
- No máximo um técnico responsável por OS; numeração por empresa com bloqueio de linha.
- Homologação em VPS com Docker Compose, HTTPS e backup via `pg_dump`.

## Pré-requisitos planejados

- Python 3.13 ou superior.
- PostgreSQL (desenvolvimento, teste e produção).
- Dependências fixadas em `backend/requirements.txt`.
