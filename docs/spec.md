# Technical Specification — OrdemFácil

**Projeto:** OrdemFácil — Sistema Web de Gerenciamento de Ordens de Serviço  
**Versão:** 1.2  
**Documento de referência:** `requirements.md`  
**Status:** Especificação técnica do MVP com decisões registradas e fundação multiempresa implementada

---

## 1. Objetivo deste documento

Este documento descreve a arquitetura, os componentes, os módulos, o modelo de dados, as interfaces da API, as regras técnicas e as diretrizes de implementação do OrdemFácil.

O objetivo é orientar o desenvolvimento do MVP de forma consistente com os requisitos funcionais e não funcionais definidos em `requirements.md`.

Este documento não substitui os requisitos. Em caso de divergência, os requisitos aprovados devem ser revisados antes da implementação.

## 2. Visão técnica do produto

O OrdemFácil será uma aplicação web composta por três camadas principais:

1. **Frontend:** interface acessada pelo navegador, desenvolvida com HTML, CSS e JavaScript.
2. **Backend:** API REST desenvolvida em Python com FastAPI, responsável por autenticação, validações e regras de negócio.
3. **Banco de dados:** PostgreSQL, responsável pelo armazenamento persistente das informações.

A comunicação entre frontend e backend será realizada por HTTP, utilizando JSON. A API deverá disponibilizar documentação OpenAPI por meio dos recursos nativos do FastAPI.

### 2.1 Arquitetura lógica

```text
┌──────────────────────────────────────────────┐
│                 Navegador                    │
│          HTML + CSS + JavaScript             │
└──────────────────────┬───────────────────────┘
                       │ HTTP / JSON
                       ▼
┌──────────────────────────────────────────────┐
│                API REST                      │
│                  FastAPI                     │
│                                              │
│  Rotas → Serviços → Regras de negócio        │
│                    ↓                         │
│              Repositórios / ORM              │
└──────────────────────┬───────────────────────┘
                       │ SQL
                       ▼
┌──────────────────────────────────────────────┐
│                 PostgreSQL                   │
│                                              │
│ Empresas | Usuários | Clientes | Fornecedores│
│       OS | Histórico de OS                   │
└──────────────────────────────────────────────┘
```

### 2.2 Diretrizes arquiteturais

- Manter frontend e backend desacoplados.
- Concentrar regras de negócio no backend.
- Não confiar em validações realizadas somente no navegador.
- Organizar o backend por módulos de domínio.
- Utilizar transações nas operações que alterem múltiplas tabelas.
- Padronizar respostas e erros da API.
- Utilizar migrations para controlar a evolução do banco de dados.
- Não armazenar senhas, tokens ou segredos no código-fonte.

## 3. Premissas técnicas do MVP

Para viabilizar a primeira versão, serão adotadas as seguintes premissas provisórias:

- O MVP será multiempresa: várias empresas utilizarão a mesma instalação da plataforma.
- Os dados de cada empresa deverão permanecer isolados logicamente.
- Cada usuário pertencerá a uma empresa no MVP. A possibilidade de um usuário participar de várias empresas poderá ser avaliada futuramente.
- O sistema terá os perfis Administrador, Atendente e Técnico, sempre vinculados ao contexto da empresa.
- Uma ordem de serviço terá, inicialmente, um único técnico responsável.
- O número da OS será gerado automaticamente pelo backend.
- Clientes e fornecedores serão inativados, em vez de excluídos fisicamente quando houver histórico relacionado.
- A interface será responsiva, mas não será desenvolvido aplicativo mobile nativo.
- Anexos, geração de PDF, integrações externas e controle financeiro não fazem parte da primeira entrega.

**Decisão confirmada:** o OrdemFácil será multiempresa. O isolamento deverá ser implementado desde a primeira versão, incluindo `company_id` nas entidades pertencentes a uma empresa e validação obrigatória do contexto empresarial em todas as operações. Não será suficiente filtrar os dados apenas na interface.

## 4. Stack tecnológica

| Camada | Tecnologia | Uso |
|---|---|---|
| Frontend | HTML5 | Estrutura das páginas |
| Frontend | CSS3 | Estilos e responsividade |
| Frontend | JavaScript | Interatividade e consumo da API |
| Backend | Python | Linguagem principal |
| Backend | FastAPI | API REST |
| Persistência | PostgreSQL | Banco de dados relacional |
| ORM | SQLAlchemy | Mapeamento objeto-relacional |
| Migrations | Alembic | Versionamento do esquema do banco |
| Validação | Pydantic | Validação de entrada e saída |
| Servidor ASGI | Uvicorn | Execução da aplicação FastAPI |
| Testes | Pytest | Testes automatizados do backend |

As versões das dependências deverão ser fixadas em arquivo de dependências e atualizadas de forma controlada.

## 5. Organização do projeto

Estrutura sugerida para o repositório:

```text
ordemfacil/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── security.py
│   │   │   └── permissions.py
│   │   ├── database/
│   │   │   ├── session.py
│   │   │   └── base.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── customer.py
│   │   │   ├── supplier.py
│   │   │   ├── service_order.py
│   │   │   └── service_order_history.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── customer.py
│   │   │   ├── supplier.py
│   │   │   ├── service_order.py
│   │   │   └── dashboard.py
│   │   ├── routes/
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── customers.py
│   │   │   ├── suppliers.py
│   │   │   ├── service_orders.py
│   │   │   └── dashboard.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── user_service.py
│   │   │   ├── customer_service.py
│   │   │   ├── supplier_service.py
│   │   │   ├── service_order_service.py
│   │   │   └── dashboard_service.py
│   │   └── repositories/
│   │       ├── customer_repository.py
│   │       ├── supplier_repository.py
│   │       └── service_order_repository.py
│   │
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── index.html
│   ├── assets/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── pages/
│   └── components/
│
├── docs/
│   ├── requirements.md
│   ├── spec.md
│   ├── design.md
│   ├── tasks.md
│   └── acceptance.md
│
├── .gitignore
└── README.md
```

A estrutura poderá ser ajustada durante a implementação, desde que a separação de responsabilidades seja preservada.

## 6. Módulos do sistema

### 6.1 Autenticação e usuários

Responsável por autenticar usuários e controlar permissões.

**Responsabilidades:**
- Login e logout.
- Identificação do usuário autenticado.
- Gerenciamento de usuários pelo administrador.
- Associação de perfil ao usuário.
- Bloqueio de usuários inativos.
- Proteção de rotas e operações.

**Perfis:**

| Perfil | Permissões gerais |
|---|---|
| Administrador | Acesso completo e gerenciamento de usuários |
| Atendente | Clientes, fornecedores e gerenciamento operacional de OS |
| Técnico | Consulta e atualização das OS atribuídas |

O backend deverá verificar o perfil e a relação do técnico com a OS em cada operação protegida.

### 6.2 Clientes

Responsável pelo cadastro e gerenciamento dos clientes.

**Operações:**
- Criar cliente.
- Listar e pesquisar clientes.
- Consultar detalhes.
- Atualizar cadastro.
- Inativar cadastro.

**Validações:**
- Nome ou razão social obrigatório.
- Tipo de pessoa obrigatório: física ou jurídica.
- CPF/CNPJ, quando informado, deverá ser validado e normalizado.
- E-mail deverá respeitar formato válido, quando informado.
- Telefone deverá aceitar formatação nacional.
- Não permitir duplicidade de CPF/CNPJ entre cadastros ativos, quando o documento for informado.

### 6.3 Fornecedores

Responsável pelo cadastro e consulta de fornecedores.

**Operações:**
- Criar fornecedor.
- Listar e pesquisar fornecedores.
- Consultar detalhes.
- Atualizar cadastro.
- Inativar cadastro.

O cadastro deverá aceitar nome ou razão social, documento quando aplicável, contato, telefone, e-mail, endereço e observações.

### 6.4 Ordens de serviço

Módulo central do sistema.

**Operações:**
- Abrir ordem de serviço.
- Gerar número único.
- Vincular cliente.
- Atribuir técnico.
- Consultar e filtrar ordens.
- Editar informações permitidas.
- Atualizar status.
- Registrar observações técnicas.
- Registrar solução aplicada.
- Cancelar ordem com justificativa.
- Consultar histórico.

**Dados principais da OS:**
- Identificador interno.
- Número público da OS.
- Cliente.
- Técnico responsável.
- Descrição da solicitação.
- Serviço solicitado.
- Observações.
- Status.
- Data/hora de abertura.
- Data/hora de conclusão, quando aplicável.
- Solução aplicada, quando concluída.
- Usuário que abriu a ordem.

### 6.5 Dashboard

O dashboard deverá apresentar, no mínimo:

- Total de ordens abertas.
- Total de ordens em andamento.
- Total de ordens aguardando.
- Total de ordens concluídas.
- Total de ordens canceladas.
- Ordens abertas recentemente.

Os indicadores deverão ser calculados a partir dos dados persistidos no banco. Os números exibidos deverão respeitar o escopo de acesso do usuário.

### 6.6 Matriz de permissões do MVP

| Operação | Administrador | Atendente | Técnico |
|---|---|---|---|
| Gerenciar usuários e dados da empresa | Sim | Não | Não |
| Criar e editar clientes e fornecedores | Sim | Sim | Não |
| Inativar clientes e fornecedores | Sim | Não | Não |
| Abrir OS, atribuir técnico e editar campos operacionais | Sim | Sim | Não |
| Consultar OS da empresa | Sim | Sim | Somente as atribuídas |
| Registrar observação técnica e solução | Sim | Não | Somente nas atribuídas |
| Atualizar status conforme transições permitidas | Sim | Sim | Somente nas atribuídas |
| Cancelar OS com justificativa | Sim | Não | Não |
| Dashboard (resumo e ordens recentes) | Sim | Sim | Não |

Toda operação é validada no backend; a interface apenas oculta ações não permitidas.

## 7. Arquitetura multiempresa

O OrdemFácil será uma plataforma multiempresa (multi-tenant), na qual várias empresas utilizarão a mesma aplicação e a mesma infraestrutura de banco de dados, mantendo seus dados isolados logicamente.

### 7.1 Estratégia inicial

O MVP utilizará banco de dados compartilhado e tabelas compartilhadas, com uma coluna `company_id` nas entidades pertencentes a uma empresa. Essa abordagem reduz a complexidade operacional inicial, desde que o isolamento seja aplicado rigorosamente.

### 7.2 Contexto da empresa

- Cada usuário pertencerá a uma empresa no MVP.
- Após o login, o backend identificará o usuário e seu `company_id`.
- Todas as operações serão executadas dentro desse contexto.
- O frontend não poderá escolher livremente o `company_id` para acessar dados.
- O administrador poderá gerenciar somente os dados da própria empresa.
- Implementação: `app/core/tenant.py` expõe `AuthenticatedPrincipal`, `TenantContext` e as dependências `get_tenant_context` / `get_company_id`. Um `company_id` enviado pelo cliente é ignorado; na Fase 3 a identidade passa a vir do token de acesso.

### 7.3 Provisionamento de empresa

O fluxo inicial de cadastro deverá criar, de forma transacional:
1. O registro da empresa.
2. O primeiro usuário com perfil Administrador associado à empresa.
3. As configurações iniciais necessárias.

Decisão: o auto cadastro de empresas está habilitado no MVP, protegido por limite de requisições por IP (`SIGNUP_RATE_LIMIT_PER_HOUR`). Empresa, primeiro administrador e configurações iniciais são criados em uma única transação. Convite, aprovação e planos contratados ficam fora do MVP.

### 7.4 Proteção contra vazamento entre empresas

- Aplicar filtros por `company_id` no nível dos serviços/repositórios.
- Validar propriedade do recurso em operações por identificador.
- Usar chaves estrangeiras compostas ou validações equivalentes para impedir relações entre empresas diferentes.
- Considerar Row-Level Security (RLS) do PostgreSQL como camada adicional de defesa, após avaliação técnica.
- Criar testes negativos de isolamento para todos os módulos.
- Não revelar se um identificador existe em outra empresa; responder como recurso não encontrado ou acesso não permitido, conforme a política definida.
- Implementação: `app/repositories/base.py` centraliza `scoped_select`, `list_scoped`, `get_scoped` e `require_same_company`. Toda busca por ID inclui `company_id`; acesso cruzado retorna `404 NOT_FOUND` genérico.
- `app/database/base.py` oferece `tenant_fk_constraint` e `tenant_unique_constraint` para FKs compostas `(company_id, id)` e impede vínculos entre empresas.
- Decisão: Row-Level Security (RLS) do PostgreSQL fica fora do MVP. A defesa usa contexto autenticado, repositório escopado, FKs compostas e testes negativos; RLS pode ser reavaliado se surgir acesso direto ao banco por outras aplicações.

## 8. Modelo de dados inicial

O modelo abaixo representa a estrutura lógica inicial. Tipos e restrições definitivos deverão ser implementados nas migrations.

### 8.1 Entidade `companies`

| Campo | Tipo sugerido | Regras |
|---|---|---|
| id | UUID | Chave primária |
| legal_name | VARCHAR(180) | Razão social ou nome do titular |
| trade_name | VARCHAR(180) | Nome fantasia; opcional |
| document | VARCHAR(20) | CNPJ ou documento aplicável; validar unicidade quando informado |
| email | VARCHAR(255) | E-mail de contato |
| phone | VARCHAR(30) | Telefone de contato |
| is_active | BOOLEAN | Padrão verdadeiro |
| created_at | TIMESTAMP | Data de criação |
| updated_at | TIMESTAMP | Última atualização |

### 8.2 Entidade `users`

| Campo | Tipo sugerido | Regras |
|---|---|---|
| id | UUID | Chave primária |
| company_id | UUID | FK obrigatória para companies |
| name | VARCHAR(150) | Obrigatório |
| email | VARCHAR(255) | Obrigatório; unicidade definida conforme a política de login |
| password_hash | VARCHAR(255) | Obrigatório |
| role | VARCHAR(30) | ADMIN, ATTENDANT ou TECHNICIAN |
| is_active | BOOLEAN | Padrão verdadeiro |
| created_at | TIMESTAMP | Data de criação |
| updated_at | TIMESTAMP | Última atualização |

No MVP, o e-mail de login é único globalmente, com índice funcional `lower(trim(email))` (`uq_users_email_lower`), eliminando diferenças de caixa e espaços. Caso a mesma pessoa precise acessar mais de uma empresa, será necessário evoluir o modelo para associação usuário-empresa e seleção explícita de contexto.

### 8.3 Entidade `customers`

| Campo | Tipo sugerido | Regras |
|---|---|---|
| id | UUID | Chave primária |
| company_id | UUID | FK obrigatória para companies |
| person_type | VARCHAR(2) | PF ou PJ |
| name | VARCHAR(180) | Obrigatório |
| document | VARCHAR(20) | Opcional; normalizado |
| phone | VARCHAR(30) | Opcional |
| email | VARCHAR(255) | Opcional |
| postal_code | VARCHAR(10) | Opcional |
| street | VARCHAR(180) | Opcional |
| number | VARCHAR(20) | Opcional |
| complement | VARCHAR(100) | Opcional |
| neighborhood | VARCHAR(100) | Opcional |
| city | VARCHAR(100) | Opcional |
| state | CHAR(2) | Opcional |
| notes | TEXT | Opcional |
| is_active | BOOLEAN | Padrão verdadeiro |
| created_at | TIMESTAMP | Data de criação |
| updated_at | TIMESTAMP | Última atualização |

### 8.4 Entidade `suppliers`

| Campo | Tipo sugerido | Regras |
|---|---|---|
| id | UUID | Chave primária |
| company_id | UUID | FK obrigatória para companies |
| name | VARCHAR(180) | Obrigatório |
| document | VARCHAR(20) | Opcional |
| contact_name | VARCHAR(150) | Opcional |
| phone | VARCHAR(30) | Opcional |
| email | VARCHAR(255) | Opcional |
| address | TEXT | Opcional |
| notes | TEXT | Opcional |
| is_active | BOOLEAN | Padrão verdadeiro |
| created_at | TIMESTAMP | Data de criação |
| updated_at | TIMESTAMP | Última atualização |

### 8.5 Entidade `service_orders`

| Campo | Tipo sugerido | Regras |
|---|---|---|
| id | UUID | Chave primária |
| company_id | UUID | FK obrigatória para companies |
| order_number | BIGINT | Obrigatório; único dentro da empresa |
| customer_id | UUID | FK para customers |
| technician_id | UUID | FK para users; opcional na abertura |
| opened_by_id | UUID | FK para users |
| title | VARCHAR(180) | Obrigatório |
| description | TEXT | Obrigatório |
| requested_service | TEXT | Opcional |
| status | VARCHAR(30) | Status controlado |
| notes | TEXT | Opcional |
| resolution | TEXT | Obrigatória para concluir |
| cancellation_reason | TEXT | Obrigatória para cancelar |
| opened_at | TIMESTAMP | Gerada pelo servidor |
| completed_at | TIMESTAMP | Preenchida ao concluir |
| created_at | TIMESTAMP | Data de criação |
| updated_at | TIMESTAMP | Última atualização |

O número da OS deverá ser gerado por contador por empresa com bloqueio de linha (`SELECT ... FOR UPDATE`) dentro da transação de abertura, com restrição única composta `(company_id, order_number)`. Não deverá ser calculado contando registros existentes.

### 8.6 Entidade `service_order_history`

| Campo | Tipo sugerido | Regras |
|---|---|---|
| id | UUID | Chave primária |
| company_id | UUID | FK obrigatória para companies |
| service_order_id | UUID | FK para service_orders |
| user_id | UUID | FK para users |
| event_type | VARCHAR(40) | Tipo do evento |
| old_status | VARCHAR(30) | Opcional |
| new_status | VARCHAR(30) | Opcional |
| description | TEXT | Descrição do evento |
| created_at | TIMESTAMP | Data/hora gerada pelo servidor |

O histórico deverá registrar, no mínimo, abertura, alteração de status, atribuição ou troca de técnico, observações relevantes, conclusão e cancelamento.

### 8.7 Relacionamentos e isolamento multiempresa

- `companies` 1:N `users`.
- `companies` 1:N `customers`.
- `companies` 1:N `suppliers`.
- `companies` 1:N `service_orders`.
- `companies` 1:N `service_order_history`.
- `customers` 1:N `service_orders`.
- `users` 1:N `service_orders` como responsável pela abertura.
- `users` 1:N `service_orders` como técnico responsável.
- `service_orders` 1:N `service_order_history`.
- `users` 1:N `service_order_history`.

Regras obrigatórias de isolamento:
- Toda consulta ou alteração de cliente, fornecedor, OS e histórico deverá incluir o `company_id` obtido do usuário autenticado.
- O backend nunca deverá confiar em um `company_id` enviado livremente pelo frontend para definir o contexto da operação.
- Ao consultar uma OS, o backend deverá validar que ela pertence à empresa do usuário autenticado.
- Chaves estrangeiras e, quando apropriado, restrições compostas deverão impedir vínculos entre registros de empresas diferentes.
- Restrições de unicidade de documentos de clientes e fornecedores deverão considerar o escopo da empresa, permitindo que empresas distintas cadastrem clientes com o mesmo documento quando essa for a regra de negócio definida.
- Decisão: contador por empresa com `SELECT ... FOR UPDATE` e constraint `(company_id, order_number)`, garantindo numeração independente e segura sob concorrência.
- O histórico deverá carregar o mesmo `company_id` da OS e sua consistência deverá ser garantida pelo backend e pelo banco.
- Testes automatizados deverão tentar acessar registros de outra empresa e confirmar que o acesso é negado.

Fornecedores serão cadastrados de forma independente no MVP. Um vínculo entre fornecedor e OS poderá ser acrescentado futuramente, caso o fluxo de trabalho exija registrar peças ou serviços terceirizados.

## 9. Estados e transições da ordem de serviço

### 9.1 Estados

| Código | Rótulo | Significado |
|---|---|---|
| OPEN | Aberta | OS registrada e aguardando atendimento |
| IN_PROGRESS | Em andamento | Serviço em execução |
| WAITING | Aguardando | Serviço pendente de peça, informação ou autorização |
| COMPLETED | Concluída | Serviço finalizado |
| CANCELED | Cancelada | Ordem encerrada sem continuidade |

### 9.2 Transições iniciais propostas

```text
                 ┌──────────────┐
                 │    Aberta    │
                 └──────┬───────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
       ┌─────────────┐      ┌─────────────┐
       │ Em andamento│◄────►│  Aguardando │
       └──────┬──────┘      └─────────────┘
              │
              ▼
       ┌─────────────┐
       │  Concluída  │
       └─────────────┘

       Aberta, Em andamento ou Aguardando
                       │
                       ▼
                ┌─────────────┐
                │  Cancelada  │
                └─────────────┘
```

Regras propostas:
- Uma OS deverá iniciar em `OPEN`.
- `OPEN` poderá avançar para `IN_PROGRESS` ou `CANCELED`.
- `IN_PROGRESS` poderá avançar para `WAITING`, `COMPLETED` ou `CANCELED`.
- `WAITING` poderá retornar para `IN_PROGRESS` ou avançar para `CANCELED`.
- `COMPLETED` e `CANCELED` serão estados finais no MVP.
- Reabertura de OS concluída ou cancelada não será permitida inicialmente.
- A conclusão exigirá o preenchimento de `resolution`.
- O cancelamento exigirá `cancellation_reason`.

As transições deverão ser validadas no serviço de domínio, nunca apenas na interface.

## 10. API REST

A API deverá utilizar prefixo `/api/v1`.

### 10.1 Padrões gerais

- Formato de dados: JSON.
- Identificadores: UUID.
- Datas: ISO 8601, armazenadas preferencialmente em UTC.
- Paginação nas listagens.
- Filtros por parâmetros de consulta.
- Respostas de erro padronizadas.
- Autenticação por token de acesso.
- Documentação OpenAPI disponibilizada pelo FastAPI em ambiente de desenvolvimento.

### 10.2 Empresas

| Método | Endpoint | Descrição | Acesso |
|---|---|---|---|
| POST | `/api/v1/companies` | Criar empresa e usuário administrador inicial | Fluxo público controlado ou provisionamento |
| GET | `/api/v1/companies/me` | Consultar dados da empresa do usuário autenticado | Administrador |
| PUT | `/api/v1/companies/me` | Atualizar dados da própria empresa | Administrador |

O cadastro público deverá possuir proteção contra abuso. A criação de uma empresa deverá ocorrer em transação, criando também o primeiro usuário administrador associado a ela. Não deverá existir endpoint que permita ao usuário comum consultar empresas de terceiros.

### 10.3 Autenticação

| Método | Endpoint | Descrição | Acesso |
|---|---|---|---|
| POST | `/api/v1/auth/login` | Autenticar e obter token | Público |
| GET | `/api/v1/auth/me` | Consultar usuário autenticado e empresa atual | Autenticado |

O logout deverá invalidar a sessão ou o mecanismo de renovação de token adotado. Se forem utilizados tokens JWT sem estado, deverá ser definida uma estratégia de expiração e revogação, por exemplo, por meio de refresh tokens armazenados e revogáveis.

### 10.4 Usuários

| Método | Endpoint | Descrição | Acesso |
|---|---|---|---|
| GET | `/api/v1/users` | Listar usuários | Administrador |
| POST | `/api/v1/users` | Criar usuário | Administrador |
| GET | `/api/v1/users/{id}` | Consultar usuário | Administrador |
| PUT | `/api/v1/users/{id}` | Atualizar usuário | Administrador |
| PATCH | `/api/v1/users/{id}/status` | Ativar ou inativar usuário | Administrador |

### 10.5 Clientes

| Método | Endpoint | Descrição | Acesso |
|---|---|---|---|
| GET | `/api/v1/customers` | Listar e pesquisar clientes | Administrador, Atendente |
| POST | `/api/v1/customers` | Cadastrar cliente | Administrador, Atendente |
| GET | `/api/v1/customers/{id}` | Consultar cliente | Administrador, Atendente |
| PUT | `/api/v1/customers/{id}` | Atualizar cliente | Administrador, Atendente |
| PATCH | `/api/v1/customers/{id}/status` | Inativar ou reativar cliente | Administrador |

### 10.6 Fornecedores

| Método | Endpoint | Descrição | Acesso |
|---|---|---|---|
| GET | `/api/v1/suppliers` | Listar e pesquisar fornecedores | Administrador, Atendente |
| POST | `/api/v1/suppliers` | Cadastrar fornecedor | Administrador, Atendente |
| GET | `/api/v1/suppliers/{id}` | Consultar fornecedor | Administrador, Atendente |
| PUT | `/api/v1/suppliers/{id}` | Atualizar fornecedor | Administrador, Atendente |
| PATCH | `/api/v1/suppliers/{id}/status` | Inativar ou reativar fornecedor | Administrador |

### 10.7 Ordens de serviço

| Método | Endpoint | Descrição | Acesso |
|---|---|---|---|
| GET | `/api/v1/service-orders` | Listar, pesquisar e filtrar OS | Conforme perfil |
| POST | `/api/v1/service-orders` | Abrir OS | Administrador, Atendente |
| GET | `/api/v1/service-orders/{id}` | Consultar detalhes da OS | Conforme perfil |
| PUT | `/api/v1/service-orders/{id}` | Atualizar dados permitidos | Administrador, Atendente |
| PATCH | `/api/v1/service-orders/{id}/technician` | Atribuir ou trocar técnico | Administrador, Atendente |
| PATCH | `/api/v1/service-orders/{id}/status` | Atualizar status | Admin, Atendente ou Técnico nas OS atribuídas |
| POST | `/api/v1/service-orders/{id}/notes` | Registrar observação técnica | Administrador, Técnico autorizado |
| POST | `/api/v1/service-orders/{id}/complete` | Concluir OS e registrar solução | Administrador, Técnico autorizado |
| POST | `/api/v1/service-orders/{id}/cancel` | Cancelar OS com justificativa | Administrador |

Para técnicos, as operações de consulta e atualização deverão verificar se a OS está atribuída ao usuário autenticado.

### 10.8 Dashboard

| Método | Endpoint | Descrição | Acesso |
|---|---|---|---|
| GET | `/api/v1/dashboard/summary` | Indicadores gerais por status | Administrador, Atendente |
| GET | `/api/v1/dashboard/recent-orders` | Ordens recentes | Administrador, Atendente |

### 10.9 Filtros e paginação de OS

O endpoint de listagem deverá aceitar parâmetros semelhantes a:

```http
GET /api/v1/service-orders?page=1&page_size=20&status=OPEN&customer_id={uuid}&start_date=2026-01-01&end_date=2026-01-31&search=123
```

Parâmetros previstos:
- `page`: página solicitada.
- `page_size`: quantidade por página, com limite máximo definido.
- `status`: status da ordem.
- `customer_id`: identificador do cliente.
- `technician_id`: identificador do técnico, para perfis autorizados.
- `start_date` e `end_date`: intervalo de abertura.

O `company_id` não deverá ser aceito como filtro de segurança enviado pelo cliente. O escopo empresarial será derivado da identidade autenticada e aplicado automaticamente pelo backend.
- `search`: busca por número da OS ou nome do cliente.

A API deverá validar os filtros e impedir que um técnico consulte ordens de outros técnicos apenas alterando parâmetros da URL.

## 11. Padrão de resposta da API

### 11.1 Resposta de sucesso

Os endpoints deverão retornar os códigos HTTP apropriados e os dados previstos para cada operação.

Exemplo ilustrativo:

```json
{
  "id": "uuid",
  "order_number": 1001,
  "status": "OPEN",
  "message": "Ordem de serviço criada com sucesso."
}
```

### 11.2 Resposta de erro

Formato sugerido:

```json
{
  "detail": {
    "code": "VALIDATION_ERROR",
    "message": "Não foi possível concluir a operação.",
    "fields": {
      "customer_id": "Cliente não encontrado."
    }
  }
}
```

Códigos HTTP principais:
- `200 OK`: consulta ou atualização concluída.
- `201 Created`: registro criado.
- `204 No Content`: operação concluída sem corpo de resposta.
- `400 Bad Request`: solicitação inválida ou transição não permitida.
- `401 Unauthorized`: usuário não autenticado.
- `403 Forbidden`: usuário sem permissão.
- `404 Not Found`: recurso não encontrado.
- `409 Conflict`: conflito, como documento duplicado.
- `422 Unprocessable Entity`: dados não passaram na validação.
- `500 Internal Server Error`: erro inesperado.

Mensagens destinadas ao usuário não deverão expor detalhes internos, SQL, caminhos locais, tokens ou stack traces.

## 12. Segurança

A implementação deverá observar, no mínimo, as seguintes diretrizes:

1. Armazenar senhas somente como hash, utilizando algoritmo apropriado para senhas, como Argon2id ou bcrypt com configuração segura.
2. Utilizar HTTPS em produção.
3. Proteger endpoints privados por autenticação.
4. Validar permissões no backend em todas as operações protegidas.
5. Aplicar validação de entrada com Pydantic e restrições no banco.
6. Configurar CORS somente para as origens autorizadas.
7. Manter segredos em variáveis de ambiente ou serviço de gerenciamento de segredos.
8. Não registrar senhas, tokens ou dados pessoais desnecessários nos logs.
9. Aplicar limitação de tentativas de login e medidas contra abuso.
10. Utilizar consultas parametrizadas ou ORM para reduzir risco de SQL injection.
11. Restringir o acesso de técnicos às OS atribuídas.
12. Registrar eventos importantes para auditoria.
13. Manter dependências atualizadas e revisar vulnerabilidades.
14. Definir política de backup e teste de restauração.

### 12.1 LGPD e dados pessoais

O sistema armazenará dados pessoais de clientes, fornecedores e usuários. A implementação deverá:
- Coletar somente dados necessários à operação.
- Restringir o acesso conforme a função do usuário.
- Definir finalidade e política de retenção dos dados.
- Proteger dados em trânsito e em repouso conforme a infraestrutura disponível.
- Permitir atendimento a solicitações de titulares, conforme os procedimentos definidos pela empresa.
- Evitar exposição de documentos pessoais em listagens e logs.

As responsabilidades legais, bases legais e prazos de retenção deverão ser definidos pelo controlador dos dados com orientação apropriada. Este documento não constitui parecer jurídico.

## 13. Interface e experiência do usuário

A interface deverá priorizar clareza, facilidade de navegação e rapidez na localização de informações.

### 13.1 Estrutura inicial de telas

- Login.
- Dashboard.
- Listagem de ordens de serviço.
- Abertura de ordem de serviço.
- Detalhes da ordem de serviço.
- Edição da ordem de serviço.
- Listagem e formulário de clientes.
- Listagem e formulário de fornecedores.
- Gerenciamento de usuários.
- Perfil e configurações básicas.

### 13.2 Diretrizes de interface

- Menu de navegação consistente.
- Formulários com rótulos claros e indicação de campos obrigatórios.
- Mensagens de sucesso, erro e confirmação.
- Confirmação antes de cancelar uma OS ou executar ações sensíveis.
- Filtros visíveis na listagem de OS.
- Status identificados por texto e elemento visual, sem depender somente de cores.
- Paginação nas listagens.
- Layout adaptável a telas pequenas.
- Estados de carregamento e telas vazias.
- Acessibilidade básica: navegação por teclado, contraste adequado e rótulos associados aos campos.

O detalhamento visual, componentes e protótipos deverão ser registrados em `design.md`.

## 14. Requisitos de desempenho e escalabilidade

Para o MVP:
- Utilizar paginação em listagens.
- Criar índices para `(company_id, order_number)`, `(company_id, status, opened_at)`, `(company_id, customer_id)` e `(company_id, technician_id)`.
- Evitar consultas repetidas desnecessárias.
- Retornar somente os campos necessários em cada listagem.
- Definir limites de tamanho para paginação e campos textuais.
- Monitorar tempo de resposta e erros em produção.

Metas numéricas de desempenho deverão ser definidas após estimar quantidade de usuários, volume de ordens e infraestrutura de hospedagem.

## 15. Logs, auditoria e tratamento de erros

- Registrar erros técnicos no backend sem expor informações sensíveis.
- Associar eventos de negócio ao usuário autenticado.
- Registrar data e hora pelo servidor.
- Manter histórico de alterações de status.
- Registrar atribuição e troca de técnico.
- Registrar conclusão e cancelamento.
- Não permitir que usuários comuns alterem ou apaguem o histórico.
- Definir política de retenção dos logs técnicos.

O histórico da OS é um registro de negócio e deverá permanecer associado à ordem mesmo após sua conclusão ou cancelamento.

## 16. Ambiente e configuração

### 16.1 Variáveis de ambiente

Exemplo de configuração, sem valores reais:

```env
APP_NAME=OrdemFacil
APP_ENV=development
APP_DEBUG=true
API_V1_PREFIX=/api/v1

DATABASE_URL=postgresql+psycopg://usuario:senha@localhost:5432/ordemfacil
DATABASE_TEST_URL=postgresql+psycopg://usuario:senha@localhost:5432/ordemfacil_test

SECRET_KEY=definir-uma-chave-segura
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

CORS_ORIGINS=http://localhost:5500,http://127.0.0.1:5500

SIGNUP_RATE_LIMIT_PER_HOUR=5
```

Regras:
- O arquivo `.env` não deverá ser versionado.
- O arquivo `.env.example` deverá conter somente nomes e exemplos fictícios.
- Produção deverá utilizar `APP_DEBUG=false`.
- A chave secreta deverá ser forte e exclusiva por ambiente.
- As origens CORS deverão ser configuradas conforme o domínio real do frontend.

### 16.2 Ambientes

- **Desenvolvimento:** execução local para implementação.
- **Teste:** ambiente para validação integrada.
- **Produção:** ambiente publicado e acessível aos usuários.

As configurações e credenciais deverão ser separadas por ambiente.

## 17. Testes

A implementação deverá incluir testes automatizados e validações manuais.

### 17.1 Testes unitários

- Validação de CPF/CNPJ, quando aplicável.
- Regras de transição de status.
- Regras de conclusão e cancelamento.
- Verificação de permissões.
- Geração de número de OS.

### 17.2 Testes de integração

- Login e acesso a rotas protegidas.
- Criação, consulta e atualização de clientes.
- Criação e consulta de fornecedores.
- Abertura de OS e geração do número.
- Atribuição de técnico.
- Atualização de status.
- Registro de histórico.
- Filtros e paginação.
- Bloqueio de acesso indevido.

### 17.3 Testes de interface

- Navegação entre telas.
- Validação dos formulários.
- Exibição de mensagens de erro e sucesso.
- Pesquisa e filtros.
- Responsividade em computador e celular.
- Acessibilidade básica.

## 18. Implantação e operação

A aplicação deverá ser preparada para implantação em servidor com acesso à internet.

Diretrizes:
- Executar FastAPI por servidor ASGI adequado.
- Utilizar PostgreSQL como serviço de banco de dados.
- Utilizar proxy reverso e HTTPS em produção.
- Executar migrations de forma controlada.
- Configurar backup periódico do banco.
- Manter logs e monitoramento básico.
- Não utilizar servidor de desenvolvimento em produção.

Decisão: homologação em VPS com Docker Compose (API + PostgreSQL), reverse proxy com HTTPS via Let's Encrypt e backup periódico com `pg_dump` e teste de restauração. A troca por banco gerenciado exige atualizar este documento antes da publicação.

## 19. Critérios técnicos de conclusão

A implementação técnica do MVP será considerada concluída quando:

- A aplicação frontend conseguir consumir a API.
- O backend estiver organizado em módulos e com documentação OpenAPI.
- O PostgreSQL estiver configurado e versionado por migrations.
- Autenticação e autorização estiverem funcionando no backend.
- Os módulos de clientes, fornecedores, usuários e OS estiverem integrados.
- O número da OS for único e gerado de forma segura.
- As regras de transição de status forem aplicadas no backend.
- O histórico registrar eventos relevantes.
- Os filtros e a paginação funcionarem.
- Os testes automatizados essenciais forem executados com sucesso.
- A aplicação funcionar em ambiente de teste com interface responsiva.
- As instruções de configuração e execução estiverem registradas no `README.md`.

## 20. Decisões técnicas registradas

1. **Usuário por empresa:** no MVP, cada usuário pertence a uma única empresa e o e-mail de login é único globalmente. Perfis: `ADMIN`, `ATTENDANT` e `TECHNICIAN`.
2. **Frontend:** HTML, CSS e JavaScript puro, sem framework, conforme os componentes de `design.md` §8.
3. **Autenticação:** access token JWT com 30 minutos de validade e refresh token opaco, armazenado e revogável; refresh token em cookie `HttpOnly`, `Secure` e `SameSite=Strict`. Senhas armazenadas com Argon2id.
4. **Técnico:** somente registra observações/solução e atualiza o status das OS atribuídas; não edita campos operacionais.
5. **Responsável da OS:** no máximo um técnico por OS no MVP.
6. **Anexos:** fora do MVP.
7. **Impressão/PDF:** fora do MVP.
8. **Hospedação e backup:** homologação em VPS com Docker Compose, reverse proxy HTTPS (Let's Encrypt), `pg_dump` agendado e teste de restauração; banco de testes dedicado `ordemfacil_test` com `APP_ENV=test`.
9. **Cadastro público de empresa:** habilitado no MVP com limite de requisições por IP e criação transacional de empresa + primeiro administrador.
10. **Isolamento:** contexto autenticado + repositório escopado + FKs compostas `(company_id, id)`; RLS não adotado no MVP (ver `spec.md` §7.4).
11. **E-mail de login:** único globalmente, normalizado por `lower(trim(email))`; um usuário pertence a uma única empresa.
12. **Identificadores:** UUIDs gerados pela aplicação (`uuid4`), sem `gen_random_uuid()` no banco; mantém os modelos testáveis em SQLite unitário sem alterar o tipo no PostgreSQL.

Estas decisões são a fonte de verdade para modelo de dados, endpoints e testes. Reabri-las exige atualizar este documento e os documentos relacionados.

---

**Documento:** `spec.md`  
**Projeto:** OrdemFácil  
**Versão:** 1.2 — Fundação multiempresa  
**Documento relacionado:** `requirements.md`
