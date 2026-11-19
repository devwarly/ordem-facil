# Requirements — OrdemFácil

**Projeto:** OrdemFácil — Sistema Web de Gerenciamento de Ordens de Serviço  
**Versão:** 1.0  
**Status:** Especificação do MVP com decisões registradas

---

## 1. Visão geral

O OrdemFácil será uma aplicação web destinada a pequenas e médias empresas e profissionais autônomos que prestam serviços. O sistema permitirá organizar clientes, fornecedores e ordens de serviço em um único ambiente, facilitando a abertura, localização, acompanhamento e conclusão dos atendimentos.

A aplicação será acessada por navegador, sem necessidade de instalação de um aplicativo nativo.

## 2. Problema que o sistema pretende resolver

Empresas prestadoras de serviços frequentemente enfrentam dificuldades para registrar atendimentos, organizar informações dos clientes, localizar ordens de serviço e acompanhar o andamento dos trabalhos.

O OrdemFácil pretende reduzir a perda e a dispersão de informações, centralizando os registros e oferecendo uma visão clara da situação de cada ordem de serviço.

## 3. Objetivos

### 3.1 Objetivo geral

Desenvolver um sistema web para gerenciar ordens de serviço, permitindo que empresas prestadoras de serviços cadastrem clientes e fornecedores, registrem solicitações, acompanhem a execução dos serviços e consultem o histórico dos atendimentos.

### 3.2 Objetivos específicos

- Centralizar o cadastro e a consulta de clientes e fornecedores.
- Padronizar a abertura e o registro das ordens de serviço.
- Facilitar a localização de ordens por número, cliente, período e status.
- Permitir o acompanhamento das etapas de execução dos serviços.
- Registrar observações técnicas e soluções aplicadas.
- Apresentar indicadores básicos para apoiar a organização dos atendimentos.

## 4. Público-alvo e perfis de usuário

O sistema será uma plataforma multiempresa destinada a pequenas e médias empresas e profissionais autônomos que realizam prestação de serviços, como assistências técnicas, oficinas, empresas de manutenção, instalação, refrigeração, climatização e serviços de informática.

### 4.1 Administrador

- Acessar todas as áreas do sistema.
- Gerenciar usuários e seus perfis de acesso.
- Cadastrar, consultar, editar e inativar clientes e fornecedores.
- Criar, consultar, editar e cancelar ordens de serviço.
- Visualizar indicadores e informações gerais.

### 4.2 Atendente

- Cadastrar e consultar clientes.
- Consultar fornecedores.
- Abrir ordens de serviço.
- Consultar e editar ordens de serviço conforme suas permissões.
- Acompanhar o andamento dos atendimentos.

### 4.3 Técnico

- Consultar as ordens de serviço atribuídas a si.
- Visualizar os dados necessários para executar o serviço.
- Registrar observações técnicas.
- Informar a solução aplicada.
- Atualizar o andamento e o status das ordens atribuídas.

> As permissões específicas de cada perfil deverão ser aplicadas no backend, e não apenas ocultadas na interface.

## 5. Escopo do MVP

A primeira versão do OrdemFácil contemplará:

1. Autenticação e controle de acesso por perfil.
2. Dashboard com indicadores básicos.
3. Cadastro e gerenciamento de clientes.
4. Cadastro e gerenciamento de fornecedores.
5. Abertura e gerenciamento de ordens de serviço.
6. Atribuição de técnico responsável.
7. Atualização do status das ordens.
8. Registro de observações e solução aplicada.
9. Pesquisa, filtros e consulta ao histórico da ordem.

### 5.1 Fora do escopo inicial

Não serão implementados no MVP:

- Aplicativo mobile nativo.
- Emissão de nota fiscal eletrônica.
- Integração com WhatsApp ou outros serviços de mensagens.
- Integração com sistemas fiscais, contábeis ou de pagamento.
- Controle financeiro completo, incluindo fluxo de caixa e contas a pagar e receber.
- Controle avançado de estoque.
- Gestão de compras.
- Relatórios gerenciais avançados.
- Operação offline.

Esses itens poderão ser avaliados em versões futuras.

## 6. Requisitos funcionais

Os requisitos funcionais descrevem as ações e os serviços que o sistema deverá oferecer.

| ID | Requisito | Descrição | Prioridade |
|---|---|---|---|
| RF-001 | Autenticar usuário | O sistema deverá permitir que usuários acessem o sistema por meio de credenciais individuais. | Alta |
| RF-002 | Encerrar sessão | O sistema deverá permitir que o usuário encerre sua sessão com segurança. | Alta |
| RF-003 | Gerenciar usuários | O administrador deverá cadastrar, consultar, editar, ativar e inativar usuários. | Alta |
| RF-004 | Definir perfil de acesso | O administrador deverá atribuir aos usuários os perfis Administrador, Atendente ou Técnico. | Alta |
| RF-005 | Exibir dashboard | O sistema deverá apresentar um resumo das ordens de serviço por status e indicadores básicos. | Alta |
| RF-006 | Cadastrar cliente | O sistema deverá permitir registrar os dados de pessoas físicas ou jurídicas. | Alta |
| RF-007 | Consultar clientes | O sistema deverá permitir listar, pesquisar e visualizar clientes cadastrados. | Alta |
| RF-008 | Editar cliente | O sistema deverá permitir atualizar os dados de um cliente. | Alta |
| RF-009 | Inativar cliente | O sistema deverá permitir inativar um cadastro sem apagar o histórico relacionado. | Média |
| RF-010 | Cadastrar fornecedor | O sistema deverá permitir registrar os dados de fornecedores. | Média |
| RF-011 | Consultar fornecedores | O sistema deverá permitir listar, pesquisar e visualizar fornecedores cadastrados. | Média |
| RF-012 | Editar fornecedor | O sistema deverá permitir atualizar os dados de um fornecedor. | Média |
| RF-013 | Inativar fornecedor | O sistema deverá permitir inativar fornecedores sem apagar registros históricos relacionados. | Baixa |
| RF-014 | Abrir ordem de serviço | O sistema deverá permitir criar uma OS vinculada a um cliente. | Alta |
| RF-015 | Gerar número da OS | O sistema deverá gerar um identificador único para cada ordem de serviço. | Alta |
| RF-016 | Registrar dados da OS | O sistema deverá permitir informar descrição da solicitação, serviço solicitado, observações e datas pertinentes. | Alta |
| RF-017 | Atribuir técnico | O sistema deverá permitir associar um técnico responsável à ordem de serviço. | Alta |
| RF-018 | Consultar ordens de serviço | O sistema deverá apresentar uma listagem das ordens cadastradas. | Alta |
| RF-019 | Pesquisar e filtrar OS | O sistema deverá permitir localizar ordens por número, cliente, status e período. | Alta |
| RF-020 | Visualizar detalhes da OS | O sistema deverá apresentar os dados completos de uma ordem de serviço. | Alta |
| RF-021 | Editar ordem de serviço | O sistema deverá permitir atualizar os dados da OS conforme as permissões do usuário e as regras de negócio. | Alta |
| RF-022 | Atualizar status da OS | O sistema deverá permitir alterar o status de uma ordem conforme o fluxo definido. | Alta |
| RF-023 | Registrar observações técnicas | O técnico deverá poder adicionar observações relacionadas à execução do serviço. | Alta |
| RF-024 | Registrar solução aplicada | O técnico deverá poder descrever o serviço executado e a solução aplicada. | Alta |
| RF-025 | Consultar histórico da OS | O sistema deverá manter e exibir o histórico de alterações e atualizações da ordem. | Alta |
| RF-026 | Cancelar OS | O administrador deverá poder cancelar uma OS, registrando a justificativa. | Média |

### 6.1 Dados previstos para os cadastros

**Cliente**
- Tipo: pessoa física ou pessoa jurídica.
- Nome completo ou razão social.
- CPF ou CNPJ.
- Telefone.
- E-mail.
- Endereço.
- Observações.
- Situação do cadastro: ativo ou inativo.

**Fornecedor**
- Nome ou razão social.
- CPF ou CNPJ, quando aplicável.
- Nome do contato.
- Telefone.
- E-mail.
- Endereço.
- Observações.
- Situação do cadastro: ativo ou inativo.

**Ordem de serviço**
- Número único da OS.
- Cliente relacionado.
- Data e hora de abertura.
- Descrição do problema ou solicitação.
- Serviço solicitado.
- Técnico responsável.
- Status.
- Observações.
- Data de conclusão, quando aplicável.
- Solução aplicada, quando concluída.
- Histórico de alterações.

## 7. Fluxo e regras de negócio das ordens de serviço

### 7.1 Status previstos

O MVP utilizará os seguintes status:

- **Aberta:** ordem registrada e aguardando início do atendimento.
- **Em andamento:** serviço em execução.
- **Aguardando:** serviço temporariamente pendente, por exemplo, aguardando peça, informação ou autorização.
- **Concluída:** serviço finalizado.
- **Cancelada:** ordem encerrada sem execução ou continuidade do serviço.

### 7.2 Regras de negócio

| ID | Regra |
|---|---|
| RN-001 | Toda ordem de serviço deverá possuir um número único, gerado automaticamente. |
| RN-002 | Toda OS deverá estar vinculada a um cliente cadastrado. |
| RN-003 | A OS deverá ser criada inicialmente com o status **Aberta**. |
| RN-004 | Uma OS poderá ter um técnico responsável, conforme a disponibilidade e a organização da empresa. |
| RN-005 | Toda alteração de status deverá ser registrada no histórico, com usuário responsável e data e hora. |
| RN-006 | Uma OS somente poderá ser marcada como concluída quando as informações de conclusão exigidas estiverem preenchidas. |
| RN-007 | O cancelamento deverá exigir uma justificativa e registrar o usuário responsável e a data e hora. |
| RN-008 | Clientes e fornecedores relacionados a registros existentes não deverão ser excluídos fisicamente; deverão ser inativados. |
| RN-009 | Técnicos deverão visualizar e atualizar somente as ordens permitidas para seu perfil, especialmente as que estiverem atribuídas a eles. |
| RN-010 | O sistema deverá impedir que usuários sem permissão executem operações restritas. |

As transições permitidas entre status deverão ser detalhadas na especificação técnica. O sistema deverá evitar alterações incoerentes, como reabrir uma OS cancelada sem uma regra explícita para isso.

## 8. Requisitos não funcionais

Os requisitos não funcionais definem características de qualidade, segurança e operação do sistema.

| ID | Requisito | Descrição | Prioridade |
|---|---|---|---|
| RNF-001 | Aplicação web | O sistema deverá funcionar em navegadores modernos, sem exigir instalação local. | Alta |
| RNF-002 | Responsividade | A interface deverá adaptar-se a computadores, tablets e smartphones. | Alta |
| RNF-003 | Usabilidade | A interface deverá ser simples, intuitiva e apresentar mensagens claras ao usuário. | Alta |
| RNF-004 | Segurança de autenticação | As senhas deverão ser armazenadas utilizando algoritmo seguro de hash, nunca em texto puro. | Alta |
| RNF-005 | Controle de acesso | O backend deverá validar as permissões de cada usuário antes de executar operações protegidas. | Alta |
| RNF-006 | Proteção de dados | O sistema deverá adotar medidas para proteger dados pessoais e observar a LGPD, incluindo isolamento dos dados entre empresas. | Alta |
| RNF-007 | Integridade | O banco de dados deverá aplicar restrições e relacionamentos para preservar a consistência dos registros. | Alta |
| RNF-008 | Desempenho | As telas e consultas comuns deverão responder em tempo adequado para o volume de dados esperado no MVP. | Média |
| RNF-009 | Manutenibilidade | O código deverá ser organizado em módulos, com separação entre interface, API e acesso a dados. | Alta |
| RNF-010 | Disponibilidade | O sistema deverá estar hospedado em ambiente acessível pela internet, sujeito à disponibilidade da infraestrutura contratada. | Média |
| RNF-011 | Compatibilidade | A aplicação deverá funcionar nas versões atuais dos principais navegadores. | Média |
| RNF-012 | Backup | Deverá existir uma estratégia de cópia de segurança do banco de dados. | Alta |
| RNF-013 | Auditoria | Operações relevantes deverão manter informações de autoria e data/hora para rastreabilidade. | Alta |

## 9. Tecnologias inicialmente previstas

| Camada | Tecnologia | Responsabilidade |
|---|---|---|
| Frontend | HTML5 | Estrutura das páginas. |
| Frontend | CSS3 | Estilização e responsividade. |
| Frontend | JavaScript | Interatividade e comunicação com a API. |
| Backend | Python | Linguagem de programação do servidor. |
| Backend | FastAPI | Construção da API REST e implementação das regras de negócio. |
| Banco de dados | PostgreSQL | Armazenamento persistente dos dados. |

A arquitetura prevista separa a interface web, a API backend e o banco de dados. A comunicação entre frontend e backend ocorrerá por requisições HTTP, com troca de dados em JSON.

Bibliotecas adicionais, ORM, estratégia de autenticação, hospedagem e ferramentas de implantação serão definidos durante o detalhamento técnico.

## 10. Entidades principais previstas

As entidades abaixo representam uma visão inicial do domínio. O modelo de dados definitivo será elaborado na etapa de modelagem.

- **Usuário:** credenciais, identificação, perfil e situação de acesso.
- **Cliente:** dados de pessoas físicas ou jurídicas atendidas.
- **Fornecedor:** dados de empresas ou profissionais fornecedores.
- **Ordem de Serviço:** identificação, cliente, descrição, datas, status e responsável.
- **Histórico da OS:** alterações de status, observações, autor e data/hora.

Relacionamentos iniciais esperados:

- Um cliente poderá possuir várias ordens de serviço.
- Um técnico poderá ser responsável por várias ordens de serviço.
- Uma ordem de serviço poderá possuir vários registros de histórico.
- Um usuário poderá realizar várias alterações registradas no histórico.
- Fornecedores poderão ser cadastrados e consultados independentemente das ordens de serviço no MVP.

## 11. Critérios de aceite do MVP

O MVP será considerado funcional quando:

1. Um usuário conseguir autenticar-se e acessar somente as funcionalidades permitidas ao seu perfil.
2. O administrador conseguir cadastrar e gerenciar usuários.
3. Um usuário autorizado conseguir cadastrar, consultar e editar clientes.
4. Um usuário autorizado conseguir cadastrar e consultar fornecedores.
5. Um atendente ou administrador conseguir abrir uma OS vinculada a um cliente.
6. Cada OS receber automaticamente um número único.
7. O usuário conseguir consultar e localizar OS por número, cliente, status e período.
8. Um usuário autorizado conseguir atribuir um técnico e atualizar o status da OS.
9. O técnico conseguir registrar observações e a solução aplicada nas ordens permitidas.
10. O sistema conseguir apresentar o histórico das alterações relevantes de uma OS.
11. O dashboard apresentar informações coerentes com os registros existentes.
12. A interface funcionar adequadamente em computador e dispositivo móvel.
13. As permissões e validações forem aplicadas também no backend.
14. Os dados permanecerem armazenados corretamente após o encerramento da sessão.

## 12. Decisões registradas para o MVP

- **Modelo de utilização:** plataforma multiempresa com isolamento lógico por `company_id`; cada usuário pertence a uma única empresa no MVP (ver `spec.md` §7).
- **Cadastro de usuários:** o administrador da empresa cria os usuários; o primeiro administrador é criado junto com a empresa; convite por e-mail fica fora do MVP.
- **Cadastro de empresa:** habilitado no MVP com proteção contra abuso e criação transacional de empresa + primeiro administrador.
- **Atribuição de técnicos:** no máximo um técnico responsável por OS.
- **Fluxo de status:** estados e transições definidos em `spec.md` §9; reabertura de OS concluída ou cancelada não é permitida no MVP.
- **Anexos:** fora do MVP.
- **Impressão/PDF:** fora do MVP.
- **Dados obrigatórios:** cliente exige nome e tipo de pessoa; OS exige cliente, título e descrição; conclusão exige solução aplicada; cancelamento exige justificativa.
- **Exclusão e retenção:** clientes e fornecedores são inativados, nunca excluídos fisicamente quando houver histórico; anonimização e política formal de retenção ficam fora do MVP e devem ser aprovadas pelo controlador antes da produção.

## 13. Evoluções possíveis

Após a validação do MVP, poderão ser consideradas:

- Geração de PDF e impressão da ordem de serviço.
- Anexos de imagens e documentos.
- Envio de notificações por e-mail ou WhatsApp.
- Orçamentos vinculados às ordens de serviço.
- Controle de peças e estoque.
- Controle financeiro e de pagamentos.
- Relatórios gerenciais.
- Avaliação de satisfação do cliente.
- Suporte a múltiplas empresas e unidades.

---

**Documento:** `requirements.md`  
**Projeto:** OrdemFácil  
**Versão:** 1.1 — Decisões registradas
