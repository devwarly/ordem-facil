# AGENTS.md — OrdemFácil

## Estado atual

- Fases 0, 1 e 2 prontas: API FastAPI com `/health`, configuração validada, SQLAlchemy, Alembic, erros padronizados, CORS e fundação multiempresa (`companies`/`users`, contexto autenticado, repositório escopado e FKs compostas). Comandos no `README.md`.
- `docs/` é a fonte de verdade nesta fase: `requirements.md` → `spec.md` → `design.md` → `tasks.md` → `acceptance.md`. Consulte-os antes de implementar cada módulo (`tasks.md` §2).
- `tasks.md` é o backlog ordenado (TASK-001…121). As Fases 0, 1 e 2 estão concluídas; siga a ordem das fases e marque `[x]` somente após implementação **e** validação.
- Decisões fechadas em `spec.md` §20 e `requirements.md` §12: JWT + refresh revogável, frontend puro, auto cadastro habilitado, uma empresa por usuário, um técnico por OS, VPS com Docker Compose. Não reabri-las sem atualizar os docs.

## Regras bloqueantes

- **Isolamento multiempresa já implementado na Fase 2, mas obrigatório em todo módulo novo** (TASK-014…021). `company_id` sempre derivado do usuário autenticado (`app/core/tenant.py`); nunca aceite `company_id` enviado pelo cliente. Use `app/repositories/base.py` e FKs compostas (`app/database/base.py`). Acesso cruzado é negado como "não encontrado", sem revelar que o registro existe.
- Backend valida permissões e regras de negócio em toda operação protegida; frontend apenas oculta ações. Perfis: `ADMIN`, `ATTENDANT`, `TECHNICIAN`.
- Técnico consulta e atualiza somente OS atribuídas a ele.
- Número da OS: sequência/transação por empresa, único dentro da empresa e seguro sob concorrência. **Nunca** gere com `COUNT()` de registros.
- Máquina de estados: `OPEN` → `IN_PROGRESS` ↔ `WAITING` → `COMPLETED`; `OPEN|IN_PROGRESS|WAITING` → `CANCELED`. `COMPLETED` e `CANCELED` são finais (sem reabertura no MVP). Conclusão exige `resolution`; cancelamento exige `cancellation_reason`. Valide no serviço de domínio, não na interface.
- Clientes e fornecedores com histórico são **inativados** (`is_active`), nunca excluídos fisicamente.
- MVP: usuário pertence a uma única empresa, e-mail de login é único globalmente, uma OS tem no máximo um técnico.
- Fora do escopo do MVP (não implementar sem atualizar os docs): app nativo, NF-e, WhatsApp, pagamentos/financeiro, estoque, relatórios avançados, PDF, anexos, operação offline.

## Stack e convenções

- Backend: FastAPI, SQLAlchemy, Alembic, Pydantic, Uvicorn, PostgreSQL, Pytest — versões fixadas em `backend/requirements.txt`; layout em `backend/app/{core,database,models,schemas,routes,services,repositories}`, `backend/alembic/`, `backend/tests/`.
- Frontend: HTML/CSS/JavaScript puro em `frontend/`, consumindo API JSON com prefixo `/api/v1`.
- Toda alteração de schema exige migration Alembic. `.env` não é versionado; `.env.example` contém apenas valores fictícios.
- Interface em pt-BR: datas `DD/MM/AAAA`, horas em 24h, valores em R$. Termos canônicos: "Ordem de Serviço"/"OS", "Cliente", "Fornecedor", "Técnico", "Status".
- `acceptance.md` §3 define a massa de teste (Empresas A/B, cinco usuários) e os critérios de acesso cruzado — use-a nos testes de isolamento.

## Antes de marcar uma tarefa como concluída

Ver `tasks.md` §19 e `acceptance.md`: implementar, testar (incluindo testes negativos de isolamento), atualizar a documentação relevante e só então marcar `[x]`.
