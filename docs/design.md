# Design — OrdemFácil

**Projeto:** OrdemFácil — Sistema Web Multiempresa de Gerenciamento de Ordens de Serviço  
**Versão:** 1.0  
**Status:** Diretrizes de UX/UI do MVP com decisões registradas  
**Documentos relacionados:** `requirements.md` e `spec.md`

---

## 1. Objetivo do documento

Este documento define as diretrizes de experiência do usuário (UX), interface (UI), navegação, identidade visual e comportamento das principais telas do OrdemFácil.

A interface deverá tornar simples a rotina de empresas que precisam cadastrar clientes, abrir ordens de serviço, acompanhar atendimentos e localizar informações rapidamente.

O design deverá ser consistente com a arquitetura multiempresa: cada usuário verá somente os dados e as informações da empresa à qual está vinculado.

## 2. Princípios de design

1. **Simplicidade:** priorizar tarefas frequentes e reduzir etapas desnecessárias.
2. **Clareza:** utilizar títulos, rótulos e mensagens objetivos.
3. **Consistência:** manter padrões de navegação, formulários, botões e tabelas.
4. **Agilidade:** facilitar a abertura e a localização de ordens de serviço.
5. **Responsividade:** oferecer uma boa experiência em computadores, tablets e smartphones.
6. **Acessibilidade:** não depender apenas de cores para transmitir informações; garantir contraste, foco visível e navegação por teclado.
7. **Segurança perceptível:** identificar a empresa e o usuário autenticado, sem expor dados de outras empresas.
8. **Feedback:** informar quando uma operação está carregando, foi concluída ou apresentou erro.

## 3. Público e contexto de uso

O sistema será utilizado por pequenas e médias empresas e profissionais autônomos que prestam serviços, incluindo assistências técnicas, oficinas e empresas de manutenção.

Os principais contextos de uso são:

- Atendente recebendo uma solicitação e abrindo uma OS.
- Administrador acompanhando o volume e a situação dos atendimentos.
- Técnico consultando suas ordens e registrando o serviço executado.
- Usuário pesquisando uma ordem antiga para recuperar informações.

A interface deverá favorecer o uso cotidiano, inclusive por pessoas com pouca familiaridade com sistemas de gestão.

## 4. Identidade visual

### 4.1 Direção visual

A identidade visual deverá transmitir organização, confiança, eficiência e simplicidade. Recomenda-se uma interface limpa, profissional e sem excesso de elementos decorativos.

### 4.2 Paleta inicial sugerida

As cores abaixo são uma proposta inicial e poderão ser refinadas após a criação do protótipo.

| Uso | Cor | Código sugerido |
|---|---|---|
| Cor primária | Azul | `#2563EB` |
| Primária escura | Azul-marinho | `#1E40AF` |
| Fundo da aplicação | Cinza muito claro | `#F8FAFC` |
| Superfícies e cartões | Branco | `#FFFFFF` |
| Texto principal | Cinza-escuro | `#0F172A` |
| Texto secundário | Cinza | `#64748B` |
| Bordas | Cinza-claro | `#E2E8F0` |
| Sucesso | Verde | `#16A34A` |
| Atenção | Âmbar | `#D97706` |
| Erro | Vermelho | `#DC2626` |
| Informação | Azul-claro | `#0284C7` |

As cores de status deverão ser acompanhadas de texto e, quando útil, de ícones. A cor não deverá ser o único meio de identificar o estado de uma OS.

### 4.3 Tipografia

Recomenda-se utilizar uma fonte sem serifa, de boa legibilidade, como Inter ou system-ui.

Hierarquia sugerida:
- Título da página: 24–28 px, peso semibold.
- Título de seção: 18–20 px, peso semibold.
- Texto de interface: 14–16 px.
- Rótulos e metadados: 12–14 px.
- Botões: 14–16 px, peso medium.

### 4.4 Ícones

Utilizar ícones simples e consistentes, preferencialmente de uma mesma biblioteca. Ícones que representem ações deverão possuir rótulos acessíveis e, quando necessário, dicas de contexto.

## 5. Estrutura geral da aplicação

### 5.1 Layout desktop

O layout principal deverá conter:

- **Barra lateral:** navegação entre os módulos.
- **Cabeçalho superior:** identificação da empresa, usuário autenticado e ações de conta.
- **Área de conteúdo:** telas, formulários, tabelas e indicadores.
- **Área de notificações:** mensagens temporárias de sucesso, alerta ou erro.

Estrutura ilustrativa:

```text
┌─────────────────────────────────────────────────────────────┐
│ OrdemFácil       Empresa: Oficina Exemplo     Usuário ▾      │
├───────────────┬─────────────────────────────────────────────┤
│               │                                             │
│  Dashboard    │  Título da página          [Ação principal] │
│  Ordens de OS │                                             │
│  Clientes     │  Conteúdo                                  │
│  Fornecedores │                                             │
│  Usuários     │                                             │
│               │                                             │
│  Configurações│                                             │
│               │                                             │
└───────────────┴─────────────────────────────────────────────┘
```

A barra lateral poderá ser recolhida para ampliar a área de conteúdo.

### 5.2 Layout mobile

Em telas pequenas:
- A navegação deverá ser recolhida em menu acessível.
- O cabeçalho deverá preservar a identificação da empresa e o acesso à conta.
- Tabelas extensas deverão ser adaptadas para cartões ou rolagem horizontal controlada.
- Formulários deverão utilizar uma coluna.
- Ações principais deverão permanecer fáceis de localizar e tocar.

## 6. Navegação e estrutura de menus

Menu principal sugerido:

| Menu | Descrição | Visibilidade |
|---|---|---|
| Dashboard | Indicadores e visão geral | Administrador e Atendente |
| Ordens de Serviço | Listagem, abertura e acompanhamento de OS | Conforme perfil |
| Clientes | Cadastro e consulta de clientes | Administrador e Atendente |
| Fornecedores | Cadastro e consulta de fornecedores | Administrador e Atendente |
| Usuários | Gerenciamento dos usuários da empresa | Administrador |
| Minha Empresa | Dados e configurações da empresa | Administrador |
| Minha Conta | Dados básicos e encerramento de sessão | Todos |

O menu deverá apresentar somente as opções compatíveis com o perfil do usuário. A autorização real continuará sendo validada pelo backend.

## 7. Telas do sistema

### 7.1 Login

**Objetivo:** permitir que o usuário acesse o ambiente da sua empresa.

Elementos:
- Marca OrdemFácil.
- Campo de e-mail.
- Campo de senha.
- Botão “Entrar”.
- Link “Esqueci minha senha” (se o fluxo de recuperação for implementado).
- Mensagem de erro para credenciais inválidas.
- Link para cadastro de empresa (auto cadastro habilitado no MVP, com proteção contra abuso).

Comportamento:
- Validar campos obrigatórios.
- Exibir estado de carregamento durante autenticação.
- Não revelar se um e-mail está cadastrado ao apresentar erros de login.
- Após autenticação, direcionar o usuário ao dashboard ou à primeira tela permitida pelo perfil.

### 7.2 Cadastro de empresa

**Objetivo:** permitir o auto cadastro de uma nova empresa e de seu primeiro administrador no MVP.

Campos sugeridos:
- Razão social ou nome do titular.
- Nome fantasia (opcional).
- CNPJ ou documento aplicável.
- E-mail de contato.
- Telefone.
- Nome do administrador.
- E-mail de acesso.
- Senha e confirmação de senha.

Comportamento:
- Criar empresa e primeiro administrador em uma única transação.
- Validar os dados antes do envio.
- Informar claramente o resultado do cadastro.
- Não permitir que o usuário selecione ou informe um `company_id` arbitrário.

O cadastro é protegido por limite de tentativas por IP; empresa, primeiro administrador e configurações iniciais são criados em uma única transação.

### 7.3 Dashboard

**Objetivo:** apresentar rapidamente a situação das ordens de serviço da empresa.

Componentes:
- Saudação ou identificação da empresa.
- Cartões de indicadores:
  - OS abertas.
  - OS em andamento.
  - OS aguardando.
  - OS concluídas.
- Lista de ordens recentes.
- Atalho para “Nova ordem de serviço”.
- Atalhos para clientes e fornecedores, quando apropriado.

Regras:
- Os indicadores deverão refletir somente os registros da empresa autenticada.
- Cada cartão poderá direcionar à listagem de OS já filtrada pelo status correspondente.
- Exibir estado vazio com orientação quando ainda não houver ordens cadastradas.
- Técnicos poderão receber uma visão simplificada com suas próprias ordens, caso o dashboard seja habilitado para esse perfil.

### 7.4 Listagem de ordens de serviço

**Objetivo:** permitir localizar e acompanhar ordens de serviço.

Elementos:
- Título “Ordens de Serviço”.
- Botão “Nova OS” para perfis autorizados.
- Campo de pesquisa por número ou cliente.
- Filtro por status.
- Filtro por período de abertura.
- Filtro por técnico, para perfis autorizados.
- Tabela ou lista de resultados.

Colunas sugeridas para desktop:
- Número da OS.
- Cliente.
- Descrição resumida.
- Técnico responsável.
- Data de abertura.
- Status.
- Ação “Visualizar”.

Comportamento:
- Utilizar paginação.
- Permitir combinar filtros.
- Informar quando não houver resultados.
- Preservar filtros ao retornar da tela de detalhes, quando possível.
- Técnicos deverão visualizar somente ordens atribuídas a eles.
- Não exibir registros de outras empresas, mesmo se o usuário alterar parâmetros da requisição.

### 7.5 Abertura de ordem de serviço

**Objetivo:** registrar uma nova solicitação de atendimento.

Campos sugeridos:
- Cliente (obrigatório, com pesquisa de clientes cadastrados).
- Título ou assunto (obrigatório).
- Descrição do problema ou solicitação (obrigatório).
- Serviço solicitado (opcional).
- Técnico responsável (opcional na abertura, conforme regra operacional).
- Observações iniciais (opcional).

Informações automáticas:
- Número da OS.
- Data e hora de abertura.
- Usuário responsável pela abertura.
- Status inicial “Aberta”.
- Empresa vinculada, obtida pelo contexto autenticado.

Comportamento:
- Validar campos obrigatórios.
- Permitir localizar e selecionar cliente existente.
- Oferecer atalho para cadastrar cliente sem perder os dados já preenchidos, se viável.
- Impedir associação de cliente pertencente a outra empresa.
- Após salvar, exibir confirmação e direcionar para os detalhes da OS.

### 7.6 Detalhes da ordem de serviço

**Objetivo:** apresentar todas as informações e ações relacionadas à OS.

Seções sugeridas:
1. **Identificação:** número, status e data de abertura.
2. **Cliente:** nome e dados de contato necessários.
3. **Solicitação:** título, descrição e serviço solicitado.
4. **Responsável:** técnico atribuído.
5. **Execução:** observações técnicas e solução aplicada.
6. **Histórico:** linha do tempo com eventos e alterações.
7. **Ações:** editar, atribuir técnico, alterar status, concluir ou cancelar, conforme permissões.

O histórico deverá apresentar:
- Evento realizado.
- Usuário responsável.
- Data e hora.
- Descrição ou observação relacionada.

A tela deverá diferenciar visualmente informações da solicitação original e registros feitos durante a execução.

### 7.7 Edição e atualização de OS

A edição deverá ser contextual e respeitar o status atual e as permissões.

- Administrador e Atendente poderão editar os campos operacionais permitidos.
- Técnico poderá registrar observações e atualizar o andamento das ordens atribuídas.
- Conclusão deverá exigir a solução aplicada.
- Cancelamento deverá exigir justificativa.
- Ações finais deverão solicitar confirmação.
- Alterações relevantes deverão gerar eventos no histórico.

### 7.8 Clientes

**Listagem:**
- Nome ou razão social.
- CPF/CNPJ parcialmente mascarado, quando exibido.
- Telefone.
- Situação.
- Ação para visualizar ou editar.

**Formulário:**
- Tipo de pessoa: Física ou Jurídica.
- Nome completo ou razão social.
- CPF/CNPJ.
- Telefone.
- E-mail.
- CEP, endereço, número, complemento, bairro, cidade e UF.
- Observações.

Comportamento:
- Exibir erros junto aos campos correspondentes.
- Normalizar documentos e telefones antes de enviar.
- Permitir inativar cadastro sem apagar o histórico de OS.
- Exibir confirmação antes de inativar.

### 7.9 Fornecedores

**Listagem:**
- Nome ou razão social.
- Documento, quando informado.
- Contato.
- Telefone.
- Situação.
- Ações disponíveis.

**Formulário:**
- Nome ou razão social.
- CPF/CNPJ, quando aplicável.
- Nome do contato.
- Telefone.
- E-mail.
- Endereço.
- Observações.

O módulo deverá seguir os mesmos padrões visuais e de interação do cadastro de clientes.

### 7.10 Usuários

**Objetivo:** permitir ao administrador gerenciar os acessos da própria empresa.

Elementos:
- Nome.
- E-mail.
- Perfil.
- Situação.
- Data de cadastro.
- Ações de edição e ativação/inativação.

Formulário:
- Nome.
- E-mail.
- Perfil: Administrador, Atendente ou Técnico.
- Senha inicial ou fluxo seguro de convite/definição de senha.
- Situação.

O administrador não deverá conseguir associar um usuário a outra empresa por meio deste formulário.

### 7.11 Minha Empresa

**Objetivo:** apresentar e permitir atualizar informações da empresa autenticada.

Campos:
- Razão social ou nome do titular.
- Nome fantasia.
- CNPJ ou documento aplicável.
- E-mail.
- Telefone.

A tela deverá exibir claramente que as informações são da empresa atual. Alterações deverão ser autorizadas somente ao perfil Administrador.

### 7.12 Minha Conta

Elementos:
- Nome do usuário.
- E-mail.
- Empresa vinculada.
- Perfil.
- Opção de alteração de senha, se implementada.
- Botão “Sair”.

## 8. Componentes reutilizáveis

A interface deverá utilizar componentes consistentes para reduzir duplicação.

| Componente | Responsabilidade |
|---|---|
| AppLayout | Estrutura geral da aplicação |
| Sidebar | Navegação principal |
| Topbar | Empresa, usuário e ações da conta |
| PageHeader | Título, descrição e ação principal |
| Button | Botões e variações de ação |
| Input | Campos de texto |
| Select | Seleção de opções |
| SearchInput | Campo de pesquisa |
| StatusBadge | Exibição textual do status |
| DataTable | Listagem tabular |
| Pagination | Navegação entre páginas |
| Modal | Confirmações e formulários curtos |
| Toast | Feedback temporário |
| EmptyState | Estado sem registros |
| LoadingState | Estado de carregamento |
| FormField | Campo com rótulo, ajuda e erro |
| Timeline | Histórico de eventos da OS |

## 9. Padrões de interação

### 9.1 Botões

- **Primário:** ação principal da tela, como “Salvar” ou “Nova OS”.
- **Secundário:** ação complementar, como “Cancelar” ou “Voltar”.
- **Perigo:** ação destrutiva ou sensível, como cancelar uma OS.
- **Ícone:** ações compactas, sempre com rótulo acessível ou descrição contextual.

### 9.2 Formulários

- Apresentar rótulos persistentes, não depender somente de placeholder.
- Identificar campos obrigatórios.
- Validar dados no frontend para melhorar a experiência.
- Revalidar tudo no backend.
- Preservar os dados preenchidos quando houver erro de validação.
- Desabilitar o botão de envio durante uma operação em andamento.
- Evitar envios duplicados.

### 9.3 Mensagens

Exemplos:
- Sucesso: “Ordem de serviço criada com sucesso.”
- Erro de validação: “Verifique os campos destacados.”
- Sem resultados: “Nenhuma ordem de serviço encontrada.”
- Confirmação: “Deseja realmente cancelar esta ordem de serviço?”
- Falha de conexão: “Não foi possível conectar ao servidor. Tente novamente.”

As mensagens não deverão expor detalhes técnicos ou dados de outras empresas.

### 9.4 Estados de tela

Todas as telas com carregamento de dados deverão prever:
- Carregando.
- Conteúdo carregado.
- Lista vazia.
- Erro de carregamento.
- Acesso não autorizado.

## 10. Responsividade

Pontos de quebra iniciais sugeridos:

| Dispositivo | Largura de referência | Comportamento |
|---|---:|---|
| Celular | Até 767 px | Menu recolhido e conteúdo em coluna |
| Tablet | 768–1023 px | Navegação compacta e tabelas adaptadas |
| Desktop | A partir de 1024 px | Sidebar e conteúdo em largura ampla |

As larguras são referências de projeto, não regras rígidas. O layout deverá ser validado em diferentes tamanhos de tela.

## 11. Acessibilidade

A interface deverá seguir boas práticas de acessibilidade, buscando conformidade com WCAG 2.2 nível AA quando viável.

Diretrizes:
- Contraste adequado entre texto e fundo.
- Navegação por teclado.
- Foco visível.
- Rótulos associados aos campos.
- Mensagens de erro compreensíveis.
- Uso semântico de títulos, listas, tabelas e botões.
- Textos alternativos para imagens informativas.
- Status identificados por texto, além da cor.
- Áreas clicáveis adequadas para toque.

## 12. Segurança e privacidade na interface

- Exibir apenas dados necessários à tarefa do usuário.
- Mascarar documentos pessoais em listagens quando não for necessário exibi-los integralmente.
- Não incluir tokens ou segredos em URLs.
- Não utilizar dados enviados pelo frontend para determinar a empresa ativa.
- Não mostrar informações de clientes, usuários ou OS de outra empresa.
- Ocultar ações não permitidas para o perfil, mantendo a validação no backend.
- Encerrar ou renovar a sessão conforme a estratégia de autenticação definida.
- Evitar mensagens que revelem a existência de registros pertencentes a outra empresa.

## 13. Conteúdo e linguagem

O sistema utilizará português do Brasil.

Padrões:
- Datas exibidas em `DD/MM/AAAA`.
- Horários em formato de 24 horas.
- Valores monetários, quando futuramente utilizados, em Real (R$).
- Telefone e documentos com formatação brasileira.
- Textos curtos, diretos e orientados à ação.
- Termos consistentes: “Ordem de Serviço”, “OS”, “Cliente”, “Fornecedor”, “Técnico” e “Status”.

## 14. Fora do escopo visual do MVP

Não serão desenhadas ou implementadas como funcionalidades operacionais na primeira versão:

- Tela de controle financeiro.
- Gestão de estoque e compras.
- Emissão de nota fiscal.
- Integração visual com WhatsApp.
- Aplicativo mobile nativo.
- Painel de administração global da plataforma SaaS.
- Gestão de planos, assinaturas e cobrança recorrente.
- Relatórios avançados e gráficos analíticos.

Um painel interno de administração da plataforma poderá ser criado futuramente, separado do ambiente das empresas clientes.

## 15. Critérios de validação do design

O design será considerado pronto para implementação quando:

1. Todas as telas do MVP estiverem representadas em wireframes ou protótipos.
2. A navegação entre as telas principais estiver definida.
3. Os fluxos de abertura, consulta, atualização, conclusão e cancelamento de OS estiverem representados.
4. Os perfis Administrador, Atendente e Técnico tiverem suas experiências consideradas.
5. A identificação da empresa estiver clara no ambiente autenticado.
6. Os estados de carregamento, erro, vazio e sucesso estiverem definidos.
7. As telas principais tiverem versões desktop e mobile.
8. Formulários e tabelas seguirem padrões consistentes.
9. O protótipo não apresentar caminhos que permitam visualizar dados de outra empresa.
10. Os critérios básicos de acessibilidade tiverem sido revisados.

## 16. Próxima etapa: prototipação

A partir deste documento, deverão ser criados wireframes e protótipos das seguintes telas, nesta ordem:

1. Login.
2. Dashboard.
3. Listagem de ordens de serviço.
4. Abertura de ordem de serviço.
5. Detalhes da ordem de serviço.
6. Cadastro e listagem de clientes.
7. Cadastro e listagem de fornecedores.
8. Gerenciamento de usuários.
9. Minha Empresa e Minha Conta.

Recomenda-se validar primeiro o fluxo completo de uma OS, pois ele representa o principal objetivo do produto. Após validar esse fluxo, os demais módulos poderão reutilizar os mesmos padrões visuais.

---

**Documento:** `design.md`  
**Projeto:** OrdemFácil  
**Versão:** 1.1 — Decisões registradas  
