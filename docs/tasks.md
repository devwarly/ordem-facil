# Tasks — OrdemFácil

**Projeto:** OrdemFácil — Sistema Web Multiempresa de Gerenciamento de Ordens de Serviço  
**Versão:** 1.2  
**Documentos de referência:** `requirements.md`, `spec.md` e `design.md`  
**Status:** Backlog inicial do MVP

---

## 1. Objetivo

Este documento transforma os requisitos e as especificações do OrdemFácil em tarefas de desenvolvimento pequenas, organizadas e verificáveis.

As tarefas devem ser executadas preferencialmente na ordem apresentada. Cada etapa deverá ser testada antes de avançar para a próxima.

## 2. Orientações para execução

- Consultar `requirements.md`, `spec.md` e `design.md` antes de implementar cada módulo.
- Implementar as regras de negócio no backend; o frontend não será considerado uma camada de segurança.
- Garantir isolamento multiempresa em todas as consultas e operações.
- Não confiar em `company_id` enviado pelo navegador: o contexto deverá ser obtido do usuário autenticado.
- Criar migrations para toda alteração no esquema do banco.
- Criar testes para regras de negócio, permissões e isolamento entre empresas.
- Não implementar funcionalidades fora do MVP sem atualizar os documentos.
- Marcar uma tarefa como concluída somente após implementação e validação.
- Registrar decisões técnicas relevantes no `spec.md` ou em documentação complementar.
- Decisões fechadas em `spec.md` §20; não reabri-las sem atualizar a documentação.

## 3. Convenções

- `[ ]` Pendente.
- `[x]` Concluída.
- **Prioridade alta:** necessária para o funcionamento seguro do MVP.
- **Prioridade média:** importante, mas pode ser finalizada após o fluxo principal.
- **Prioridade baixa:** melhoria ou preparação para evolução.

---

## 4. Fase 0 — Preparação do projeto

**Objetivo:** organizar o repositório, ferramentas e ambiente de desenvolvimento.

### Tarefas

- [x] **TASK-001 — Criar estrutura inicial do repositório**  
  Criar as pastas `backend`, `frontend` e `docs`, conforme a estrutura definida em `spec.md`.

- [x] **TASK-002 — Adicionar documentação do projeto**  
  Adicionar `requirements.md`, `spec.md`, `design.md`, `tasks.md` e um `README.md` inicial à pasta `docs` ou à raiz, conforme a organização escolhida.

- [x] **TASK-003 — Configurar Git e `.gitignore`**  
  Ignorar ambientes virtuais, arquivos `.env`, caches, arquivos temporários, logs e artefatos de build.

- [x] **TASK-004 — Criar arquivo `.env.example`**  
  Documentar as variáveis necessárias sem incluir credenciais reais.

- [x] **TASK-005 — Definir e registrar versões das dependências**  
  Preparar a configuração de dependências do backend e registrar as versões utilizadas.

**Critério de conclusão:** repositório organizado, documentação disponível e nenhum segredo versionado.

---

## 5. Fase 1 — Configuração do backend e banco de dados

**Objetivo:** preparar a API FastAPI e a conexão com PostgreSQL.

### Tarefas

- [x] **TASK-006 — Criar aplicação FastAPI**  
  Implementar `main.py`, inicialização da aplicação, configuração básica e endpoint de verificação de saúde.

- [x] **TASK-007 — Configurar variáveis de ambiente**  
  Implementar leitura e validação das configurações da aplicação.

- [x] **TASK-008 — Configurar conexão com PostgreSQL**  
  Criar engine, sessão e dependências de banco de dados.

- [x] **TASK-009 — Configurar SQLAlchemy**  
  Preparar base declarativa, convenções de modelos e integração com PostgreSQL.

- [x] **TASK-010 — Configurar Alembic**  
  Preparar migrations e validar criação e atualização do banco.

- [x] **TASK-011 — Configurar tratamento padronizado de erros**  
  Definir respostas consistentes para erros de validação, autenticação, autorização e recursos inexistentes.

- [x] **TASK-012 — Configurar CORS**  
  Permitir somente as origens autorizadas por ambiente.

- [x] **TASK-013 — Criar testes básicos da aplicação**  
  Testar inicialização, endpoint de saúde e conexão com banco.

**Critério de conclusão:** API executa localmente, conecta ao PostgreSQL e aplica migrations sem erro.

---

## 6. Fase 2 — Fundação multiempresa

**Objetivo:** implementar o isolamento de dados entre empresas antes dos módulos de negócio.

### Tarefas

- [x] **TASK-014 — Criar modelo Company**  
  Implementar entidade `companies` com identificação, dados cadastrais, situação e datas de criação/atualização.

- [x] **TASK-015 — Criar migration de empresas**  
  Gerar e aplicar migration para a tabela `companies`.

- [x] **TASK-016 — Associar usuários a empresas**  
  Incluir `company_id` obrigatório em `users` e criar relacionamento com `companies`.

- [x] **TASK-017 — Definir política de unicidade do e-mail**  
  Aplicar a decisão do MVP: e-mail de login único globalmente, documentando a limitação de um usuário por empresa.

- [x] **TASK-018 — Criar contexto de empresa autenticada**  
  Implementar dependência que obtenha o `company_id` a partir da identidade autenticada.

- [x] **TASK-019 — Criar mecanismo de escopo multiempresa**  
  Implementar padrão reutilizável para filtrar e validar registros pelo `company_id`.

- [x] **TASK-020 — Proteger relacionamentos entre empresas**  
  Definir constraints e validações para impedir que registros de empresas diferentes sejam associados.

- [x] **TASK-021 — Criar testes de isolamento multiempresa**  
  Criar pelo menos duas empresas de teste e validar que uma não consegue consultar, alterar ou relacionar dados da outra.

**Critério de conclusão:** contexto empresarial aplicado no backend e testes negativos comprovam o isolamento entre empresas.

> Esta fase é bloqueadora para os módulos de clientes, fornecedores e ordens de serviço. Não avançar com dados de negócio sem o isolamento multiempresa implementado e testado.

---

## 7. Fase 3 — Autenticação e usuários

**Objetivo:** permitir acesso seguro ao ambiente de cada empresa.

### Tarefas

- [ ] **TASK-022 — Criar modelo User**  
  Implementar os campos definidos em `spec.md`, incluindo empresa, perfil e situação.

- [ ] **TASK-023 — Implementar hash de senha**  
  Utilizar algoritmo apropriado para armazenamento seguro de senhas.

- [ ] **TASK-024 — Implementar autenticação**  
  Criar login e emissão de credenciais de acesso conforme a estratégia definida no `spec.md`.

- [ ] **TASK-025 — Implementar identificação do usuário autenticado**  
  Criar dependência para recuperar usuário, perfil e empresa da credencial validada.

- [ ] **TASK-026 — Implementar autorização por perfil**  
  Criar verificações reutilizáveis para Administrador, Atendente e Técnico.

- [ ] **TASK-027 — Implementar endpoint de usuário atual**  
  Criar `GET /api/v1/auth/me`, retornando dados do usuário e da empresa atual sem informações sensíveis.

- [ ] **TASK-028 — Implementar encerramento ou revogação de sessão**  
  Aplicar o comportamento compatível com a estratégia de autenticação escolhida.

- [ ] **TASK-029 — Implementar gerenciamento de usuários**  
  Criar endpoints para listar, cadastrar, consultar, editar e ativar/inativar usuários da própria empresa.

- [ ] **TASK-030 — Criar fluxo de provisionamento de empresa**  
  Implementar criação da empresa e do primeiro usuário Administrador em uma única transação, caso o cadastro público seja adotado.

- [ ] **TASK-031 — Criar testes de autenticação e autorização**  
  Testar credenciais inválidas, usuário inativo, token inválido, perfil sem permissão e tentativa de acesso cruzado entre empresas.

**Critério de conclusão:** usuários autenticam-se e só acessam operações e dados permitidos para seu perfil e empresa.

---

## 8. Fase 4 — Cadastro de clientes

**Objetivo:** implementar o cadastro e gerenciamento de clientes por empresa.

### Tarefas

- [ ] **TASK-032 — Criar modelo Customer**  
  Implementar os campos de pessoa física/jurídica, documento, contato, endereço, observações e situação, incluindo `company_id`.

- [ ] **TASK-033 — Criar migration de clientes**  
  Criar tabela, índices, constraints e relacionamentos necessários.

- [ ] **TASK-034 — Criar schemas de cliente**  
  Implementar schemas Pydantic para criação, atualização e resposta.

- [ ] **TASK-035 — Implementar validações de cliente**  
  Validar campos obrigatórios, tipo de pessoa, formato de e-mail e documento quando informado.

- [ ] **TASK-036 — Implementar cadastro e consulta de clientes**  
  Criar endpoints para criar, listar e consultar clientes dentro do escopo da empresa.

- [ ] **TASK-037 — Implementar atualização e inativação de clientes**  
  Permitir edição e alteração de situação sem apagar registros relacionados.

- [ ] **TASK-038 — Implementar pesquisa e paginação de clientes**  
  Permitir pesquisar por nome, documento ou outros campos definidos.

- [ ] **TASK-039 — Criar testes do módulo de clientes**  
  Testar validações, duplicidade no escopo da empresa, paginação, permissões e isolamento multiempresa.

**Critério de conclusão:** clientes podem ser gerenciados por usuários autorizados sem possibilidade de acesso cruzado entre empresas.

---

## 9. Fase 5 — Cadastro de fornecedores

**Objetivo:** implementar o cadastro e gerenciamento de fornecedores por empresa.

### Tarefas

- [ ] **TASK-040 — Criar modelo Supplier**  
  Implementar dados cadastrais, contato, endereço, observações, situação e `company_id`.

- [ ] **TASK-041 — Criar migration de fornecedores**  
  Criar tabela, índices, constraints e relacionamentos necessários.

- [ ] **TASK-042 — Criar schemas de fornecedor**  
  Implementar schemas Pydantic para criação, atualização e resposta.

- [ ] **TASK-043 — Implementar cadastro e consulta de fornecedores**  
  Criar endpoints de criação, listagem e consulta.

- [ ] **TASK-044 — Implementar atualização e inativação de fornecedores**  
  Permitir editar e inativar fornecedores sem excluir fisicamente o cadastro.

- [ ] **TASK-045 — Implementar pesquisa e paginação de fornecedores**  
  Permitir pesquisar fornecedores por nome ou documento.

- [ ] **TASK-046 — Criar testes do módulo de fornecedores**  
  Testar validações, permissões, paginação e isolamento multiempresa.

**Critério de conclusão:** fornecedores podem ser gerenciados por empresa e não podem ser consultados por outra empresa.

---

## 10. Fase 6 — Ordens de serviço

**Objetivo:** implementar o fluxo principal do OrdemFácil.

### Tarefas

- [ ] **TASK-047 — Criar modelo ServiceOrder**  
  Implementar número, cliente, técnico, usuário de abertura, descrição, serviço solicitado, status, datas, solução, justificativa de cancelamento e `company_id`.

- [ ] **TASK-048 — Implementar geração segura do número da OS**  
  Criar estratégia transacional de numeração única por empresa. Não utilizar contagem de registros para gerar o próximo número.

- [ ] **TASK-049 — Criar migration de ordens de serviço**  
  Criar tabela, índices, constraints e chaves estrangeiras.

- [ ] **TASK-050 — Criar modelo ServiceOrderHistory**  
  Implementar histórico com empresa, OS, usuário, tipo de evento, status anterior/novo, descrição e data/hora.

- [ ] **TASK-051 — Criar migration do histórico**  
  Criar tabela e relacionamentos, garantindo consistência com a empresa da OS.

- [ ] **TASK-052 — Criar schemas de ordem de serviço**  
  Implementar schemas de criação, atualização, alteração de status, conclusão, cancelamento e resposta.

- [ ] **TASK-053 — Implementar abertura de OS**  
  Criar endpoint que vincule cliente da mesma empresa, gere número, registre usuário de abertura e defina status inicial `OPEN`.

- [ ] **TASK-054 — Implementar listagem e consulta de OS**  
  Criar endpoints para listar e visualizar detalhes, sempre aplicando escopo da empresa.

- [ ] **TASK-055 — Implementar filtros e paginação de OS**  
  Permitir filtrar por número, cliente, status, técnico e período de abertura.

- [ ] **TASK-056 — Implementar edição de OS**  
  Permitir atualização dos campos autorizados conforme perfil e status.

- [ ] **TASK-057 — Implementar atribuição de técnico**  
  Permitir atribuir ou trocar técnico, validando que o usuário pertence à mesma empresa e possui perfil Técnico.

- [ ] **TASK-058 — Implementar máquina de estados da OS**  
  Validar transições permitidas no serviço de negócio.

- [ ] **TASK-059 — Implementar registro de observações técnicas**  
  Permitir que técnicos autorizados registrem observações, com autoria e data/hora.

- [ ] **TASK-060 — Implementar conclusão de OS**  
  Exigir solução aplicada, registrar data de conclusão e evento no histórico.

- [ ] **TASK-061 — Implementar cancelamento de OS**  
  Exigir justificativa, validar permissão e registrar evento no histórico.

- [ ] **TASK-062 — Implementar histórico da OS**  
  Registrar abertura, mudanças de status, atribuições, observações relevantes, conclusão e cancelamento.

- [ ] **TASK-063 — Implementar autorização específica para Técnico**  
  Garantir que o técnico só consulte e atualize ordens atribuídas a ele, dentro da própria empresa.

- [ ] **TASK-064 — Criar testes do fluxo de OS**  
  Testar abertura, numeração, edição, atribuição, transições, conclusão, cancelamento, histórico, permissões e isolamento multiempresa.

**Critério de conclusão:** o ciclo de vida de uma OS funciona de ponta a ponta, com histórico e isolamento empresarial testados.

---

## 11. Fase 7 — Dashboard

**Objetivo:** apresentar uma visão resumida das ordens de serviço da empresa.

### Tarefas

- [ ] **TASK-065 — Implementar serviço de indicadores**  
  Calcular totais por status e ordens recentes no escopo da empresa autenticada.

- [ ] **TASK-066 — Criar endpoint de resumo**  
  Implementar `GET /api/v1/dashboard/summary`.

- [ ] **TASK-067 — Criar endpoint de ordens recentes**  
  Implementar `GET /api/v1/dashboard/recent-orders`.

- [ ] **TASK-068 — Criar testes do dashboard**  
  Validar cálculos, filtros por empresa e comportamento sem registros.

**Critério de conclusão:** indicadores correspondem aos dados reais e nunca agregam registros de empresas diferentes.

---

## 12. Fase 8 — Estrutura e componentes do frontend

**Objetivo:** preparar a interface e os componentes reutilizáveis.

### Tarefas

- [ ] **TASK-069 — Criar estrutura do frontend**  
  Organizar páginas, componentes, estilos, scripts e recursos estáticos.

- [ ] **TASK-070 — Implementar identidade visual inicial**  
  Aplicar paleta, tipografia, espaçamentos, bordas e padrões definidos em `design.md`.

- [ ] **TASK-071 — Implementar AppLayout**  
  Criar estrutura principal com barra lateral, cabeçalho e área de conteúdo.

- [ ] **TASK-072 — Implementar navegação por perfil**  
  Exibir opções compatíveis com o perfil, sem tratar a interface como mecanismo de autorização.

- [ ] **TASK-073 — Criar componentes de formulário**  
  Implementar campos, rótulos, mensagens de validação e estados de envio.

- [ ] **TASK-074 — Criar componentes de feedback**  
  Implementar toast, alertas, confirmação, loading e estado vazio.

- [ ] **TASK-075 — Criar componentes de listagem**  
  Implementar tabela, pesquisa, filtros e paginação reutilizáveis.

- [ ] **TASK-076 — Implementar responsividade**  
  Adaptar menu, formulários, tabelas e telas para dispositivos móveis.

- [ ] **TASK-077 — Implementar padrões básicos de acessibilidade**  
  Garantir foco visível, navegação por teclado, rótulos e contraste.

**Critério de conclusão:** estrutura visual reutilizável e responsiva disponível para os módulos.

---

## 13. Fase 9 — Telas de autenticação e empresa

**Objetivo:** conectar a interface aos recursos de acesso e contexto empresarial.

### Tarefas

- [ ] **TASK-078 — Implementar tela de login**  
  Criar formulário e integração com endpoint de autenticação.

- [ ] **TASK-079 — Implementar persistência segura da sessão no frontend**  
  Seguir a estratégia de autenticação definida. Não armazenar credenciais em locais inseguros.

- [ ] **TASK-080 — Implementar proteção de páginas**  
  Redirecionar usuários não autenticados e tratar sessão expirada.

- [ ] **TASK-081 — Implementar identificação da empresa e usuário**  
  Exibir os dados retornados pelo endpoint de usuário atual.

- [ ] **TASK-082 — Implementar tela de cadastro de empresa, se aprovada**  
  Criar interface para provisionar empresa e primeiro administrador.

- [ ] **TASK-083 — Implementar tela Minha Empresa**  
  Consultar e atualizar dados da empresa autenticada.

- [ ] **TASK-084 — Implementar tela Minha Conta**  
  Exibir dados do usuário e permitir encerramento da sessão.

**Critério de conclusão:** usuário entra no sistema e visualiza somente o ambiente da empresa à qual pertence.

---

## 14. Fase 10 — Telas de clientes, fornecedores e usuários

**Objetivo:** disponibilizar os cadastros na interface.

### Tarefas

- [ ] **TASK-085 — Implementar listagem de clientes**  
  Integrar pesquisa, filtros, paginação e ações autorizadas.

- [ ] **TASK-086 — Implementar formulário de cliente**  
  Criar e editar clientes, com validações e feedback.

- [ ] **TASK-087 — Implementar inativação de cliente**  
  Exibir confirmação e atualizar situação após resposta da API.

- [ ] **TASK-088 — Implementar listagem de fornecedores**  
  Integrar pesquisa e paginação.

- [ ] **TASK-089 — Implementar formulário de fornecedor**  
  Criar e editar fornecedores.

- [ ] **TASK-090 — Implementar inativação de fornecedor**  
  Exibir confirmação e atualizar situação.

- [ ] **TASK-091 — Implementar listagem de usuários**  
  Exibir usuários da empresa, perfil e situação.

- [ ] **TASK-092 — Implementar formulário de usuário**  
  Criar e editar usuários conforme permissões do Administrador.

- [ ] **TASK-093 — Implementar ativação e inativação de usuário**  
  Exibir confirmação e refletir a situação atualizada.

**Critério de conclusão:** cadastros podem ser operados pela interface e refletem corretamente as regras da API.

---

## 15. Fase 11 — Telas de ordens de serviço

**Objetivo:** disponibilizar o fluxo principal para os usuários.

### Tarefas

- [ ] **TASK-094 — Implementar dashboard**  
  Exibir cartões de indicadores e ordens recentes.

- [ ] **TASK-095 — Implementar listagem de OS**  
  Exibir número, cliente, descrição, técnico, data e status.

- [ ] **TASK-096 — Implementar pesquisa e filtros de OS**  
  Integrar filtros por número, cliente, status, técnico e período.

- [ ] **TASK-097 — Implementar formulário de abertura de OS**  
  Permitir selecionar cliente, preencher solicitação e enviar para a API.

- [ ] **TASK-098 — Implementar tela de detalhes da OS**  
  Exibir identificação, cliente, solicitação, responsável, execução e histórico.

- [ ] **TASK-099 — Implementar edição de OS**  
  Exibir e habilitar somente campos permitidos para o perfil e situação.

- [ ] **TASK-100 — Implementar atribuição de técnico**  
  Permitir selecionar técnico da própria empresa.

- [ ] **TASK-101 — Implementar atualização de status**  
  Exibir somente transições permitidas e tratar erros retornados pela API.

- [ ] **TASK-102 — Implementar registro de observações técnicas**  
  Disponibilizar formulário para usuários autorizados.

- [ ] **TASK-103 — Implementar conclusão de OS**  
  Solicitar solução aplicada e confirmação antes de concluir.

- [ ] **TASK-104 — Implementar cancelamento de OS**  
  Solicitar justificativa e confirmação antes de cancelar.

- [ ] **TASK-105 — Implementar linha do tempo do histórico**  
  Exibir eventos em ordem cronológica, com autor e data/hora.

**Critério de conclusão:** usuário autorizado consegue executar o ciclo de uma OS pela interface, do registro ao encerramento.

---

## 16. Fase 12 — Integração, segurança e qualidade

**Objetivo:** validar o sistema integrado e corrigir problemas antes da publicação.

### Tarefas

- [ ] **TASK-106 — Revisar isolamento multiempresa em todos os endpoints**  
  Conferir listagens, detalhes, atualizações, inativações, relacionamentos e indicadores.

- [ ] **TASK-107 — Executar testes de acesso cruzado**  
  Tentar acessar recursos de outra empresa usando IDs conhecidos e confirmar bloqueio.

- [ ] **TASK-108 — Revisar autorização por perfil**  
  Validar Administrador, Atendente e Técnico em todas as operações.

- [ ] **TASK-109 — Revisar validações frontend/backend**  
  Garantir que dados inválidos sejam rejeitados pelo backend.

- [ ] **TASK-110 — Revisar tratamento de erros**  
  Evitar mensagens técnicas, stack traces e informações sensíveis na interface.

- [ ] **TASK-111 — Executar testes de integração ponta a ponta**  
  Validar cadastro da empresa, login, cadastros, abertura e conclusão de OS.

- [ ] **TASK-112 — Executar testes responsivos**  
  Validar as principais telas em diferentes larguras.

- [ ] **TASK-113 — Revisar acessibilidade básica**  
  Testar navegação por teclado, foco, rótulos e contraste.

- [ ] **TASK-114 — Revisar dependências e configurações de segurança**  
  Conferir segredos, CORS, HTTPS, política de senha e logs.

**Critério de conclusão:** fluxos principais e controles de segurança aprovados nos testes definidos.

---

## 17. Fase 13 — Implantação e documentação

**Objetivo:** preparar o MVP para execução em ambiente de teste ou produção.

### Tarefas

- [ ] **TASK-115 — Preparar configuração de produção**  
  Separar variáveis, segredos, origens permitidas e configurações de debug.

- [ ] **TASK-116 — Preparar execução da aplicação**  
  Documentar comandos de inicialização do frontend, backend e banco.

- [ ] **TASK-117 — Configurar proxy reverso e HTTPS**  
  Preparar publicação segura conforme o ambiente de hospedagem escolhido.

- [ ] **TASK-118 — Preparar estratégia de backup**  
  Configurar cópias de segurança e documentar procedimento de restauração.

- [ ] **TASK-119 — Documentar migrations e atualização**  
  Registrar procedimento seguro de atualização do banco.

- [ ] **TASK-120 — Atualizar README.md**  
  Documentar requisitos, instalação, configuração, execução, testes e estrutura do projeto.

- [ ] **TASK-121 — Realizar validação final do MVP**  
  Executar os critérios de aceite de `requirements.md` e registrar resultados.

**Critério de conclusão:** aplicação implantada em ambiente definido, documentada e validada conforme os critérios de aceite.

---

## 18. Ordem recomendada de implementação

| Ordem | Fase | Resultado esperado |
|---:|---|---|
| 1 | Preparação | Repositório e documentação |
| 2 | Backend e banco | API e PostgreSQL configurados |
| 3 | Fundação multiempresa | Isolamento de dados implementado |
| 4 | Autenticação | Login, usuários e permissões |
| 5 | Clientes | Cadastro de clientes |
| 6 | Fornecedores | Cadastro de fornecedores |
| 7 | Ordens de serviço | Fluxo principal completo |
| 8 | Dashboard | Indicadores básicos |
| 9 | Componentes frontend | Estrutura visual reutilizável |
| 10 | Autenticação e empresa | Acesso pela interface |
| 11 | Cadastros frontend | Clientes, fornecedores e usuários |
| 12 | OS frontend | Fluxo completo pela interface |
| 13 | Qualidade | Testes e revisão de segurança |
| 14 | Implantação | MVP publicado e documentado |

## 19. Definition of Done — definição de tarefa concluída

Uma tarefa somente poderá ser marcada como concluída quando:

- [ ] A implementação atender ao escopo descrito na tarefa.
- [ ] O código seguir a organização e os padrões definidos no projeto.
- [ ] As validações necessárias estiverem implementadas no backend.
- [ ] As permissões e o isolamento multiempresa estiverem respeitados.
- [ ] Os testes relevantes tiverem sido criados ou atualizados e executados.
- [ ] Não houver erros conhecidos que impeçam o fluxo implementado.
- [ ] A documentação relacionada tiver sido atualizada, quando necessário.
- [ ] A alteração tiver sido revisada e integrada ao projeto.

## 20. Riscos e dependências

- **Isolamento multiempresa:** falhas podem expor dados de uma empresa a outra. A fundação multiempresa e seus testes são bloqueadores.
- **Autenticação:** decisão fechada em `spec.md` §20; implementar refresh tokens revogáveis antes das telas de login.
- **Numeração da OS:** contador por empresa com bloqueio de linha e teste de concorrência (`CA-MULTI-010`).
- **Escopo do MVP:** recursos como PDF, anexos, estoque, financeiro e integrações permanecem fora da primeira entrega.
- **Cadastro público:** habilitado com limite por IP; criação transacional de empresa + administrador.
- **Hospedação:** VPS com Docker Compose e HTTPS definidos em `spec.md` §18; validar backup antes da publicação.

---

**Documento:** `tasks.md`  
**Projeto:** OrdemFácil  
**Versão:** 1.2 — Fases 0 a 2 concluídas
