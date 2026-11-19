# Acceptance Criteria — OrdemFácil

**Projeto:** OrdemFácil — Sistema Web Multiempresa de Gerenciamento de Ordens de Serviço  
**Versão:** 1.0  
**Documentos relacionados:** `requirements.md`, `spec.md`, `design.md` e `tasks.md`  
**Status:** Critérios iniciais de aceite do MVP

---

## 1. Objetivo

Este documento define os critérios objetivos que deverão ser atendidos para considerar as funcionalidades do OrdemFácil implementadas e aceitas.

Os critérios serão utilizados para:
- Validar funcionalidades manualmente.
- Orientar a criação de testes automatizados.
- Verificar o cumprimento dos requisitos.
- Apoiar a homologação do MVP.
- Evitar que funcionalidades sejam consideradas concluídas sem validação.

## 2. Regras gerais de aceite

1. Os testes deverão ser executados em ambiente de teste, com dados fictícios.
2. Cada cenário deverá registrar resultado: **Aprovado**, **Reprovado** ou **Bloqueado**.
3. Testes de autorização e isolamento multiempresa são obrigatórios.
4. A interface não substitui as validações do backend.
5. Uma funcionalidade só será aceita quando os critérios aplicáveis estiverem aprovados.
6. Erros não poderão expor senhas, tokens, stack traces, comandos SQL ou dados de outras empresas.
7. Os testes deverão contemplar respostas de sucesso, validação, ausência de permissão e falhas esperadas.
8. Os dados de teste deverão ser identificáveis e removíveis sem afetar dados reais.

## 3. Ambiente e massa de dados de teste

Preparar, no mínimo, os seguintes dados:

### 3.1 Empresas

- **Empresa A:** Oficina Alfa.
- **Empresa B:** Assistência Beta.

### 3.2 Usuários

| Usuário | Empresa | Perfil |
|---|---|---|
| Ana Administradora | Oficina Alfa | Administrador |
| Bruno Atendente | Oficina Alfa | Atendente |
| Carlos Técnico | Oficina Alfa | Técnico |
| Diana Administradora | Assistência Beta | Administrador |
| Eduardo Técnico | Assistência Beta | Técnico |

Cada usuário deverá possuir credenciais próprias e válidas.

### 3.3 Dados de negócio

- Um cliente cadastrado na Empresa A.
- Um cliente cadastrado na Empresa B.
- Um fornecedor cadastrado na Empresa A.
- Um fornecedor cadastrado na Empresa B.
- Pelo menos uma OS aberta na Empresa A.
- Pelo menos uma OS aberta na Empresa B.
- Uma OS atribuída ao Técnico Carlos.
- Uma OS atribuída ao Técnico Eduardo.

Os identificadores utilizados nos testes deverão ser conhecidos para permitir tentativas controladas de acesso cruzado.

## 4. Critérios de aceite — Fundação multiempresa

### CA-MULTI-001 — Isolamento de clientes

**Dado que** existem clientes cadastrados em duas empresas diferentes,  
**Quando** um usuário da Empresa A consultar a listagem de clientes,  
**Então** deverá visualizar somente os clientes da Empresa A.

### CA-MULTI-002 — Isolamento de fornecedores

**Dado que** existem fornecedores cadastrados em duas empresas,  
**Quando** um usuário da Empresa A consultar fornecedores,  
**Então** deverá visualizar somente os fornecedores da Empresa A.

### CA-MULTI-003 — Isolamento de ordens de serviço

**Dado que** existem ordens de serviço em duas empresas,  
**Quando** um usuário da Empresa A consultar as ordens,  
**Então** deverá visualizar somente as ordens da Empresa A.

### CA-MULTI-004 — Bloqueio de acesso por identificador

**Dado que** um usuário da Empresa A conhece o identificador de uma OS da Empresa B,  
**Quando** tentar consultar, editar, concluir ou cancelar essa OS,  
**Então** o sistema deverá negar o acesso e não revelar os dados da outra empresa.

### CA-MULTI-005 — Bloqueio de associação entre empresas

**Dado que** um usuário da Empresa A está abrindo uma OS,  
**Quando** tentar associar um cliente ou técnico pertencente à Empresa B,  
**Então** o backend deverá rejeitar a operação.

### CA-MULTI-006 — Contexto empresarial confiável

**Dado que** um usuário autenticado pertence à Empresa A,  
**Quando** enviar uma requisição manipulando o campo `company_id` para informar a Empresa B,  
**Então** o backend deverá ignorar ou rejeitar a tentativa e manter o contexto da Empresa A.

### CA-MULTI-007 — Isolamento do dashboard

**Dado que** existem ordens nas Empresas A e B,  
**Quando** cada administrador consultar o dashboard,  
**Então** os indicadores deverão considerar exclusivamente os registros da própria empresa.

### CA-MULTI-008 — Isolamento do histórico

**Dado que** uma OS possui histórico de alterações,  
**Quando** um usuário de outra empresa tentar consultar esse histórico,  
**Então** o acesso deverá ser negado.

### CA-MULTI-009 — Numeração de OS por empresa

**Dado que** duas empresas criam ordens de serviço,  
**Quando** o sistema gerar os números,  
**Então** cada empresa deverá manter sua sequência independente, sem duplicidade dentro da mesma empresa.

### CA-MULTI-010 — Teste concorrente de numeração

**Dado que** vários usuários criam OS simultaneamente na mesma empresa,  
**Quando** as operações forem processadas,  
**Então** cada OS deverá receber um número único, sem colisões ou sobrescritas.

## 5. Critérios de aceite — Autenticação e usuários

### CA-AUTH-001 — Login válido

**Dado que** um usuário está ativo e possui credenciais válidas,  
**Quando** informar e-mail e senha corretos,  
**Então** o sistema deverá autenticar o usuário e disponibilizar acesso conforme seu perfil e empresa.

### CA-AUTH-002 — Login inválido

**Dado que** um usuário informa credenciais incorretas,  
**Quando** tentar entrar no sistema,  
**Então** deverá receber mensagem genérica de falha, sem revelar se o e-mail está cadastrado.

### CA-AUTH-003 — Usuário inativo

**Dado que** um usuário está inativado,  
**Quando** tentar autenticar-se,  
**Então** o sistema deverá impedir o acesso.

### CA-AUTH-004 — Endpoint protegido

**Dado que** uma requisição é enviada sem credencial válida,  
**Quando** acessar um endpoint protegido,  
**Então** a API deverá retornar HTTP 401.

### CA-AUTH-005 — Permissão insuficiente

**Dado que** um usuário autenticado não possui permissão para determinada operação,  
**Quando** tentar executá-la,  
**Então** a API deverá retornar HTTP 403, sem realizar a alteração.

### CA-AUTH-006 — Consultar usuário atual

**Dado que** um usuário está autenticado,  
**Quando** consultar `/api/v1/auth/me`,  
**Então** deverá receber seus dados básicos, perfil e empresa, sem receber hash de senha ou segredos.

### CA-AUTH-007 — Encerramento de sessão

**Dado que** um usuário encerrou sua sessão,  
**Quando** tentar reutilizar credenciais de sessão revogadas ou expiradas,  
**Então** o acesso deverá ser negado conforme a estratégia de autenticação adotada.

### CA-AUTH-008 — Cadastro de usuário

**Dado que** um Administrador está autenticado,  
**Quando** cadastrar um usuário com dados válidos,  
**Então** o novo usuário deverá ser associado automaticamente à empresa do Administrador.

### CA-AUTH-009 — Restrição de gerenciamento

**Dado que** um Atendente ou Técnico está autenticado,  
**Quando** tentar cadastrar, editar ou inativar usuários,  
**Então** a API deverá negar a operação.

### CA-AUTH-010 — Senha protegida

**Dado que** um usuário foi cadastrado,  
**Quando** os dados forem consultados no banco,  
**Então** a senha não deverá estar armazenada em texto puro.

### CA-AUTH-011 — Perfil aplicado no backend

**Dado que** a interface oculta uma ação para determinado perfil,  
**Quando** o usuário tentar executar a mesma operação diretamente pela API,  
**Então** o backend deverá validar a permissão e impedir a operação não autorizada.

## 6. Critérios de aceite — Cadastro de clientes

### CA-CLI-001 — Cadastro válido

**Dado que** um usuário autorizado está na empresa correta,  
**Quando** informar os campos obrigatórios de um cliente,  
**Então** o sistema deverá cadastrar o cliente associado à empresa autenticada.

### CA-CLI-002 — Campos obrigatórios

**Dado que** o usuário tenta cadastrar um cliente sem nome ou tipo de pessoa,  
**Quando** enviar o formulário,  
**Então** o sistema deverá rejeitar o cadastro e indicar os campos inválidos.

### CA-CLI-003 — Tipo de pessoa

**Dado que** o usuário seleciona pessoa física ou jurídica,  
**Quando** preencher o documento,  
**Então** o sistema deverá aplicar a validação correspondente, quando o documento for informado.

### CA-CLI-004 — Documento duplicado na mesma empresa

**Dado que** já existe um cliente ativo com determinado CPF/CNPJ na Empresa A,  
**Quando** um usuário da Empresa A tentar cadastrar outro cliente com o mesmo documento,  
**Então** o sistema deverá impedir a duplicidade conforme a regra definida.

### CA-CLI-005 — Documento igual em empresas diferentes

**Dado que** um documento está cadastrado como cliente da Empresa A,  
**Quando** a Empresa B cadastrar um cliente com o mesmo documento,  
**Então** o sistema deverá permitir o cadastro, conforme o escopo de unicidade por empresa.

### CA-CLI-006 — Consulta de cliente

**Dado que** um cliente está cadastrado,  
**Quando** um usuário autorizado consultar seus detalhes,  
**Então** o sistema deverá apresentar os dados permitidos do cadastro.

### CA-CLI-007 — Edição de cliente

**Dado que** um cliente pertence à empresa autenticada,  
**Quando** um usuário autorizado alterar seus dados,  
**Então** o sistema deverá persistir as alterações.

### CA-CLI-008 — Inativação de cliente

**Dado que** um cliente possui ordens de serviço relacionadas,  
**Quando** um Administrador inativá-lo,  
**Então** o cadastro deverá permanecer armazenado e o histórico das OS deverá continuar acessível aos usuários autorizados.

### CA-CLI-009 — Cliente de outra empresa

**Dado que** um usuário tenta consultar ou editar cliente de outra empresa,  
**Quando** a API receber a solicitação,  
**Então** deverá negar o acesso sem revelar os dados do cliente.

## 7. Critérios de aceite — Cadastro de fornecedores

### CA-FOR-001 — Cadastro válido

**Dado que** um usuário autorizado informa os dados obrigatórios de fornecedor,  
**Quando** enviar o formulário,  
**Então** o fornecedor deverá ser cadastrado na empresa autenticada.

### CA-FOR-002 — Validação dos campos

**Dado que** o usuário informa e-mail inválido ou deixa campo obrigatório vazio,  
**Quando** tentar salvar,  
**Então** o sistema deverá apresentar os erros correspondentes.

### CA-FOR-003 — Consulta de fornecedores

**Dado que** existem fornecedores cadastrados,  
**Quando** um usuário autorizado abrir a listagem,  
**Então** deverá visualizar somente fornecedores da própria empresa.

### CA-FOR-004 — Edição de fornecedor

**Dado que** um fornecedor pertence à empresa autenticada,  
**Quando** um usuário autorizado atualizar os dados,  
**Então** as alterações deverão ser persistidas.

### CA-FOR-005 — Inativação de fornecedor

**Dado que** um fornecedor está ativo,  
**Quando** o Administrador solicitar sua inativação,  
**Então** o sistema deverá alterar sua situação sem apagar fisicamente o registro.

### CA-FOR-006 — Isolamento de fornecedores

**Dado que** um usuário tenta consultar ou alterar fornecedor de outra empresa,  
**Quando** a API receber a solicitação,  
**Então** deverá negar o acesso.

## 8. Critérios de aceite — Ordens de serviço

### CA-OS-001 — Abertura de OS

**Dado que** um Administrador ou Atendente está autenticado e existe um cliente ativo na mesma empresa,  
**Quando** preencher os campos obrigatórios e confirmar a abertura,  
**Então** o sistema deverá criar a OS com status `OPEN`.

### CA-OS-002 — Número único

**Dado que** uma OS foi criada,  
**Quando** o sistema concluir o cadastro,  
**Então** deverá atribuir automaticamente um número único dentro da empresa.

### CA-OS-003 — Dados automáticos

**Dado que** uma OS foi aberta,  
**Quando** seus detalhes forem consultados,  
**Então** deverão estar registrados número, data/hora de abertura, usuário responsável, empresa e status inicial.

### CA-OS-004 — Cliente obrigatório

**Dado que** o usuário tenta abrir uma OS sem cliente válido,  
**Quando** enviar a solicitação,  
**Então** o sistema deverá rejeitar a operação.

### CA-OS-005 — Cliente de outra empresa

**Dado que** o usuário tenta abrir uma OS utilizando um cliente de outra empresa,  
**Quando** enviar a solicitação,  
**Então** o backend deverá rejeitar a associação.

### CA-OS-006 — Atribuição de técnico

**Dado que** existe um usuário com perfil Técnico na mesma empresa,  
**Quando** um usuário autorizado atribuir esse técnico à OS,  
**Então** o responsável deverá ser atualizado e o evento deverá ser registrado no histórico.

### CA-OS-007 — Técnico de outra empresa

**Dado que** um usuário tenta atribuir técnico pertencente a outra empresa,  
**Quando** enviar a alteração,  
**Então** o backend deverá rejeitar a operação.

### CA-OS-008 — Listagem de OS

**Dado que** existem ordens cadastradas na empresa,  
**Quando** um usuário autorizado abrir a listagem,  
**Então** deverá visualizar as ordens dentro do seu escopo de acesso.

### CA-OS-009 — Pesquisa por número

**Dado que** existe uma OS com determinado número,  
**Quando** o usuário pesquisar pelo número,  
**Então** o sistema deverá retornar a ordem correspondente, se ela pertencer à empresa e estiver dentro de seu escopo de acesso.

### CA-OS-010 — Filtro por status

**Dado que** existem ordens com diferentes status,  
**Quando** o usuário selecionar um status,  
**Então** a listagem deverá apresentar somente as ordens correspondentes.

### CA-OS-011 — Filtro por período

**Dado que** existem ordens abertas em datas diferentes,  
**Quando** o usuário informar um período válido,  
**Então** o sistema deverá retornar somente as ordens abertas dentro do intervalo.

### CA-OS-012 — Paginação

**Dado que** existem mais registros do que o limite por página,  
**Quando** o usuário navegar entre páginas,  
**Então** o sistema deverá apresentar os resultados corretos sem duplicações ou omissões causadas pela paginação.

### CA-OS-013 — Edição de OS

**Dado que** uma OS pertence à empresa autenticada e pode ser editada,  
**Quando** um usuário autorizado atualizar seus campos permitidos,  
**Então** o sistema deverá persistir as alterações e registrar os eventos relevantes.

### CA-OS-014 — Técnico consulta OS atribuída

**Dado que** uma OS está atribuída ao Técnico Carlos,  
**Quando** Carlos consultar suas ordens,  
**Então** deverá visualizar essa OS.

### CA-OS-015 — Técnico não consulta OS de outro técnico

**Dado que** uma OS está atribuída a outro técnico da mesma empresa,  
**Quando** Carlos tentar consultá-la ou atualizá-la,  
**Então** o backend deverá negar o acesso, conforme as permissões definidas.

### CA-OS-016 — Técnico registra observação

**Dado que** uma OS está atribuída ao Técnico Carlos,  
**Quando** ele registrar uma observação técnica válida,  
**Então** a observação deverá ser salva com autoria e data/hora.

### CA-OS-017 — Transição para em andamento

**Dado que** uma OS está aberta,  
**Quando** um usuário autorizado iniciar o atendimento,  
**Então** o status deverá mudar de `OPEN` para `IN_PROGRESS`.

### CA-OS-018 — Transição para aguardando

**Dado que** uma OS está em andamento,  
**Quando** um usuário autorizado informar uma pendência e alterar o status,  
**Então** o status deverá mudar para `WAITING` e a alteração deverá constar no histórico.

### CA-OS-019 — Retorno de aguardando

**Dado que** uma OS está aguardando,  
**Quando** a pendência for resolvida e um usuário autorizado retomar o serviço,  
**Então** o status deverá mudar para `IN_PROGRESS`.

### CA-OS-020 — Conclusão exige solução

**Dado que** uma OS está em andamento,  
**Quando** um usuário tentar concluí-la sem informar a solução aplicada,  
**Então** o sistema deverá rejeitar a operação e informar o campo obrigatório.

### CA-OS-021 — Conclusão válida

**Dado que** uma OS está em andamento e possui solução aplicada,  
**Quando** um usuário autorizado concluir o serviço,  
**Então** o status deverá mudar para `COMPLETED`, a data de conclusão deverá ser registrada e o histórico atualizado.

### CA-OS-022 — Cancelamento exige justificativa

**Dado que** uma OS está em estado passível de cancelamento,  
**Quando** um usuário tentar cancelá-la sem justificativa,  
**Então** o sistema deverá rejeitar a operação.

### CA-OS-023 — Cancelamento válido

**Dado que** um Administrador possui autorização para cancelar a OS,  
**Quando** informar uma justificativa válida e confirmar,  
**Então** o status deverá mudar para `CANCELED` e o histórico deverá registrar justificativa, usuário e data/hora.

### CA-OS-024 — Bloqueio de transição inválida

**Dado que** uma OS está concluída ou cancelada,  
**Quando** um usuário tentar alterar seu status para um estado não permitido,  
**Então** o backend deverá rejeitar a operação sem modificar o registro.

### CA-OS-025 — Histórico de alterações

**Dado que** uma OS sofreu alterações relevantes,  
**Quando** um usuário autorizado consultar seu histórico,  
**Então** deverá visualizar os eventos em ordem cronológica, com usuário responsável e data/hora.

### CA-OS-026 — Histórico não editável por usuário comum

**Dado que** existem eventos registrados no histórico,  
**Quando** um usuário tentar alterá-los ou removê-los por endpoint não autorizado,  
**Então** o sistema deverá impedir a operação.

## 9. Critérios de aceite — Dashboard

### CA-DASH-001 — Indicadores por status

**Dado que** existem OS com diferentes status,  
**Quando** um Administrador ou Atendente acessar o dashboard,  
**Então** os cartões deverão apresentar os totais correspondentes à empresa autenticada.

### CA-DASH-002 — Atualização dos indicadores

**Dado que** uma OS teve seu status alterado,  
**Quando** o dashboard for atualizado,  
**Então** os indicadores deverão refletir a nova situação.

### CA-DASH-003 — Ordens recentes

**Dado que** existem ordens cadastradas,  
**Quando** o usuário acessar o dashboard,  
**Então** deverá visualizar as ordens recentes da própria empresa.

### CA-DASH-004 — Dashboard sem registros

**Dado que** uma empresa ainda não possui OS,  
**Quando** o usuário acessar o dashboard,  
**Então** o sistema deverá apresentar indicadores zerados e orientação para abrir a primeira OS.

### CA-DASH-005 — Restrição por perfil

**Dado que** um Técnico acessa o sistema,  
**Quando** tentar consultar um dashboard restrito a Administrador e Atendente,  
**Então** o comportamento deverá respeitar a política de acesso definida para esse perfil.

## 10. Critérios de aceite — Interface e experiência

### CA-UI-001 — Layout consistente

**Dado que** o usuário navega entre os módulos,  
**Quando** abrir diferentes páginas,  
**Então** deverá encontrar padrões consistentes de cabeçalho, navegação, botões, formulários e mensagens.

### CA-UI-002 — Identificação da empresa

**Dado que** um usuário está autenticado,  
**Quando** visualizar o cabeçalho ou área de conta,  
**Então** deverá identificar a empresa à qual está vinculado.

### CA-UI-003 — Navegação por perfil

**Dado que** usuários possuem perfis diferentes,  
**Quando** acessarem o menu,  
**Então** deverão visualizar somente as opções compatíveis com seus perfis.

### CA-UI-004 — Validação de formulários

**Dado que** um formulário contém campos obrigatórios,  
**Quando** o usuário tentar enviá-lo incompleto,  
**Então** a interface deverá indicar os campos que precisam ser corrigidos.

### CA-UI-005 — Feedback de sucesso

**Dado que** uma operação foi concluída,  
**Quando** a API retornar sucesso,  
**Então** a interface deverá apresentar mensagem clara e atualizar os dados exibidos.

### CA-UI-006 — Feedback de erro

**Dado que** a API retornar erro,  
**Quando** a operação não puder ser concluída,  
**Então** a interface deverá apresentar mensagem compreensível sem expor detalhes internos.

### CA-UI-007 — Estado de carregamento

**Dado que** a interface está aguardando resposta da API,  
**Quando** a operação estiver em andamento,  
**Então** deverá apresentar indicação de carregamento e evitar envios duplicados.

### CA-UI-008 — Estado vazio

**Dado que** uma listagem não possui registros,  
**Quando** o usuário acessá-la,  
**Então** deverá visualizar mensagem explicativa e, quando permitido, uma ação para criar o primeiro registro.

### CA-UI-009 — Responsividade

**Dado que** o usuário acessa o sistema em computador, tablet ou smartphone,  
**Quando** navegar pelas telas principais,  
**Então** o conteúdo deverá se adaptar sem perda de funcionalidades essenciais ou sobreposição indevida.

### CA-UI-010 — Acessibilidade por teclado

**Dado que** o usuário navega sem mouse,  
**Quando** utilizar Tab, Shift+Tab, Enter, Espaço e teclas aplicáveis,  
**Então** deverá conseguir acessar e operar os controles essenciais com foco visível.

### CA-UI-011 — Status não depende somente de cor

**Dado que** uma OS possui determinado status,  
**Quando** o status for exibido,  
**Então** deverá existir texto legível identificando a situação, além de qualquer cor ou ícone.

### CA-UI-012 — Confirmação de ações sensíveis

**Dado que** o usuário solicita cancelar uma OS ou inativar um cadastro,  
**Quando** iniciar a ação,  
**Então** a interface deverá solicitar confirmação antes de efetivá-la.

## 11. Critérios de aceite — Segurança e privacidade

### CA-SEC-001 — HTTPS em produção

**Dado que** o sistema está publicado em produção,  
**Quando** o usuário acessar a aplicação,  
**Então** a comunicação deverá ocorrer por HTTPS.

### CA-SEC-002 — Segredos fora do código

**Dado que** o projeto está versionado,  
**Quando** os arquivos forem revisados,  
**Então** não deverão conter senhas reais, chaves privadas, tokens ou credenciais de produção.

### CA-SEC-003 — CORS restrito

**Dado que** o backend está em execução,  
**Quando** uma origem não autorizada tentar realizar requisição de navegador,  
**Então** o backend não deverá permitir acesso por CORS.

### CA-SEC-004 — Erros sem informações internas

**Dado que** ocorre uma falha inesperada,  
**Quando** a API responder ao cliente,  
**Então** não deverá expor stack trace, consulta SQL, caminho de arquivo ou segredo.

### CA-SEC-005 — Proteção de documentos

**Dado que** documentos pessoais são exibidos em listagens,  
**Quando** sua exibição integral não for necessária,  
**Então** deverão ser mascarados ou omitidos conforme a política de privacidade.

### CA-SEC-006 — Auditoria

**Dado que** ocorre uma alteração relevante em uma OS,  
**Quando** a operação for concluída,  
**Então** deverá ser possível identificar o usuário responsável e a data/hora do evento.

### CA-SEC-007 — Dados mínimos

**Dado que** um formulário solicita dados pessoais,  
**Quando** o usuário realizar o cadastro,  
**Então** o sistema deverá solicitar somente os dados necessários ao fluxo definido.

### CA-SEC-008 — Backup e restauração

**Dado que** existe uma política de backup configurada,  
**Quando** for executado um teste de restauração,  
**Então** deverá ser possível recuperar o banco de dados conforme o procedimento documentado.

## 12. Critérios de aceite — Implantação e documentação

### CA-DEP-001 — Configuração por ambiente

**Dado que** o sistema será executado em ambientes diferentes,  
**Quando** as configurações forem carregadas,  
**Então** desenvolvimento, teste e produção deverão utilizar configurações separadas.

### CA-DEP-002 — Migrations

**Dado que** o banco está vazio,  
**Quando** as migrations forem executadas na ordem prevista,  
**Então** o esquema deverá ser criado sem erros.

### CA-DEP-003 — Inicialização documentada

**Dado que** um desenvolvedor novo recebe o repositório,  
**Quando** seguir o README,  
**Então** deverá conseguir configurar e executar o projeto conforme as instruções.

### CA-DEP-004 — Testes automatizados

**Dado que** o projeto possui testes automatizados,  
**Quando** a suíte essencial for executada no ambiente de teste,  
**Então** não deverão existir falhas nos testes obrigatórios do MVP.

### CA-DEP-005 — Aplicação disponível

**Dado que** a implantação foi concluída,  
**Quando** um usuário autorizado acessar o endereço publicado,  
**Então** deverá conseguir autenticar-se e executar os fluxos aceitos.

## 13. Matriz de rastreabilidade

A matriz relaciona os principais requisitos aos critérios de aceite.

| Requisito | Critérios relacionados |
|---|---|
| RF-001 e RF-002 — Autenticação | CA-AUTH-001 a CA-AUTH-007 |
| RF-003 e RF-004 — Usuários e perfis | CA-AUTH-008 a CA-AUTH-011 |
| RF-005 — Dashboard | CA-DASH-001 a CA-DASH-005 |
| RF-006 a RF-009 — Clientes | CA-CLI-001 a CA-CLI-009 |
| RF-010 a RF-013 — Fornecedores | CA-FOR-001 a CA-FOR-006 |
| RF-014 a RF-022 — Gestão de OS | CA-OS-001 a CA-OS-015 e CA-OS-017 a CA-OS-024 |
| RF-023 e RF-024 — Observações e solução | CA-OS-016, CA-OS-020 e CA-OS-021 |
| RF-025 — Histórico | CA-OS-025 e CA-OS-026 |
| RF-026 — Cancelamento | CA-OS-022 e CA-OS-023 |
| Multiempresa | CA-MULTI-001 a CA-MULTI-010 |
| Requisitos de interface | CA-UI-001 a CA-UI-012 |
| Requisitos de segurança e privacidade | CA-SEC-001 a CA-SEC-008 |
| Implantação e documentação | CA-DEP-001 a CA-DEP-005 |

## 14. Checklist de homologação do MVP

Utilizar este checklist na validação final:

### Fundação e acesso
- [ ] Duas empresas conseguem utilizar a mesma plataforma.
- [ ] Cada empresa possui seu próprio administrador.
- [ ] Usuários autenticam-se com credenciais individuais.
- [ ] Perfis e permissões são aplicados no backend.
- [ ] Não existe acesso cruzado entre empresas.

### Cadastros
- [ ] Clientes podem ser cadastrados, consultados, editados e inativados.
- [ ] Fornecedores podem ser cadastrados, consultados, editados e inativados.
- [ ] Usuários podem ser gerenciados pelo administrador da empresa.

### Ordens de serviço
- [ ] Uma OS pode ser aberta e recebe número único por empresa.
- [ ] A OS fica vinculada a cliente da mesma empresa.
- [ ] Uma OS pode receber técnico responsável da mesma empresa.
- [ ] Pesquisa, filtros e paginação funcionam.
- [ ] O técnico consulta e atualiza somente ordens atribuídas a ele.
- [ ] As transições de status respeitam as regras.
- [ ] Conclusão exige solução aplicada.
- [ ] Cancelamento exige justificativa.
- [ ] Histórico registra eventos relevantes.

### Interface e operação
- [ ] Dashboard apresenta indicadores corretos por empresa.
- [ ] Interface funciona em computador e celular.
- [ ] Formulários apresentam validações e mensagens claras.
- [ ] Estados de carregamento, erro e lista vazia estão implementados.
- [ ] A navegação por teclado funciona nas telas principais.

### Segurança e publicação
- [ ] HTTPS está configurado em produção.
- [ ] Segredos não estão versionados.
- [ ] CORS está restrito às origens autorizadas.
- [ ] Logs não expõem dados sensíveis.
- [ ] Backup e restauração foram testados.
- [ ] README contém instruções suficientes para executar o projeto.
- [ ] Testes automatizados essenciais estão aprovados.

## 15. Registro de execução dos testes

Utilizar a tabela abaixo durante a homologação.

| ID do critério | Resultado | Evidência / observação | Responsável | Data |
|---|---|---|---|---|
| CA-MULTI-001 | Pendente |  |  |  |
| CA-AUTH-001 | Pendente |  |  |  |
| CA-CLI-001 | Pendente |  |  |  |
| CA-FOR-001 | Pendente |  |  |  |
| CA-OS-001 | Pendente |  |  |  |
| CA-DASH-001 | Pendente |  |  |  |
| CA-UI-001 | Pendente |  |  |  |
| CA-SEC-001 | Pendente |  |  |  |
| CA-DEP-001 | Pendente |  |  |  |

Valores permitidos para resultado: **Aprovado**, **Reprovado**, **Bloqueado** ou **Pendente**.

## 16. Condições para aprovação do MVP

O MVP poderá ser considerado aprovado quando:

1. Todos os critérios obrigatórios de autenticação, autorização e isolamento multiempresa estiverem aprovados.
2. Os fluxos essenciais de clientes, fornecedores e ordens de serviço estiverem funcionando.
3. O ciclo de vida da OS estiver validado, incluindo conclusão e cancelamento.
4. O dashboard apresentar dados corretos e restritos à empresa autenticada.
5. Não houver defeitos críticos ou vulnerabilidades conhecidas que comprometam dados ou acesso.
6. Os testes automatizados essenciais estiverem aprovados.
7. A aplicação estiver documentada e disponível no ambiente de homologação.

Critérios não aplicáveis ou adiados deverão possuir justificativa registrada e aprovação do responsável pelo produto. Falhas de isolamento multiempresa não poderão ser aceitas como pendência para publicação.

---

**Documento:** `acceptance.md`  
**Projeto:** OrdemFácil  
**Versão:** 1.0 — Critérios iniciais de aceite do MVP
