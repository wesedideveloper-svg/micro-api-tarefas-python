~~# Registro dos principais prompts de desenvolvimento

Este documento registra os prompts cujo texto original está disponível na conversa e os resultados observados. As transcrições preservam o texto enviado pelo usuário. As instruções de `AGENTS.md` permanecem no próprio arquivo.

**Data do registro:** 12/10/2026. A data individual de envio dos prompts anteriores não está disponível; a data deste registro não deve ser interpretada como a data desses envios.

Autorização para realizar uma etapa não equivale à validação humana de seu resultado. Quando não há revisão explícita registrada, a validação é indicada como pendente.

## Etapa 0 — Idioma da comunicação

**Data:** envio não informado; registrado em 12/10/2026.

**Objetivo:** definir português do Brasil para a comunicação.

**Prompt original:**

```text
Primeiro portugues-brasil. pergunta e resposta ou msg de aguarde ou carregando ok.
```

**Resultado obtido:** o assistente confirmou o uso de português do Brasil nas respostas, perguntas e mensagens de andamento.

**Validação humana:** preferência expressamente definida pelo usuário; não há avaliação posterior específica registrada.

**Refinamentos realizados:** nenhum registrado.

## Etapa 1 — Planejamento da arquitetura e da implementação

**Data:** envio não informado; registrado em 12/10/2026.

**Objetivo:** planejar o projeto sem modificar arquivos nem implementar funcionalidades.

**Prompt original:**

```text
Atue como um engenheiro de software sênior especializado em Python, FastAPI e arquitetura de APIs REST.

Estamos desenvolvendo o projeto acadêmico `micro-api-tarefas-python`.

Leia integralmente os arquivos `README.md` e `AGENTS.md` antes de responder.

**Sua tarefa nesta etapa é apenas planejar. Não crie, altere ou exclua arquivos. Não execute comandos.**

Apresente:

1. Sua compreensão dos objetivos e requisitos do projeto.
2. Uma proposta de estrutura de diretórios e arquivos.
3. A responsabilidade de cada camada: API, Service, Repository e SQLite.
4. As dependências Python necessárias e suas finalidades.
5. A sequência recomendada de implementação, dividida em pequenas etapas.
6. Os pontos que precisam de decisão ou esclarecimento antes da implementação.

Respeite o escopo acadêmico e priorize simplicidade, organização, testes e documentação.

Aguarde minha aprovação antes de implementar qualquer alteração.
```

**Resultado obtido:** inicialmente, o assistente informou que não poderia ler o README local com as ferramentas disponíveis sem executar um comando e solicitou seu conteúdo. Após o refinamento abaixo, leu integralmente os dois arquivos e apresentou os seis itens solicitados: objetivos, estrutura, camadas, dependências, sequência incremental e decisões pendentes. Nenhum arquivo foi alterado nessa etapa.

**Validação humana:** o usuário posteriormente autorizou iniciar apenas a estrutura mínima FastAPI, considerando o planejamento discutido. Não há aprovação explícita registrada para todas as decisões propostas sobre CRUD, persistência ou IA.

**Refinamentos realizados:** autorização de comandos exclusivamente de leitura, com o seguinte texto original:

```text
Autorizo a execução de comandos exclusivamente de leitura para consultar os arquivos do projeto.

Leia integralmente `README.md` e `AGENTS.md`, localizados na raiz do projeto `micro-api-tarefas-python`.

Você pode utilizar comandos como `pwd`, `ls` e `cat` para localizar e ler esses arquivos.

Restrições:
- Não criar, alterar ou excluir arquivos.
- Não instalar dependências.
- Não executar comandos que modifiquem o projeto.
- Não realizar commits.

Após a leitura, apresente os seis itens do planejamento solicitados anteriormente, considerando FastAPI, SQLite, SQLAlchemy, Swagger UI e integração com IA.

Aguarde minha aprovação antes de implementar qualquer funcionalidade.
```

## Etapa 2 — Aplicação mínima FastAPI e Swagger UI

**Data:** envio não informado; registrado em 12/10/2026.

**Objetivo:** criar a aplicação mínima, o endpoint de saúde, a documentação interativa e um teste automatizado.

**Prompt original:**

```text
Atue como um engenheiro de software sênior especializado em Python e FastAPI.

Vamos iniciar a implementação do projeto acadêmico `micro-api-tarefas-python`.

Leia os arquivos `README.md` e `AGENTS.md` e considere o planejamento que já discutimos.

**Objetivo desta etapa:** criar a estrutura mínima da aplicação FastAPI e disponibilizar a documentação interativa Swagger UI.

**Requisitos:**

1. Criar o pacote `app` com os arquivos `__init__.py` e `main.py`.
2. Configurar uma instância FastAPI com título "Micro-API de Gerenciamento de Tarefas", versão "0.1.0" e descrição do projeto.
3. Criar o endpoint `GET /health`, retornando `{"status": "ok"}`.
4. Disponibilizar a documentação Swagger UI em `/docs` e a especificação OpenAPI em `/openapi.json`.
5. Criar o arquivo `requirements.txt` contendo apenas as dependências necessárias nesta etapa, compatíveis com Python 3.10.
6. Criar um teste automatizado simples para o endpoint `/health`, utilizando Pytest e TestClient.
7. Criar `requirements-dev.txt` com as dependências necessárias para executar esse teste.

**Restrições:**

- Não implementar o CRUD de tarefas ainda.
- Não configurar SQLite ou SQLAlchemy nesta etapa.
- Não integrar nenhum provedor de IA.
- Não modificar `README.md`, `AGENTS.md` ou `.gitignore`.
- Não executar commits.
- Não adicionar funcionalidades fora do escopo.
- Manter o código simples e organizado.

Você está autorizado a criar os arquivos necessários e executar comandos para instalar dependências no ambiente virtual `.venv` e validar a aplicação e seus testes.

Ao finalizar, apresente os arquivos criados, os comandos executados, os resultados dos testes e as instruções para iniciar a API.

Não avance para a próxima etapa sem minha aprovação.
```

**Resultado obtido:**

- Criados `app/__init__.py`, `app/main.py`, `requirements.txt`, `requirements-dev.txt` e `tests/test_health.py`.
- Configurados título, versão e descrição da aplicação, `GET /health`, `/docs` e `/openapi.json`.
- Instaladas na `.venv` as dependências diretas FastAPI 0.115.12, Uvicorn 0.34.2, Pytest 8.3.5 e HTTPX 0.28.1, além das dependências transitivas.
- Em Python 3.10.12, a execução final do Pytest resultou em **1 teste aprovado e 1 aviso de depreciação** interno do Starlette/AnyIO.
- A verificação adicional com TestClient confirmou HTTP 200 em `/docs` e `/openapi.json`, presença do Swagger UI, metadados da aplicação e `/health` na especificação.
- `pip check` não detectou dependências incompatíveis.
- Fornecidas instruções para iniciar a API com `.venv/bin/python -m uvicorn app.main:app --reload`.
- Não foram implementados CRUD, SQLite, SQLAlchemy ou integração com IA. Os arquivos protegidos não foram modificados e nenhum commit foi realizado.

**Validação humana:** em 12/10/2026, o usuário confirmou visualmente o funcionamento da aplicação em ambiente local:

- O endpoint `GET /health` retornou `{"status":"ok"}`.
- O Swagger UI foi acessado em `http://127.0.0.1:8000/docs`.
- O endpoint `GET /health` apareceu corretamente na documentação Swagger.

A validação manual de funcionamento foi concluída. A revisão detalhada do código-fonte permanece pendente. Os testes automatizados foram executados com sucesso pelo Codex.

**Refinamentos realizados:** a instalação inicial falhou por falta de acesso ao índice de pacotes no ambiente restrito; a repetição com acesso de rede foi concluída. A primeira execução do teste ficou sem resposta no ambiente restrito e foi interrompida; a repetição fora dessa restrição, com limite de tempo, passou. Não houve novo prompt do usuário nem alteração de escopo para essas tentativas.

## Etapa 3 — Registro dos prompts acadêmicos

**Data:** registrado em 12/10/2026.

**Objetivo:** documentar os principais prompts disponíveis e os resultados conhecidos, sem alterar a aplicação.

**Prompt original:**

```text
Leia README.md e AGENTS.md.

Crie o diretório docs e o arquivo docs/prompts.md para registrar os principais prompts utilizados no desenvolvimento acadêmico.

Organize o documento por etapas, contendo:
- Data
- Objetivo
- Prompt original
- Resultado obtido
- Validação humana
- Refinamentos realizados, quando houver

Registre os prompts anteriores somente quando seu texto original estiver disponível. Não invente prompts nem resultados.

Não altere os arquivos da aplicação nem implemente novas funcionalidades nesta etapa.

Apresente as alterações realizadas para minha revisão. Não realize commit.
```

**Resultado obtido:** lidos integralmente `README.md` e `AGENTS.md`; criado `docs/prompts.md`, organizado por etapas, com transcrições dos prompts disponíveis e indicação das limitações de data e validação humana. Nenhum arquivo da aplicação foi alterado nesta etapa.

**Validação humana:** pendente de revisão deste documento pelo usuário.

**Refinamentos realizados:** nenhum registrado até a criação deste documento.

## Etapa 2.1 — Enums de status e prioridade das tarefas

**Data:** registrado em 12/10/2026.

**Objetivo:** definir os valores permitidos de status e prioridade, usando `str` e `Enum` com compatibilidade com Python 3.10, em uma entrega independente da implementação de schemas e persistência.

**Prompt original:**

```text
Estamos iniciando a Etapa 2.1 do projeto acadêmico micro-api-tarefas-python.

Leia README.md, AGENTS.md e docs/prompts.md.

O planejamento da modelagem foi aprovado, mas decidimos separar as funcionalidades em pequenas entregas, cada uma com seu próprio commit.

Nesta etapa, implemente exclusivamente:

1. Criar app/enums.py.
2. Definir TaskStatus com os valores pendente e concluida.
3. Definir TaskPriority com os valores baixa, media e alta.
4. Utilizar str e Enum, mantendo compatibilidade com Python 3.10.
5. Criar tests/test_task_enums.py para validar os valores dos enums.
6. Atualizar docs/prompts.md com o registro desta etapa, incluindo o prompt, os resultados e os testes efetivamente executados.

Restrições:

- Não criar schemas Pydantic.
- Não implementar SQLAlchemy ou SQLite.
- Não criar Repository, Service ou endpoints CRUD.
- Não alterar README.md, AGENTS.md ou app/main.py.
- Não realizar commit.

Execute os testes automatizados, incluindo o teste existente de /health.

Ao finalizar, apresente os arquivos criados ou alterados, os resultados dos testes e o git status.

Aguarde minha revisão e aprovação antes de continuar.
```

**Resultado obtido:**

- Criado `app/enums.py` com `TaskStatus.PENDENTE = "pendente"`, `TaskStatus.CONCLUIDA = "concluida"`, `TaskPriority.BAIXA = "baixa"`, `TaskPriority.MEDIA = "media"` e `TaskPriority.ALTA = "alta"`. As duas classes herdam de `str` e `Enum` da biblioteca padrão.
- Criado `tests/test_task_enums.py` com testes parametrizados para os conjuntos de valores permitidos, herança de `str` e `Enum`, correspondência entre membros e valores, construção por valor e rejeição de valores inválidos.
- Executado `timeout 15s .venv/bin/python -m pytest -q` no ambiente restrito: a execução ficou sem resposta e terminou com código 124, por limite de tempo. Essa tentativa não forneceu resultado de aprovação ou reprovação dos testes.
- Executado `timeout 30s .venv/bin/python -m pytest -q` fora dessa restrição: **10 testes aprovados em 0,32 s**, incluindo os nove casos dos enums e o teste existente de `/health`.
- Emitido um aviso de depreciação interno do Starlette/AnyIO sobre o alias `anyio.abc.BlockingPortal`, sem falhas nos testes.
- Não foram instaladas dependências, criados schemas, configurada persistência ou implementadas camadas e endpoints de tarefas. `README.md`, `AGENTS.md` e `app/main.py` não foram alterados. Nenhum commit foi realizado.

**Validação humana:** o usuário aprovou o planejamento da modelagem. Os arquivos app/enums.py e tests/test_task_enums.py foram posteriormente revisados com auxílio do ChatGPT. A implementação dos enums e os testes foram considerados corretos e adequados ao escopo acadêmico. A execução do Pytest apresentou 10 testes aprovados, incluindo /health. A Etapa 2.1 foi aprovada para commit.

**Refinamentos realizados:** a suíte foi repetida fora do ambiente restrito após a primeira tentativa atingir o limite de tempo. Não houve alteração de código motivada por falha de teste nem ampliação do escopo.

## Etapa 2.2 — Schemas Pydantic v2 das tarefas

**Data:** registrado em 12/10/2026.

**Objetivo:** implementar os contratos de criação, atualização parcial e resposta das tarefas, reutilizando os enums existentes, com validações e testes automatizados.

**Prompt original:**

```text
Estamos iniciando a Etapa 2.2 do projeto acadêmico micro-api-tarefas-python.

Leia integralmente README.md, AGENTS.md, app/enums.py e docs/prompts.md.

A Etapa 2.1 foi concluída, revisada e registrada no commit 3cb5aea.

Implemente exclusivamente os schemas Pydantic v2 e seus testes automatizados.

1. Criar app/schemas.py com:
   - TaskCreate
   - TaskUpdate
   - TaskResponse

2. Reutilizar TaskStatus e TaskPriority definidos em app/enums.py.

3. Aplicar as seguintes regras:

   TaskCreate:
   - titulo obrigatório, entre 3 e 150 caracteres após trim.
   - descricao opcional, até 2.000 caracteres, com trim e texto vazio convertido para None.
   - prioridade padrão media.
   - status não pode ser informado; toda tarefa nova será pendente.
   - id não pode ser informado.

   TaskUpdate:
   - Permitir atualização parcial de titulo, descricao, status e prioridade.
   - Distinguir campos omitidos de campos enviados como null.
   - descricao=null permite remover a descrição.
   - titulo, status e prioridade não podem receber null.
   - Rejeitar atualização sem campos.

   TaskResponse:
   - Retornar id, titulo, descricao, status e prioridade.
   - Configurar from_attributes=True.
   - Validar id como inteiro positivo.

4. Rejeitar campos desconhecidos com extra="forbid".

5. Criar tests/test_task_schemas.py com testes para valores válidos, inválidos, limites, valores padrão, atualização parcial e serialização.

6. Se necessário, declarar explicitamente Pydantic v2 em requirements.txt, preservando a compatibilidade com Python 3.10.

7. Atualizar docs/prompts.md registrando o prompt original, as alterações realizadas, os resultados dos testes e a validação humana como pendente.

Restrições:
- Não implementar SQLAlchemy ou SQLite.
- Não criar Repository, Service ou endpoints CRUD.
- Não alterar app/main.py, app/enums.py, README.md, AGENTS.md ou .gitignore.
- Não realizar commit.
- Não implementar funcionalidades adicionais.

Execute todos os testes automatizados, incluindo os existentes de enums e /health.

Ao finalizar, apresente:
- Arquivos criados ou alterados.
- Principais decisões técnicas.
- Resultados dos testes.
- Git status.

Aguarde minha revisão antes de avançar.
```

**Resultado obtido:**

- Criado `app/schemas.py` com `TaskCreate`, `TaskUpdate` e `TaskResponse`, reutilizando `TaskStatus` e `TaskPriority`.
- Definidas validações compartilhadas de título (3 a 150 caracteres após trim) e descrição (até 2.000 caracteres após trim, com texto vazio convertido em `None`).
- `TaskCreate` exige título e aplica prioridade `media` e descrição `None` por padrão. Não contém campos `id` ou `status`, que são rejeitados como extras; a definição do status pendente na criação efetiva ficará para a futura camada de negócio.
- `TaskUpdate` aceita campos omitidos, rejeita `null` explícito em título, status e prioridade e rejeita atualização vazia. `descricao=None` permite limpar a descrição. `model_fields_set` e `model_dump(exclude_unset=True)` preservam a distinção entre campo omitido e valor explicitamente enviado.
- `TaskResponse` exige os cinco campos, aceita descrição nula, usa `from_attributes=True` e valida o ID como inteiro estritamente positivo, rejeitando conversões de texto, booleanos e números fracionários.
- Os três schemas usam `extra="forbid"`. A serialização JSON produz os valores textuais dos enums.
- Criado `tests/test_task_schemas.py` com 94 casos, incluindo entradas válidas e inválidas, limites após trim, valores padrão, campos desconhecidos, atualização parcial, limpeza da descrição, resposta por atributos e serialização JSON.
- Adicionado `pydantic==2.14.1` a `requirements.txt`, declarando como dependência direta a versão v2 já instalada na `.venv` com Python 3.10. Não foi necessário instalar dependências.
- Executado `.venv/bin/python -m pytest -q tests/test_task_schemas.py`: **94 testes aprovados em 0,33 s**.
- Executado `.venv/bin/python -m pip check`: nenhuma incompatibilidade de dependências detectada.
- Executado `timeout 30s .venv/bin/python -m pytest -q` fora do ambiente restrito, devido ao comportamento do TestClient observado nas etapas anteriores: **104 testes aprovados em 0,53 s**, incluindo os 94 casos dos schemas, os nove casos dos enums e `/health`.
- A suíte completa apresentou um aviso de depreciação interno do Starlette/AnyIO sobre `anyio.abc.BlockingPortal`, sem falhas.
- Não foram implementados SQLAlchemy, SQLite, Repository, Service ou endpoints CRUD. Os arquivos protegidos não foram alterados e nenhum commit foi realizado.

**Validação humana:** concluída em 12/10/2026. O usuário revisou os arquivos app/schemas.py e tests/test_task_schemas.py com auxílio do ChatGPT.

A revisão confirmou que os schemas atendem aos requisitos de criação, atualização parcial e resposta das tarefas, incluindo validação dos campos, normalização dos textos, tratamento de valores null, distinção entre campos omitidos e informados explicitamente, rejeição de campos desconhecidos e serialização JSON.

A implementação foi considerada adequada ao escopo acadêmico, sem necessidade de alterações no código dos schemas.

O Codex informou a aprovação inicial de 104 testes automatizados, incluindo 94 testes dos schemas, nove dos enums e um do endpoint /health.

A Etapa 2.2 foi aprovada para commit, considerando também a revisão complementar realizada posteriormente.

**Refinamentos realizados:** o requisito de tamanho mínimo do título passou de um caractere, proposto no planejamento inicial, para três caracteres, conforme o prompt de implementação.

Após a primeira revisão humana, foi solicitada uma revisão complementar da cobertura dos testes, com atenção especial à distinção entre campos omitidos e null, validações após normalização dos textos e serialização parcial.

Foram acrescentados dez casos de teste e reforçada uma verificação existente, elevando o total da suíte de 104 para 114 testes aprovados, conforme execução informada pelo Codex.

Não houve necessidade de alterar app/schemas.py nem de ampliar o escopo funcional da etapa.

### Revisão complementar da Etapa 2.2 — Cobertura dos schemas

**Data:** registrado em 12/10/2026.

**Objetivo:** revisar os schemas e reforçar apenas lacunas reais da cobertura, sem duplicar testes nem alterar a implementação sem defeito comprovado.

**Prompt original:**

```text
Antes de finalizar a Etapa 2.2, faça uma revisão complementar dos arquivos app/schemas.py e tests/test_task_schemas.py.

Objetivo: reforçar a cobertura dos testes, mantendo o código simples e evitando alterações desnecessárias.

Verifique especialmente:

1. A distinção entre campos omitidos e campos enviados explicitamente como null no TaskUpdate.
2. A rejeição de null para titulo, status e prioridade.
3. A aceitação de descricao=null para remover a descrição.
4. A conversão de descricao contendo somente espaços para None.
5. A validação do titulo após remover espaços, incluindo valores nos limites.
6. A rejeição de campos desconhecidos nos três schemas.
7. A serialização correta usando model_dump(exclude_unset=True).

Regras:
- Identifique quais cenários já possuem testes e quais realmente precisam de novos testes.
- Não duplique testes existentes.
- Altere app/schemas.py somente se encontrar um defeito comprovado.
- Não implemente novas funcionalidades.
- Não altere endpoints, banco de dados ou enums.
- Execute a suíte completa de testes.
- Atualize docs/prompts.md com esta revisão complementar, os resultados e a indicação de que a validação humana final ainda está pendente.
- Não realize commit.

Ao finalizar, apresente os testes adicionados, eventuais correções e o resultado completo do Pytest.

Aguarde minha aprovação antes de avançar.
```

O prompt foi acompanhado de uma referência ao arquivo `tests/test_task_schemas.py` no editor.

**Resultado obtido:**

- Confirmada a cobertura já existente de campos omitidos versus `null`, rejeição de `null` em título/status/prioridade, descrição nula e vazia, limites válidos do título após trim, campos desconhecidos nos três schemas e atualização parcial serializada com `exclude_unset=True`.
- Ampliado o teste parametrizado de títulos inválidos para incluir dois caracteres e 151 caracteres cercados de espaços em `TaskCreate` e `TaskUpdate`: quatro casos adicionais.
- Estendido o teste existente de normalização e limite da descrição a `TaskResponse`: cinco casos adicionais, incluindo `None`, texto vazio, somente espaços/tabulação/quebra de linha, trim e limite de 2.000 caracteres.
- Reforçado o teste existente de atualização parcial com uma asserção de `model_dump(exclude_unset=True)` no modo Python, além da verificação já existente no modo JSON.
- Adicionado `test_update_dump_preserves_normalized_and_explicit_default_values`: verifica que o dump parcial contém os textos já normalizados e mantém status `pendente` e prioridade `media` explicitamente enviados.
- Não foi identificado defeito comprovado; `app/schemas.py` permaneceu sem alterações nesta revisão. Apenas `tests/test_task_schemas.py` e este documento foram alterados nesta revisão.
- Executado `timeout 30s .venv/bin/python -m pytest -q` fora do ambiente restrito, conforme a limitação do TestClient observada anteriormente: **114 testes aprovados em 0,51 s**, sendo 104 casos dos schemas, nove dos enums e um de `/health`.
- A suíte apresentou um aviso de depreciação interno do Starlette/AnyIO sobre o alias `anyio.abc.BlockingPortal`, sem falhas. Nenhum commit foi realizado.

**Validação humana:** concluída em 12/10/2026. O usuário solicitou uma revisão complementar dos testes para reforçar a cobertura de campos omitidos, valores null, normalização de textos, limites de validação e serialização de atualizações parciais.

O Codex identificou que os principais cenários já estavam cobertos e acrescentou dez casos de teste, além de reforçar uma verificação existente de model_dump(exclude_unset=True).

Não foram identificados defeitos que exigissem alterações em app/schemas.py.

O Codex informou a execução da suíte completa com 114 testes aprovados, sendo 104 dos schemas, nove dos enums e um do endpoint /health, com um aviso de depreciação interno do Starlette/AnyIO, sem falhas.

A implementação e os cenários apresentados foram revisados com auxílio do ChatGPT e considerados adequados. A revisão complementar foi aprovada para commit.

Situação final da Etapa 2.2: aprovada para commit, sem funcionalidades pendentes dentro do escopo definido.

**Refinamentos realizados:** acrescentados dez casos aos testes de schemas e uma asserção aos casos existentes de atualização parcial. Os cenários já cobertos foram reaproveitados, sem duplicação de funções de teste e sem mudança de funcionalidades.

## Etapa 2.3 — Persistência inicial com SQLAlchemy e SQLite

**Data:** registrado em 12/10/2026.

**Objetivo:** configurar a persistência inicial e o modelo tipado Task, com restrições de integridade e testes isolados, sem inicialização automática na aplicação.

**Prompt original:**

```text
Estamos iniciando a Etapa 2.3 do projeto acadêmico micro-api-tarefas-python.

Leia integralmente README.md, AGENTS.md, app/enums.py, app/schemas.py, requirements.txt e docs/prompts.md.

A Etapa 2.2 foi concluída, revisada e registrada no commit efa2e85.

Objetivo: implementar exclusivamente a camada inicial de persistência com SQLAlchemy 2.x e SQLite, mantendo a arquitetura simples, organizada e compatível com Python 3.10.12.

**1. Configuração do banco de dados**

- Criar app/database.py.
- Configurar o SQLAlchemy 2.x com SQLite.
- Utilizar uma variável DATABASE_URL configurável, com valor padrão apontando para um arquivo SQLite local do projeto.
- Configurar engine, sessionmaker e Base declarativa.
- Preparar uma função get_db() para fornecer e encerrar corretamente as sessões.
- Não criar conexão ou tabelas como efeito colateral da importação dos módulos.
- Não adicionar inicialização automática do banco em app/main.py.
- Garantir que o arquivo SQLite gerado não seja versionado no Git.

**2. Modelo de tarefas**

Criar app/models.py com a classe Task, utilizando SQLAlchemy 2.x e mapeamento tipado com Mapped e mapped_column.

Campos:

- id: inteiro, chave primária, gerado automaticamente.
- titulo: string obrigatória, máximo de 150 caracteres.
- descricao: texto opcional, máximo de 2.000 caracteres.
- status: obrigatório, padrão "pendente".
- prioridade: obrigatória, padrão "media".

Reutilizar TaskStatus e TaskPriority definidos em app/enums.py.

A persistência dos enums deve utilizar seus valores textuais ("pendente", "concluida", "baixa", "media", "alta"), e não os nomes dos membros Python.

Adicionar restrições SQLite CHECK para garantir:
- Valores válidos de status e prioridade.
- Título não vazio e com tamanho entre 3 e 150 caracteres.
- Descrição nula ou com até 2.000 caracteres.

Evitar duplicar validações complexas já implementadas nos schemas Pydantic. As restrições do banco devem proteger a integridade dos dados.

**3. Testes automatizados**

Criar tests/test_task_models.py.

Utilizar banco SQLite temporário e isolado para os testes, sem modificar o banco de desenvolvimento.

Testar:
- Criação da estrutura de tabelas.
- Persistência e recuperação de uma tarefa.
- Geração automática do ID.
- Valores padrão de status e prioridade.
- Descrição opcional.
- Persistência dos valores textuais dos enums.
- Rejeição de status e prioridade inválidos pelo banco.
- Restrições de título e descrição.
- Funcionamento das sessões e isolamento dos testes.

Não criar testes dependentes de dados persistidos anteriormente.

**4. Dependências e documentação**

- Adicionar SQLAlchemy 2.x ao requirements.txt, mantendo compatibilidade com Python 3.10.
- Atualizar docs/prompts.md com o prompt original, arquivos criados, decisões técnicas e resultados reais dos testes.
- Registrar a validação humana como pendente.
- Atualizar .gitignore somente se necessário para impedir o versionamento do banco SQLite.

**5. Restrições**

- Não criar Repository ou Service.
- Não implementar endpoints CRUD.
- Não modificar app/main.py, app/enums.py ou app/schemas.py.
- Não implementar integração com IA.
- Não criar migrações com Alembic nesta etapa.
- Não alterar README.md ou AGENTS.md.
- Não realizar commit.
- Não implementar funcionalidades adicionais.

**6. Validação**

Execute a suíte completa de testes, incluindo:
- Testes dos modelos SQLAlchemy.
- Testes dos schemas Pydantic.
- Testes dos enums.
- Teste do endpoint /health.

Execute também:
- pip check
- git diff --check
- git status

Ao finalizar, apresente:
1. Arquivos criados ou alterados.
2. Código e decisões principais da configuração SQLite e do modelo Task.
3. Quantidade de testes aprovados e eventuais avisos.
4. Resultado do git status.
5. Possíveis riscos ou pontos que exigem revisão humana.

Aguarde minha revisão e aprovação antes de avançar para a próxima etapa.
```

**Resultado obtido e decisões técnicas:**

- Criado `app/database.py` com `DATABASE_URL` lida do ambiente, padrão SQLite no arquivo `tarefas.db` da raiz, usando caminho absoluto derivado da localização do módulo. Configurados engine, `SessionLocal` com `autoflush=False` e `Base` declarativa.
- Configurado `check_same_thread=False` para o uso posterior de sessões SQLite nas dependências síncronas do FastAPI. Isso não autoriza compartilhar a mesma sessão entre requisições.
- `get_db()` fornece uma sessão por chamada e a encerra com gerenciador de contexto, inclusive em caso de erro; não realiza commit automático. O encerramento reverte transações não confirmadas.
- A criação da engine é lazy: não há abertura de conexão nem criação de tabelas na importação. Nenhuma inicialização foi acrescentada em `app/main.py`; o banco de desenvolvimento não foi criado pelos testes.
- Criado `app/models.py` com a tabela `tasks` e mapeamento `Mapped`/`mapped_column`. ID inteiro é gerado pelo SQLite; título é obrigatório e descrição é anulável.
- Enums usam `values_callable`, `native_enum=False` e `create_constraint=True`: armazenam valores textuais e geram restrições CHECK. Status e prioridade têm defaults no ORM e no banco (`pendente` e `media`), protegendo também inserções por SQL direto.
- Adicionados CHECKs para título com tamanho de 3 a 150 após `trim` do SQLite e máximo de 150 caracteres armazenados; descrição nula ou com até 2.000 caracteres. A normalização completa das entradas permanece nos schemas: o `trim` padrão do SQLite remove espaços comuns nas extremidades, não reproduz integralmente o `strip()` do Python para todos os caracteres de espaço.
- Criado `tests/test_task_models.py` com 32 casos. Cada caso usa arquivo SQLite próprio em `tmp_path`, cria suas tabelas explicitamente e descarta a engine ao terminar. Incluídos testes de estrutura, recuperação por nova sessão, IDs, defaults ORM e SQL, descrição opcional, todas as combinações dos enums, CHECKs e NOT NULL via SQL direto, limites, encerramento normal e com erro das sessões, rollback de dados não confirmados, isolamento e importação sem conexão em subprocesso.
- Adicionado `SQLAlchemy==2.0.44` a `requirements.txt` e instalado na `.venv` com `.venv/bin/python -m pip install --no-cache-dir -r requirements.txt`, com acesso de rede. O ambiente utiliza Python 3.10.12.
- `.gitignore` já contém `*.db`, `*.sqlite` e `*.sqlite3`; não foi alterado. `git check-ignore tarefas.db` confirmou que o arquivo padrão está ignorado. Um caminho personalizado de banco deve conservar uma dessas extensões ou ter regra própria de exclusão.

**Testes e verificações executados:**

- `timeout 30s .venv/bin/python -m pytest -q`, fora da restrição que afetou o TestClient nas etapas anteriores: **146 testes aprovados em 1,68 s**, sendo 32 da persistência, 104 dos schemas, nove dos enums e um de `/health`.
- Um aviso de depreciação interno do Starlette/AnyIO sobre `anyio.abc.BlockingPortal`, sem falhas.
- `.venv/bin/python -m pip check`: nenhuma incompatibilidade detectada.
- `git diff --check`: sem erros.
- `git status --short` antes da atualização deste registro: `requirements.txt` modificado e `app/database.py`, `app/models.py`, `tests/test_task_models.py` novos. A atualização deste registro também modifica `docs/prompts.md`.
- Os arquivos protegidos não foram alterados. Nenhum commit foi realizado.

**Validação humana:** concluída. O usuário revisou `app/database.py`, `app/models.py` e `tests/test_task_models.py` com auxílio do ChatGPT. A implementação e os testes foram considerados adequados ao escopo acadêmico. Nenhum defeito obrigatório foi identificado. A revisão complementar resultou em 147 testes aprovados, conforme execução informada pelo Codex. A Etapa 2.3 foi aprovada para commit.

**Refinamentos realizados:** não foram necessárias correções após a primeira execução da suíte completa. A criação explícita das tabelas ficou restrita aos bancos temporários de teste; a inicialização futura do banco de desenvolvimento dependerá de etapa aprovada separadamente.

### Revisão complementar da Etapa 2.3 — Testes de persistência

**Data:** registrado em 12/10/2026.

**Objetivo:** revisar encerramento de sessões, rollback, validação de enums via ORM, isolamento dos bancos temporários e ausência de efeitos colaterais na importação, acrescentando apenas cobertura necessária.

**Prompt original:**

```text
Antes de finalizar a Etapa 2.3, faça uma revisão complementar de app/database.py, app/models.py e tests/test_task_models.py.

Objetivo: verificar possíveis lacunas na cobertura dos testes de persistência, mantendo a implementação simples.

Verifique especialmente:

1. Se os testes demonstram corretamente o encerramento das sessões criadas por get_db(), tanto no fluxo normal quanto em caso de exceção.
2. Se o rollback de dados não confirmados está suficientemente coberto.
3. O comportamento do SQLAlchemy ao persistir valores inválidos de status e prioridade via ORM, diferenciando validação do ORM e restrições CHECK do SQLite.
4. Se os testes de isolamento realmente utilizam bancos temporários independentes.
5. Se a importação de app.database e app.models permanece sem abrir conexões ou criar tabelas.

Regras:
- Reaproveite os testes existentes.
- Adicione somente os casos que realmente faltarem.
- Não duplique cenários já cobertos.
- Não altere app/database.py ou app/models.py sem encontrar um defeito comprovado.
- Não crie Repository, Service ou endpoints CRUD.
- Não altere os schemas Pydantic ou enums.
- Execute a suíte completa de testes.
- Atualize docs/prompts.md com o prompt original, as alterações e os resultados, mantendo a validação humana final como pendente.
- Não realize commit.

Ao finalizar, apresente os testes adicionados, eventuais correções e o resultado completo do Pytest.

Aguarde minha aprovação antes de avançar.
```

O prompt foi acompanhado de uma referência ao arquivo `tests/test_task_models.py` no editor.

**Resultado obtido:**

- A cobertura existente já comprovava devolução da conexão e rollback de dados inseridos por `flush()` sem commit, tanto no encerramento normal de `get_db()` quanto ao propagar uma exceção. Esse mesmo teste foi reforçado com um spy que executa o `Session.close()` real e comprova sua chamada única, além de verificar ausência de transação ativa e identity map vazio após o encerramento.
- Acrescentados dois casos parametrizados em `test_invalid_enum_via_orm_is_rejected_by_sqlite_check`, para status e prioridade. A configuração atual não ativa `validate_strings=True`: atribuir uma string inválida ao modelo não gera validação antecipada. O `flush()` envia a inserção ao SQLite, que rejeita o valor com `IntegrityError`; os testes verificam a mensagem de CHECK e o nome da restrição. Após rollback explícito, confirmam ausência de tarefa persistida.
- Os testes existentes de SQL direto permanecem cobrindo CHECKs e NOT NULL sem interferência do ORM; os novos casos exercitam um caminho diferente, de inserção via ORM.
- Substituídos os dois casos parametrizados de isolamento por um único teste que demonstra diretamente dois arquivos SQLite temporários diferentes: confirma o caminho do banco da fixture, insere dados em ambos e verifica que cada um contém apenas sua própria tarefa. As engines são descartadas ao término.
- Reaproveitado o teste de importação em subprocesso, acrescentando uma proteção que falha caso `MetaData.create_all()` seja chamado. Mantida a proteção contra abertura de conexão e a verificação de que o arquivo SQLite não foi criado.
- Não foi encontrado defeito comprovado: `app/database.py` e `app/models.py` não foram alterados nesta revisão. Apenas `tests/test_task_models.py` e este documento foram alterados nesta solicitação.
- Executado `timeout 30s .venv/bin/python -m pytest -q` fora da restrição que afetou o TestClient anteriormente: **147 testes aprovados em 1,79 s**, sendo 33 casos da persistência, 104 dos schemas, nove dos enums e um de `/health`.
- Emitido um aviso de depreciação interno do Starlette/AnyIO sobre `anyio.abc.BlockingPortal`, sem falhas. Nenhum commit foi realizado.

**Validação humana:** concluída. `app/database.py`, `app/models.py` e `tests/test_task_models.py` foram revisados com auxílio do ChatGPT. A implementação e os testes, incluindo os reforços da revisão complementar, foram considerados adequados ao escopo acadêmico. Nenhum defeito obrigatório foi identificado. A revisão complementar resultou em 147 testes aprovados, conforme execução informada pelo Codex. A Etapa 2.3 e sua revisão complementar foram aprovadas para commit.

**Refinamentos realizados:** dois novos casos para enums inválidos via ORM; reforço dos testes existentes de sessão e importação; substituição de dois casos de isolamento por uma demonstração direta de bancos independentes. O total passou de 146 para 147 testes, sem alteração funcional da implementação.

## Etapa 2.4 — Repository de tarefas

**Data:** registrado em 12/10/2026.

**Objetivo:** implementar exclusivamente as operações de persistência de tarefas, usando a sessão fornecida pelo chamador e preservando seu controle sobre as transações.

**Prompt original:**

```text
Estamos iniciando a Etapa 2.4 do projeto acadêmico micro-api-tarefas-python.

Leia integralmente README.md, AGENTS.md, docs/prompts.md, app/database.py, app/models.py, app/enums.py e app/schemas.py antes de implementar.

A Etapa 2.3 foi concluída, revisada e registrada no commit 8fe44e3.

**Objetivo:** implementar exclusivamente a camada Repository para operações de persistência de tarefas com SQLAlchemy 2.x e SQLite, mantendo compatibilidade com Python 3.10.12.

### 1. Estrutura

Criar:
- app/repositories/__init__.py
- app/repositories/task_repository.py
- tests/test_task_repository.py

### 2. Repository

Implementar a classe TaskRepository, recebendo uma Session do SQLAlchemy pelo construtor.

Disponibilizar as operações:

- create: inserir uma tarefa a partir dos dados validados de TaskCreate e retornar o modelo Task.
- get_by_id: consultar pelo ID e retornar Task ou None.
- list_all: listar tarefas, com ordenação determinística por ID crescente.
- update: atualizar uma tarefa existente usando TaskUpdate, respeitando model_dump(exclude_unset=True), inclusive descricao=None para remover a descrição.
- delete: excluir uma tarefa existente.

Regras importantes:

- Não criar engine ou SessionLocal dentro do Repository.
- Não abrir nem fechar a sessão recebida.
- Não realizar commit ou rollback dentro do Repository; o controle da transação ficará para a futura camada Service.
- Utilizar session.add(), session.flush(), session.get(), select() e session.delete() quando apropriado.
- Não retornar schemas HTTP; retornar modelos SQLAlchemy ou resultados simples.
- Não implementar regras de negócio nesta camada.
- Não criar abstrações genéricas desnecessárias.
- Não implementar paginação, filtros ou busca por título nesta etapa.

### 3. Testes

Criar testes automatizados utilizando bancos SQLite temporários e independentes.

Validar:

1. Criação de tarefa e geração de ID após flush.
2. Aplicação dos valores padrão.
3. Consulta por ID existente e inexistente.
4. Listagem vazia e listagem ordenada por ID crescente.
5. Atualização parcial de título, descrição, status e prioridade.
6. Distinção entre campo omitido e descricao=None.
7. Exclusão de tarefa existente.
8. Comportamento para tarefa inexistente, conforme o contrato escolhido e documentado.
9. Ausência de commit automático: verificar que alterações não confirmadas são revertidas ao encerrar a sessão.
10. Persistência após commit explícito feito pelo teste.
11. Isolamento entre os bancos de teste.

Não duplicar desnecessariamente os testes dos schemas Pydantic ou das restrições do modelo SQLAlchemy já implementados nas etapas anteriores.

### 4. Restrições

- Não modificar app/main.py, app/database.py, app/models.py, app/enums.py ou app/schemas.py sem encontrar um defeito comprovado e justificar previamente.
- Não implementar Service ou endpoints CRUD.
- Não criar inicialização automática do banco.
- Não integrar IA.
- Não adicionar dependências sem necessidade.
- Não alterar README.md ou AGENTS.md.
- Não realizar commit.
- Não implementar funcionalidades fora do escopo.

### 5. Documentação

Atualizar docs/prompts.md com:

- Prompt original desta etapa.
- Arquivos criados.
- Decisões técnicas.
- Resultados reais dos testes.
- Validação humana pendente.
- Refinamentos realizados, se houver.

### 6. Verificações

Execute:

- A suíte completa de testes com Pytest.
- pip check.
- git diff --check.
- git status.

Ao finalizar, apresente:

1. Arquivos criados ou modificados.
2. Código e decisões principais do Repository.
3. Quantidade de testes aprovados e eventuais avisos.
4. Resultado do git status.
5. Possíveis riscos que exigem revisão humana.

**Aguarde minha revisão e aprovação antes de criar qualquer commit ou avançar para a próxima etapa.**
```

**Arquivos criados:** `app/repositories/__init__.py`, `app/repositories/task_repository.py` e `tests/test_task_repository.py`. Este documento foi atualizado; os arquivos protegidos e as dependências permaneceram intactos.

**Decisões técnicas:**

- `TaskRepository(session)` recebe uma sessão já existente, sem criar engine, abrir ou fechar sessões. Nenhum método chama commit ou rollback.
- `create(data: TaskCreate) -> Task` usa `model_dump()`, `session.add()` e `session.flush()`. O flush gera o ID e aplica os defaults já definidos no modelo, sem confirmar a transação.
- `get_by_id(task_id: int) -> Task | None` usa `session.get()`.
- `list_all() -> list[Task]` usa `select(Task).order_by(Task.id)`, com ordenação crescente e determinística.
- `update(task_id: int, data: TaskUpdate) -> Task | None` consulta pelo ID, aplica somente `model_dump(exclude_unset=True)` e executa flush. Campo omitido é preservado; `descricao=None` remove a descrição. ID inexistente retorna `None`, sem erro HTTP ou regra de negócio.
- `delete(task_id: int) -> bool` consulta pelo ID, usa `session.delete()` e flush; retorna `True` se excluiu e `False` se a tarefa não existe.
- Os retornos são modelos SQLAlchemy ou resultados simples. Não foram adicionados filtros, paginação, Service, endpoints ou inicialização automática.
- Erros de persistência são propagados: a futura camada Service deverá decidir commit ou rollback e tratar os erros. O flush opera sobre a sessão recebida, portanto também pode enviar outras alterações pendentes da mesma sessão; o chamador deve controlar sua unidade de trabalho.

**Resultado obtido e testes executados:**

- Criados 20 casos de teste com bancos SQLite individuais em `tmp_path`, sessões com `autoflush=False` e descarte das engines ao terminar.
- Cobertos criação com ID/defaults e dados explícitos, consulta existente/inexistente, listagem vazia/ordenada, cinco casos de atualização parcial incluindo limpeza da descrição, atualização inexistente, exclusão existente/inexistente e isolamento entre dois bancos temporários.
- Seis casos parametrizados verificam criação, atualização e exclusão com ou sem commit explícito do teste, consultando por nova sessão após o encerramento da sessão de escrita.
- Um teste impede chamadas a commit, rollback e close da sessão pelo Repository durante suas operações. Os testes não repetem os limites dos schemas ou os CHECKs já cobertos nas etapas anteriores.
- Executado `timeout 30s .venv/bin/python -m pytest -q` fora da restrição que afetou o TestClient anteriormente: **167 testes aprovados em 1,81 s**, sendo 20 do Repository, 33 da persistência, 104 dos schemas, nove dos enums e um de `/health`.
- Um aviso de depreciação interno do Starlette/AnyIO sobre `anyio.abc.BlockingPortal`, sem falhas.
- `.venv/bin/python -m pip check`: nenhuma incompatibilidade detectada.
- `git diff --check`: sem erros.
- `git status --short`: `docs/prompts.md` modificado, `app/repositories/` e `tests/test_task_repository.py` novos. Nenhum commit foi realizado.

**Validação humana:** concluída. O usuário revisou a Etapa 2.4 com auxílio do ChatGPT. `app/repositories/task_repository.py` e `tests/test_task_repository.py` foram considerados adequados ao escopo acadêmico. Nenhum defeito obrigatório foi encontrado no Repository. O usuário autorizou o commit após o refinamento do teste de controle da sessão e a aprovação das verificações; a suíte repetida apresentou 167 testes aprovados. A Etapa 2.4 foi aprovada para commit.

**Refinamentos realizados:** ajustado exclusivamente `test_repository_does_not_manage_received_session` para limitar os mocks de `commit`, `rollback` e `close` ao bloco `monkeypatch.context()`. Os métodos originais são restaurados ao sair do bloco, inclusive em caso de exceção, antes da limpeza normal da fixture. Os mocks continuam lançando erro se o Repository chamar esses métodos e agora também têm verificações explícitas de `assert_not_called()`. Nenhum caso foi adicionado ou removido, e o Repository não foi alterado.

Após o refinamento, executados `timeout 30s .venv/bin/python -m pytest -q`, `.venv/bin/python -m pip check` e `git diff --check`. Resultado: **167 testes aprovados em 1,88 s**, com um aviso de depreciação interno do Starlette/AnyIO e sem falhas; nenhuma incompatibilidade de dependências ou erro no diff. O commit autorizado deve conter somente `app/repositories/__init__.py`, `app/repositories/task_repository.py`, `tests/test_task_repository.py` e `docs/prompts.md`, com a mensagem `feat: adiciona repository de tarefas`.

## Etapa 2.5 — Service de tarefas e controle de transações

**Data:** registrado em 12/10/2026.

**Objetivo:** implementar exclusivamente o Service, reutilizando o Repository e controlando commit, rollback e a exceção de tarefa inexistente, sem dependência de HTTP.

**Prompt original:**

```text
Estamos iniciando a Etapa 2.5 do projeto acadêmico micro-api-tarefas-python.

Leia integralmente README.md, AGENTS.md, docs/prompts.md, app/database.py, app/models.py, app/schemas.py, app/enums.py e app/repositories/task_repository.py.

A Etapa 2.4 foi concluída, revisada e registrada no commit 23f242f, com 167 testes aprovados.

**Objetivo:** implementar exclusivamente a camada Service, responsável pelas operações de negócio e pelo controle de transações, mantendo compatibilidade com Python 3.10.12.

### 1. Estrutura

Criar:
- app/services/__init__.py
- app/services/task_service.py
- tests/test_task_service.py

### 2. TaskService

Implementar uma classe TaskService que receba uma Session do SQLAlchemy pelo construtor e utilize TaskRepository internamente.

Disponibilizar os métodos:

- create(data: TaskCreate) -> Task
- get_by_id(task_id: int) -> Task
- list_all() -> list[Task]
- update(task_id: int, data: TaskUpdate) -> Task
- delete(task_id: int) -> None

Regras:

1. O Service deve reutilizar o Repository, sem duplicar consultas SQL.
2. create, update e delete devem executar commit() somente após a operação ser concluída com sucesso.
3. Em caso de erro durante operações de escrita, executar rollback() e propagar a exceção.
4. Após create e update, garantir que o objeto retornado esteja consistente com os dados persistidos.
5. get_by_id e list_all não devem executar commit().
6. Para tarefa inexistente, get_by_id, update e delete devem lançar uma exceção específica da aplicação, por exemplo TaskNotFoundError, definida na camada Service ou em um módulo simples de exceções.
7. Não lançar HTTPException dentro do Service. A conversão para HTTP 404 ficará para a futura camada API.
8. Manter as regras de validação nos schemas Pydantic e as operações SQL no Repository.
9. Não abrir nem fechar a Session recebida pelo Service.
10. Não implementar novas regras de negócio não previstas no projeto.

### 3. Testes

Criar testes automatizados com SQLite temporário, sem utilizar o banco de desenvolvimento.

Cobrir:

- Criação de tarefa com commit e persistência.
- Consulta por ID existente e inexistente.
- Listagem vazia e listagem ordenada.
- Atualização parcial e persistência após commit.
- Remoção da descrição com descricao=None.
- Exclusão e persistência da exclusão.
- Exceção específica para tarefa inexistente.
- Rollback quando ocorrer erro em create, update ou delete.
- Ausência de commit em operações de leitura.
- Garantia de que o Service não fecha a sessão.
- Isolamento entre os testes.

Evitar duplicar desnecessariamente testes já existentes dos schemas, modelos e Repository.

### 4. Restrições

- Não alterar app/main.py.
- Não implementar endpoints CRUD.
- Não modificar Repository, modelos, schemas, enums ou configuração do banco sem defeito comprovado e justificativa.
- Não implementar integração com IA.
- Não criar migrações ou novas dependências sem necessidade.
- Não alterar README.md ou AGENTS.md.
- Não realizar commit.
- Não implementar funcionalidades fora do escopo.

### 5. Documentação

Atualizar docs/prompts.md com o prompt original, arquivos criados, decisões técnicas, resultados reais dos testes e validação humana pendente.

### 6. Verificações

Execute:
- Suíte completa com Pytest.
- pip check.
- git diff --check.
- git status.

Ao finalizar, apresente os arquivos criados ou modificados, decisões técnicas, quantidade de testes aprovados, eventuais avisos e possíveis riscos para revisão humana.

**Aguarde minha revisão e aprovação antes de realizar qualquer commit ou avançar para a próxima etapa.**
```

**Arquivos criados:** `app/services/__init__.py`, `app/services/task_service.py` e `tests/test_task_service.py`. Este documento foi atualizado. Nenhum arquivo das camadas anteriores ou dependência foi alterado.

**Decisões técnicas:**

- `TaskService(session)` recebe uma sessão existente e instancia `TaskRepository` com essa mesma sessão. Não abre ou fecha sessões e não executa consultas SQL diretamente.
- `create`, `update` e `delete` chamam a operação do Repository e somente então confirmam a transação com `commit()`.
- `create` e `update` executam `refresh()` após commit, para retornar o modelo com os dados persistidos carregados, mesmo com a expiração padrão do SQLAlchemy após commit.
- Erros nas operações de escrita levam a `rollback()` e são propagados com `raise`, sem conversão para HTTP.
- `TaskNotFoundError`, definida no mesmo módulo do Service, contém `task_id` e mensagem em português. `get_by_id`, `update` e `delete` lançam essa exceção quando o Repository indica ausência de tarefa. Update/delete inexistentes não fazem commit e passam pelo rollback das escritas.
- `get_by_id` e `list_all` delegam ao Repository e não executam commit.
- Validações continuam nos schemas e o tratamento dos campos omitidos continua no Repository. Não foram acrescentadas regras de negócio, endpoints, inicialização automática, IA ou migrações.
- O Service controla a transação inteira da sessão recebida: outras alterações pendentes também podem ser confirmadas ou revertidas. Recomenda-se uma sessão por unidade de trabalho.
- Após o refinamento abaixo, uma falha de `refresh()` posterior a um commit bem-sucedido é propagada sem executar rollback. Os dados já confirmados permanecem persistidos. Essa limitação deve ser considerada na futura camada API; não há promessa de atomicidade entre commit e leitura posterior.

**Resultado obtido e verificações executadas:**

- Criados 20 casos com SQLite temporário por teste, `autoflush=False`, sessões gerenciadas pelas fixtures e descarte das engines ao terminar.
- Cobertos criação/persistência, consulta existente, exceção específica nos três métodos por ID, listagem vazia/ordenada, leituras sem commit, atualização parcial e remoção da descrição, exclusão persistida e isolamento entre bancos temporários.
- Seis casos parametrizados simulam falhas após a operação real do Repository (com flush já executado) ou no commit, para criação, atualização e exclusão. Verificam chamada de rollback, preservação da exceção original, ausência de commit prematuro e dados originais confirmados por nova sessão. Também verificam que a sessão continua utilizável após rollback.
- Dois casos verificam a ordem commit/refresh e os dados retornados para create/update. Outro caso impede `close()` durante os cinco métodos do Service. Todos os patches ficam em `monkeypatch.context()`, restaurando os métodos antes da limpeza das fixtures.
- Executado `timeout 30s .venv/bin/python -m pytest -q`, fora da restrição que afetou o TestClient anteriormente: **187 testes aprovados em 2,57 s**, sendo 20 do Service, 20 do Repository, 33 da persistência, 104 dos schemas, nove dos enums e um de `/health`.
- Um aviso de depreciação interno do Starlette/AnyIO sobre `anyio.abc.BlockingPortal`, sem falhas.
- `.venv/bin/python -m pip check`: nenhuma incompatibilidade detectada.
- `git diff --check`: sem erros.
- `git status --short`: `docs/prompts.md` modificado, `app/services/` e `tests/test_task_service.py` novos. Nenhum commit foi realizado.

**Validação humana:** concluída. O usuário revisou `app/services/task_service.py` e `tests/test_task_service.py`, considerou os 20 testes iniciais adequados e solicitou o refinamento abaixo. Após o refinamento no tratamento de `refresh()` e os 189 testes aprovados, aprovou a revisão humana final da Etapa 2.5 e autorizou o commit com a mensagem `feat: adiciona camada service de tarefas`.

**Refinamentos realizados:** não foram necessárias correções após a primeira execução da suíte completa. Nenhuma alteração nas camadas existentes foi necessária.

### Refinamento da Etapa 2.5 — Falhas no refresh após commit

**Data:** registrado em 12/10/2026.

**Objetivo:** separar falhas da operação de escrita e do commit das falhas de leitura posteriores à confirmação da transação.

**Prompt original:**

```text
A revisão humana dos arquivos app/services/task_service.py e tests/test_task_service.py foi realizada.

Os 20 testes existentes foram considerados adequados. Antes da aprovação final da Etapa 2.5, realizar somente o seguinte refinamento:

1. Em TaskService.create() e TaskService.update(), manter repository e commit dentro do try/except, mas mover session.refresh(task) para depois do bloco de tratamento de exceções.
2. Preservar rollback e propagação da exceção em falhas do Repository ou do commit.
3. Adicionar dois testes simulando falha no refresh(), um para create e outro para update.
4. Confirmar que a exceção original do refresh é propagada e que a operação já confirmada permanece persistida.
5. Não alterar Repository, schemas, modelos, endpoints ou outras funcionalidades.
6. Atualizar docs/prompts.md com o refinamento e seus resultados.
7. Executar novamente a suíte completa, pip check e git diff --check.
8. Apresentar o resultado e o git status.

Não realizar commit ainda. Aguardar minha aprovação final.
```

O prompt foi acompanhado de uma referência ao arquivo `tests/test_task_service.py` no editor.

**Alterações e resultado obtido:**

- Em `app/services/task_service.py`, `create()` e `update()` mantêm a operação do Repository e o commit no `try/except`. O refresh e o retorno agora ocorrem depois desse bloco. Falhas do Repository e do commit continuam causando rollback e propagação da exceção; falhas do refresh são propagadas sem rollback.
- Em `tests/test_task_service.py`, adicionados dois casos parametrizados em `test_refresh_failure_propagates_without_undoing_commit`, um de criação e um de atualização. Os testes verificam a identidade da exceção original, uma chamada a commit e refresh, nenhuma chamada a rollback e os dados confirmados por uma nova sessão. A atualização também verifica a preservação do ID e a remoção da descrição persistida.
- Os patches ficam em `monkeypatch.context()`, sem interferir na limpeza das fixtures. Nenhum teste existente foi removido, e nenhuma outra camada foi alterada.
- Executado `timeout 30s .venv/bin/python -m pytest -q` fora da restrição que afetou o TestClient anteriormente: **189 testes aprovados em 2,39 s**, sendo 22 do Service, 20 do Repository, 33 da persistência, 104 dos schemas, nove dos enums e um de `/health`.
- Um aviso interno de depreciação do Starlette/AnyIO sobre `anyio.abc.BlockingPortal`, sem falhas.
- `.venv/bin/python -m pip check`: nenhuma incompatibilidade detectada. `git diff --check`: sem erros.
- `git status --short`: `docs/prompts.md` modificado, `app/services/` e `tests/test_task_service.py` novos, ainda sem commit nesta etapa.

**Validação humana:** concluída. O usuário aprovou a revisão humana final da Etapa 2.5, considerando o refinamento no tratamento de `refresh()`, os dois novos casos e a suíte completa com 189 testes aprovados. Autorizou o commit somente de `app/services/`, `tests/test_task_service.py` e `docs/prompts.md`, com a mensagem `feat: adiciona camada service de tarefas`.

**Refinamentos realizados:** refresh separado do tratamento de falhas de escrita, com cobertura explícita da persistência após commit mesmo quando a leitura posterior falha. O total da suíte passou de 187 para 189 testes aprovados.

## Etapa 2.6 — Endpoints CRUD com FastAPI

**Data:** registrado em 12/10/2026.

**Objetivo:** disponibilizar o CRUD REST de tarefas, reutilizando o Service, com inicialização explícita das tabelas e documentação automática no Swagger.

**Prompt original:**

```text
Estamos iniciando a Etapa 2.6 — Endpoints CRUD com FastAPI do projeto acadêmico micro-api-tarefas-python.

A Etapa 2.5 foi concluída no commit 75ea94f, com 189 testes aprovados.

Antes de implementar, leia integralmente:
- README.md e AGENTS.md, se existirem
- docs/prompts.md
- app/main.py
- app/database.py
- app/models.py
- app/schemas.py
- app/enums.py
- app/repositories/task_repository.py
- app/services/task_service.py
- Os testes existentes relevantes

**Objetivo:** disponibilizar as operações CRUD de tarefas pela API REST, reutilizando o Service existente, com documentação automática no Swagger.

### 1. Endpoints

Implementar:

- POST /tarefas — criar tarefa, retornar HTTP 201 e TaskResponse.
- GET /tarefas — listar tarefas, retornar HTTP 200 e list[TaskResponse].
- GET /tarefas/{task_id} — consultar tarefa, retornar HTTP 200 e TaskResponse.
- PATCH /tarefas/{task_id} — atualizar parcialmente, retornar HTTP 200 e TaskResponse.
- DELETE /tarefas/{task_id} — excluir tarefa, retornar HTTP 204 sem corpo.

### 2. Organização

Preferir um APIRouter em app/api/tasks.py, com app/api/__init__.py, registrando o router em app/main.py.

Utilizar Depends(get_db) para receber a sessão SQLAlchemy por requisição e construir TaskService(session).

Usar os schemas TaskCreate, TaskUpdate e TaskResponse já existentes.

### 3. Tratamento de erros

- Converter TaskNotFoundError em HTTP 404, com mensagem clara.
- Deixar o FastAPI/Pydantic tratar entradas inválidas com HTTP 422.
- Preservar HTTP 500 para erros internos inesperados, sem expor detalhes sensíveis.
- Não implementar autenticação ou tratamento genérico desnecessário.

### 4. Banco de dados

Garantir que a tabela tasks exista ao executar a aplicação, usando Base.metadata.create_all(bind=engine) em um ponto explícito e adequado do ciclo de inicialização do FastAPI.

Não criar tabelas durante a importação dos módulos e não introduzir Alembic nesta etapa.

Preservar a configuração existente de SQLite e o gerenciamento de sessões.

### 5. Testes

Criar tests/test_task_api.py utilizando TestClient e um banco SQLite temporário, com substituição de get_db para isolamento.

Cobrir:
- POST com dados válidos, defaults e HTTP 201.
- GET de lista vazia e com tarefas.
- GET por ID existente e inexistente.
- PATCH parcial, incluindo descricao=None.
- DELETE com HTTP 204 e corpo vazio.
- HTTP 404 para GET, PATCH e DELETE inexistentes.
- HTTP 422 para dados inválidos e campos extras.
- Persistência entre requisições de teste.
- Preservação de GET /health.
- Disponibilidade de /docs e /openapi.json.

Evitar duplicar desnecessariamente os testes já existentes das camadas inferiores.

### 6. Restrições

- Não alterar Repository, Service, schemas, enums ou modelos sem defeito comprovado.
- Não implementar filtros, endpoint específico de conclusão, integração com IA, autenticação, paginação ou frontend.
- Não adicionar dependências sem necessidade.
- Não alterar README.md ou AGENTS.md.
- Não realizar commit.
- Não avançar para a próxima etapa.

### 7. Documentação e validação

Atualizar docs/prompts.md com o prompt, decisões técnicas, arquivos alterados, testes executados e aprovação humana pendente.

Executar:
- Suíte completa com Pytest.
- pip check.
- git diff --check.
- git status.

Ao finalizar, informar:
- Arquivos criados e modificados.
- Quantidade total de testes aprovados.
- Decisões técnicas.
- Possíveis riscos e avisos.
- Instruções para executar a aplicação e acessar o Swagger.

**Não realizar commit. Aguarde minha revisão humana antes de avançar.**
```

**Arquivos criados:** `app/api/__init__.py`, `app/api/tasks.py`, `tests/conftest.py` e `tests/test_task_api.py`.

**Arquivos modificados:** `app/main.py` para registro do router, lifespan e handler de tarefa inexistente; `tests/test_health.py` para usar o cliente isolado; este documento para registrar a etapa. Repository, Service, schemas, enums, modelos, configuração do banco, dependências, README e AGENTS permaneceram intactos.

**Decisões técnicas:**

- APIRouter com prefixo `/tarefas` e tag `Tarefas`. POST retorna 201; GET e PATCH retornam 200; DELETE retorna `Response` com 204 e nenhum corpo.
- Cada endpoint síncrono recebe `Session` por `Depends(get_db)`, constrói `TaskService(session)` e delega a operação correspondente. Commit e rollback continuam exclusivos do Service.
- Entradas usam `TaskCreate` e `TaskUpdate`; saídas usam `response_model=TaskResponse` ou `list[TaskResponse]`. IDs de caminho são inteiros positivos; valores inválidos produzem 422.
- Handler específico de `TaskNotFoundError` em `app/main.py` retorna 404 e `{"detail": "Tarefa <id> não encontrada."}`. As respostas 404 são documentadas nas rotas por ID. Não há captura genérica de exceções: erros inesperados mantêm o 500 padrão sem detalhes internos, com debug desativado por padrão.
- `Base.metadata.create_all(bind=engine)` executa no lifespan antes de aceitar requisições. Os modelos são registrados pela importação das rotas e do Service, mas não há abertura de conexão ou criação de tabelas na importação.
- Fixture compartilhada `client` em `tests/conftest.py` usa arquivo SQLite próprio em `tmp_path`, substitui `get_db` por sessões desse banco e troca a engine referenciada pelo lifespan. A fixture não cria tabelas previamente: o lifespan real faz isso. Overrides são restaurados e a engine de teste é descartada ao terminar.
- O teste existente de `/health` foi adaptado para essa fixture, evitando que a nova inicialização acessasse o banco de desenvolvimento. O comportamento esperado do endpoint permaneceu igual.
- `create_all()` cria tabelas ausentes, mas não migra tabelas já existentes. Falhas posteriores ao commit (por exemplo no refresh do Service) ainda podem produzir HTTP 500 com a operação já persistida; o comportamento do Service aprovado foi preservado.

**Resultados reais e verificações executadas:**

- Criados 27 casos em `tests/test_task_api.py`; preservado o teste de `/health`, agora isolado. Cobertos códigos HTTP, JSON de resposta/defaults, persistência entre requisições, atualização parcial e descrição nula, exclusão sem corpo, 404 dos três métodos por ID, 422 de POST/PATCH e IDs inválidos, Swagger/OpenAPI, 500 sem exposição da mensagem interna, criação das tabelas no lifespan e importação de `app.main` sem conexão ou criação de tabelas.
- Executado `timeout 45s .venv/bin/python -m pytest -q` fora da restrição que afetou o TestClient anteriormente: **216 testes aprovados em 3,35 s**, incluindo os 189 casos existentes e os 27 novos casos da API.
- Um aviso de depreciação interno do Starlette/AnyIO sobre `anyio.abc.BlockingPortal`, sem falhas.
- `.venv/bin/python -m pip check`: nenhuma incompatibilidade detectada.
- `git diff --check`: sem erros.
- `git status --short`: modificados `app/main.py`, `tests/test_health.py` e `docs/prompts.md`; novos `app/api/`, `tests/conftest.py` e `tests/test_task_api.py`.
- Nenhum commit foi realizado. Nenhuma funcionalidade da próxima etapa foi implementada.

**Execução local:** na raiz, usar `.venv/bin/python -m uvicorn app.main:app --reload`. O lifespan criará a tabela `tasks` no SQLite configurado por `DATABASE_URL` (padrão `tarefas.db`). Swagger em `http://127.0.0.1:8000/docs`, OpenAPI em `http://127.0.0.1:8000/openapi.json` e saúde em `http://127.0.0.1:8000/health`.

**Validação humana:** concluída e aprovada. O usuário informou que revisou `app/api/tasks.py`, `app/main.py`, `tests/conftest.py` e `tests/test_task_api.py`. Nenhuma correção obrigatória foi identificada. A Etapa 2.6 foi aprovada para commit, condicionado à repetição bem-sucedida da suíte completa, `pip check` e `git diff --check`. Foram autorizados somente `app/api/`, `app/main.py`, `tests/conftest.py`, `tests/test_task_api.py`, `tests/test_health.py` e `docs/prompts.md`, com a mensagem `feat: adiciona endpoints CRUD de tarefas`.

**Refinamentos realizados:** o teste de saúde passou a compartilhar a fixture isolada para preservar o banco de desenvolvimento durante o lifespan. Não foram necessárias correções após a primeira execução da suíte completa.

## Etapa 2.7 — Conclusão de tarefas e filtro por status

**Data:** registrado em 12/10/2026.

**Objetivo:** implementar exclusivamente conclusão de tarefa e filtro opcional por status, mantendo o fluxo FastAPI → Service → Repository → SQLite.

**Prompt original:**

```text
Estamos iniciando a Etapa 2.7 — Conclusão de tarefas e filtro por status do projeto acadêmico micro-api-tarefas-python.

A Etapa 2.6 foi concluída no commit b0f7d6c, com 216 testes aprovados e Git limpo.

Antes de implementar, leia integralmente:
- README.md e AGENTS.md, se existirem
- docs/prompts.md
- app/main.py
- app/api/tasks.py
- app/database.py
- app/enums.py
- app/models.py
- app/schemas.py
- app/repositories/task_repository.py
- app/services/task_service.py
- Os testes existentes relevantes

OBJETIVO

Implementar exclusivamente duas funcionalidades: conclusão de tarefa e filtro opcional por status.

1. CONCLUSÃO DE TAREFA

Criar o endpoint:

PATCH /tarefas/{task_id}/concluir

Regras:
- Receber somente o ID na URL, sem corpo obrigatório.
- Alterar o status para "concluida".
- Retornar HTTP 200 com TaskResponse.
- Se a tarefa não existir, retornar HTTP 404 usando TaskNotFoundError.
- Se já estiver concluída, retornar HTTP 200 com a tarefa, sem erro.
- Preservar título, descrição e prioridade.
- Reutilizar o Repository e o Service existentes.
- Manter o controle de transações no Service.
- Não duplicar código desnecessariamente.

2. FILTRO POR STATUS

Ampliar o endpoint existente:

GET /tarefas

Adicionar um parâmetro opcional de consulta:

status=pendente ou status=concluida

Regras:
- Sem parâmetro: retornar todas as tarefas, mantendo o comportamento atual.
- Com status válido: retornar somente as tarefas com o status solicitado.
- Status inválido: retornar HTTP 422.
- Lista sem resultados: retornar HTTP 200 com [].
- Preservar a ordenação por ID crescente.
- Realizar a filtragem no Repository, usando SQLAlchemy, e não em memória na API.
- Reutilizar o enum TaskStatus existente.
- Preservar compatibilidade com list_all() e com os testes anteriores.

3. ARQUITETURA

Manter o fluxo:

FastAPI → TaskService → TaskRepository → SQLite

Implementar apenas os métodos necessários em cada camada, com alterações mínimas.

Não criar novos modelos ou schemas sem necessidade.

4. TESTES

Adicionar testes automatizados cobrindo:

- Conclusão de tarefa pendente.
- Conclusão de tarefa já concluída.
- Conclusão de tarefa inexistente (404).
- Preservação dos demais campos.
- Persistência após conclusão.
- Filtro por status pendente.
- Filtro por status concluída.
- Listagem sem filtro.
- Status inválido (422).
- Filtro sem resultados.
- Ordenação por ID.
- Rollback em falhas de escrita.
- Ausência de commit nas consultas.
- Documentação dos novos parâmetros e endpoint no OpenAPI.

Utilizar SQLite temporário nos testes, sem acessar o banco de desenvolvimento.

5. RESTRIÇÕES

- Não implementar IA nesta etapa.
- Não implementar autenticação, paginação ou frontend.
- Não adicionar dependências desnecessárias.
- Não alterar a estrutura do banco.
- Não modificar README.md ou AGENTS.md.
- Não alterar o comportamento dos cinco endpoints CRUD existentes.
- Não realizar commit.
- Não avançar para a próxima etapa.

6. DOCUMENTAÇÃO

Atualizar docs/prompts.md com:
- Prompt utilizado.
- Arquivos criados ou alterados.
- Decisões técnicas.
- Resultados dos testes.
- Aprovação humana pendente.

7. VALIDAÇÃO

Executar:
- Suíte completa com Pytest.
- pip check.
- git diff --check.
- git status.

Ao finalizar, apresentar:
- Arquivos modificados.
- Quantidade de testes aprovados.
- Decisões técnicas.
- Eventuais riscos e avisos.
- Exemplos de chamadas dos novos endpoints.

Não realizar commit. Aguarde minha revisão humana antes de avançar.
```

**Arquivos alterados:** `app/api/tasks.py`, `app/services/task_service.py`, `app/repositories/task_repository.py`, `tests/test_task_api.py`, `tests/test_task_service.py`, `tests/test_task_repository.py` e este documento. Nenhum arquivo novo foi necessário.

**Decisões técnicas:**

- `TaskService.complete(task_id)` delega a `update(task_id, TaskUpdate(status=TaskStatus.CONCLUIDA))`. Reutiliza o Repository, tratamento de tarefa inexistente, commit/rollback e refresh já existentes, sem duplicar consultas nem lógica transacional.
- A conclusão preserva os campos omitidos e aceita repetir a operação em tarefa já concluída. A repetição passa pela atualização existente e confirma a transação; não há regra adicional que impeça essa confirmação.
- `PATCH /tarefas/{task_id}/concluir` recebe apenas ID positivo, sem corpo obrigatório, e retorna `TaskResponse` com HTTP 200. Reutiliza o handler existente para `TaskNotFoundError`/404.
- `TaskRepository.list_all(status: TaskStatus | None = None)` mantém a chamada sem argumentos e a ordenação por ID crescente; com status, aplica `where(Task.status == status)` no SQLAlchemy. Não há filtragem em memória na API.
- `TaskService.list_all()` recebe o mesmo filtro opcional e o encaminha ao Repository, sem commit.
- `GET /tarefas` usa parâmetro Query opcional tipado com `TaskStatus`. FastAPI valida os valores e retorna 422 para inválidos. Sem parâmetro, a lista mantém o comportamento anterior; sem correspondências, retorna 200 com lista vazia.
- Modelos, schemas, enums, configuração do banco, main, estrutura das tabelas e dependências foram preservados. Os cinco endpoints CRUD mantêm seus contratos, com a extensão opcional da listagem solicitada.

**Testes e resultados reais:**

- Adicionados 20 casos: dois no Repository, sete no Service e onze na API. Reutilizadas as fixtures SQLite temporárias existentes, sem acesso ao banco de desenvolvimento.
- No Repository, verificada a filtragem para ambos os status com IDs inseridos fora de ordem; a saída mantém ID crescente.
- No Service, adicionadas conclusão pendente/já concluída com campos preservados e recuperação por nova sessão; leitura filtrada delegada sem commit para ambos os status. Estendidos os testes existentes de tarefa inexistente e de falhas após flush/no commit para conclusão, verificando rollback e preservação do status pendente no banco.
- Na API, cobertas conclusão sem corpo, repetição em tarefa já concluída, persistência, preservação dos demais campos, 404, ambos os filtros com ordenação e listagem sem filtro, três entradas inválidas com 422 e dois casos de filtro sem correspondências. O OpenAPI documenta a nova rota sem requestBody e o filtro opcional com os valores do enum.
- Ajustada somente a assinatura do stub do teste de erro interno da listagem para aceitar o novo argumento opcional; a verificação de HTTP 500 sem detalhes sensíveis foi preservada.
- Executado `timeout 45s .venv/bin/python -m pytest -q` fora da restrição que afetou o TestClient anteriormente: **236 testes aprovados em 4,78 s**, incluindo todos os 216 casos anteriores.
- Um aviso de depreciação interno do Starlette/AnyIO sobre `anyio.abc.BlockingPortal`, sem falhas.
- `.venv/bin/python -m pip check`: nenhuma incompatibilidade detectada. `git diff --check`: sem erros.
- `git status --short`: apenas os sete arquivos desta etapa modificados. Nenhum commit foi realizado.

**Exemplos de chamadas:**

```bash
curl -X PATCH http://127.0.0.1:8000/tarefas/1/concluir
curl 'http://127.0.0.1:8000/tarefas?status=pendente'
curl 'http://127.0.0.1:8000/tarefas?status=concluida'
curl http://127.0.0.1:8000/tarefas
```

Os exemplos por ID pressupõem que a tarefa exista. O Swagger permanece em `http://127.0.0.1:8000/docs`.

**Validação humana:** concluída e aprovada. O usuário confirmou a aprovação humana final da Etapa 2.7, incluindo conclusão de tarefas, filtro por status e testes. Autorizou o commit somente de `app/api/tasks.py`, `app/services/task_service.py`, `app/repositories/task_repository.py`, `tests/test_task_api.py`, `tests/test_task_service.py`, `tests/test_task_repository.py` e `docs/prompts.md`, condicionado à repetição bem-sucedida da suíte completa, `pip check` e `git diff --check`, com a mensagem `feat: adiciona conclusao e filtro de tarefas`. A Etapa 2.8 não foi autorizada nesta solicitação.

**Refinamentos realizados:** reutilizados os testes transacionais existentes para cobrir conclusão, sem repetir sua infraestrutura. A primeira execução da suíte completa passou; não foram necessárias correções adicionais.

## Etapa 2.8.1 — Sugestão local e determinística de prioridade

**Data:** registrado em 12/10/2026.

**Objetivo:** preparar a sugestão local de prioridade por palavras-chave, independente de banco, HTTP ou provedor de IA.

**Prompt original:**

```text
Estamos iniciando a Etapa 2.8.1 do projeto acadêmico `micro-api-tarefas-python`.

A Etapa 2.7 foi concluída e registrada no commit `479bd1d`, com 236 testes aprovados.

Antes de implementar, leia integralmente `README.md`, `AGENTS.md`, `docs/prompts.md` e os arquivos relevantes da aplicação.

**Objetivo:** implementar exclusivamente uma sugestão local e determinística de prioridade para tarefas, preparando a futura integração com IA.

Requisitos:

1. Criar `app/services/priority_service.py` com uma função ou classe simples que receba título e descrição e retorne um valor de `TaskPriority`: `baixa`, `media` ou `alta`.
2. Definir regras explícitas, simples e documentadas, baseadas em palavras-chave. A prioridade padrão sugerida será `media` quando não houver correspondência.
3. Normalizar os textos para comparação sem diferenciar maiúsculas e minúsculas.
4. Quando houver palavras-chave de prioridades diferentes, aplicar precedência `alta > media > baixa`.
5. Criar `tests/test_priority_service.py`, cobrindo as três prioridades, ausência de correspondência, textos vazios, descrição opcional e conflitos entre palavras-chave.
6. Atualizar `docs/prompts.md` com este prompt, decisões técnicas, arquivos alterados, resultados dos testes e validação humana pendente.

Restrições:

- Não integrar API externa ou provedor de IA nesta etapa.
- Não adicionar dependências.
- Não modificar o banco de dados, modelos, schemas, Repository, Service existente ou endpoints CRUD.
- Não criar endpoint de sugestão ainda.
- Não alterar `README.md` ou `AGENTS.md`.
- Não realizar commit.
- Não avançar para a Etapa 2.8.2.

Execute a suíte completa de testes, `pip check`, `git diff --check` e `git status`.

Ao finalizar, apresente os arquivos alterados, as regras de classificação, a quantidade de testes aprovados e eventuais riscos.

Aguarde minha revisão humana antes de realizar qualquer commit.
```

O prompt foi acompanhado de uma referência ao arquivo `docs/prompts.md` no editor.

**Arquivos criados:** `app/services/priority_service.py` e `tests/test_priority_service.py`. Apenas este documento foi modificado entre os arquivos existentes.

**Decisões técnicas e regras de classificação:**

- Função pura `suggest_priority(titulo: str, descricao: str | None = None) -> TaskPriority`, sem sessão, persistência, rede ou alteração de tarefas.
- Título e descrição são combinados e normalizados com `casefold()`. A descrição omitida ou `None` equivale a texto vazio. A função também aceita título vazio, conforme o requisito de testes, sem modificar a validação do título nos schemas existentes.
- A biblioteca padrão `re` extrai palavras inteiras com `\b\w+\b`; pontuação comum e espaços delimitam as palavras. Não são feitas correspondências por trecho dentro de outras palavras.
- Alta: `urgente`, `emergência`, `emergencia`, `crítico`, `critico`.
- Média: `importante`, `prazo`, `revisar`.
- Baixa: `opcional`, `rotina`, `depois`.
- As regras ficam em `PRIORITY_KEYWORDS`, uma sequência com conjuntos imutáveis, em ordem alta → média → baixa. A primeira categoria com correspondência vence, independentemente da posição da palavra no texto ou do campo de origem.
- Sem correspondência, incluindo textos vazios ou somente espaços, a função retorna `TaskPriority.MEDIA`.
- A normalização preserva acentos: as variantes sem acento de emergência e crítico foram cadastradas explicitamente. Não há reconhecimento automático de plurais, flexões ou sinônimos fora da lista.
- Limitação para revisão: palavras-chave não interpretam negação ou contexto. Por exemplo, `não é urgente` ainda sugere alta. Trata-se de sugestão heurística acadêmica; nenhuma prioridade é aplicada ou salva automaticamente nesta etapa.

**Resultados reais e verificações:**

- Criados 33 casos: onze exemplos para todas as palavras-chave, três casos de correspondência pela descrição, quatro de maiúsculas/pontuação no título, cinco de ausência de correspondência/textos vazios/descrição opcional, seis conflitos de prioridade, três casos sem correspondência em palavras maiores ou plurais e um de determinismo com retorno de enum.
- Executado `timeout 45s .venv/bin/python -m pytest -q`, fora da restrição que afetou o TestClient anteriormente: **269 testes aprovados em 25,89 s**, incluindo os 236 casos existentes e os 33 novos casos de sugestão local.
- Um aviso de depreciação interno do Starlette/AnyIO sobre `anyio.abc.BlockingPortal`, sem falhas.
- `.venv/bin/python -m pip check`: nenhuma incompatibilidade detectada.
- `git diff --check`: sem erros.
- `git status --short`: `docs/prompts.md` modificado; `app/services/priority_service.py` e `tests/test_priority_service.py` novos.
- Nenhuma dependência foi adicionada, nenhuma camada existente foi modificada e nenhum endpoint ou integração externa foi criado. Nenhum commit foi realizado. A Etapa 2.8.2 não foi iniciada.

**Validação humana:** concluída e aprovada. O usuário confirmou a revisão humana final de `app/services/priority_service.py`, `tests/test_priority_service.py` e `docs/prompts.md`, sem correções obrigatórias. A Etapa 2.8.1 foi aprovada para um único commit, condicionado à repetição bem-sucedida da suíte completa, `pip check` e `git diff --check`, com a mensagem `feat: adiciona sugestao local de prioridade`. Somente esses três arquivos foram autorizados; a Etapa 2.8.2 não deve ser iniciada nesta solicitação.

**Refinamentos realizados:** não foram necessárias correções após a primeira execução da suíte completa.

## Etapa 2.8.2.1 — Cliente OpenAI e serviço de fallback

**Data:** registrado em 12/10/2026.

**Objetivo:** implementar exclusivamente o adaptador OpenAI e a coordenação de sugestão por IA com fallback local, sem criar endpoint ou consumir créditos em testes.

**Prompt original:**

```text
Aprovo o planejamento da Etapa 2.8.2 com os ajustes discutidos.

Inicie somente a Etapa 2.8.2.1 — Cliente OpenAI e serviço de fallback.

Antes de implementar, consulte a documentação oficial atual da OpenAI para confirmar:
- SDK Python compatível com Python 3.10.12.
- Modelo econômico adequado à classificação de textos curtos.
- Uso da Responses API e saída estruturada.
- Timeout e desativação de retries automáticos.

Implemente exclusivamente:

1. Cliente de integração OpenAI isolado.
2. Serviço que tenta obter a prioridade pela IA e utiliza `suggest_priority()` quando ocorrer uma falha prevista.
3. Configuração por variáveis de ambiente, sem armazenar credenciais.
4. Validação obrigatória da prioridade retornada usando `TaskPriority`.
5. Testes unitários com mocks, sem chamadas externas.
6. Registro completo da etapa em `docs/prompts.md`, mantendo validação humana pendente.

Restrições:
- Não criar endpoints nesta entrega.
- Não modificar o CRUD, banco, Repository ou schemas existentes.
- Não alterar a função local `suggest_priority()`.
- Não realizar chamadas reais à OpenAI.
- Não realizar commit.
- Não iniciar a Etapa 2.8.2.2.

Execute a suíte completa de testes, `pip check`, `git diff --check` e `git status`.

Apresente os arquivos alterados, o modelo e a versão do SDK escolhidos, os resultados dos testes e os riscos identificados.

Aguarde minha revisão humana.
```

**Documentação oficial consultada:**

- [SDK Python da OpenAI](https://developers.openai.com/api/reference/python): Python 3.10+, Responses API, timeout configurável e `max_retries=0` para desativar retries automáticos.
- [GPT-5 nano](https://developers.openai.com/api/docs/models/gpt-5-nano): modelo econômico da família GPT-5 indicado para classificação, com suporte à Responses API e Structured Outputs. Foi escolhido por atender à tarefa acadêmica; não foi tratado como o modelo mais recente ou superior a todas as alternativas.
- [Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses): uso de `responses.parse()` com modelo Pydantic em `text_format` e resultado em `output_parsed`, incluindo o tratamento de recusas e respostas incompletas.
- Confirmados localmente os metadados do SDK instalado: `openai==3.29.0`, `Requires-Python: >=3.10`, com execução em Python 3.10.12; inspecionada também a assinatura de `Responses.parse`.

**Arquivos criados:** `app/integrations/__init__.py`, `app/integrations/openai_priority_client.py`, `app/services/priority_suggestion_service.py`, `tests/test_openai_priority_client.py` e `tests/test_priority_suggestion_service.py`.

**Arquivos modificados:** `requirements.txt` para declarar `openai==3.29.0` e este documento. Não foram alterados endpoints, banco, modelos, enums, schemas existentes, Repository, TaskService, função local, README ou AGENTS.

**Decisões técnicas:**

- `OpenAIPriorityClient` usa o SDK síncrono, separado das camadas de HTTP e persistência. A importação e a configuração não fazem chamadas externas. O cliente SDK é criado somente em `suggest()` e fechado por gerenciador de contexto ao terminar, inclusive em caso de erro.
- Configuração por `OPENAI_API_KEY`, `OPENAI_MODEL` (padrão `gpt-5-nano`) e `OPENAI_TIMEOUT_SECONDS` (padrão 10 segundos). A chave é lida do ambiente e mantida apenas em memória, sem arquivo ou log. Chave ausente/vazia ou modelo explicitamente vazio desabilitam a IA e permitem fallback imediato.
- Timeout deve ser numérico, positivo e finito; configuração inválida gera `ValueError` e não é mascarada como falha do provedor. Não foi adicionada dependência de dotenv.
- O cliente utiliza a URL padrão do SDK, `https://api.openai.com/v1` para autenticação por chave quando `OPENAI_BASE_URL` não está definida, com `max_retries=0` e timeout configurado. O parâmetro explícito de URL foi removido na verificação complementar abaixo. O timeout é do transporte, não uma garantia absoluta de duração total.
- A chamada usa `responses.parse()`, saída Pydantic interna `_PriorityOutput` com campo `prioridade: TaskPriority` e `extra="forbid"`. Não altera os schemas existentes. A prioridade é novamente convertida para `TaskPriority` antes de retornar.
- Título/descrição seguem como JSON de dados, separados das instruções fixas. O prompt instrui o modelo a classificar alta para urgência/impacto crítico, média para importância/prazo comum e baixa para atividade opcional/adiável, com padrão média. Não são oferecidas ferramentas ou alterações de tarefas.
- Configurados `max_output_tokens=1024` e `store=False`. Resposta não concluída, recusada ou sem saída parseada gera `PriorityIntegrationError`; limite de tokens pode incluir raciocínio, e resposta incompleta aciona fallback.
- Erros de conexão/timeout, status HTTP do provedor, validação de resposta do SDK e prioridade/JSON inválidos são traduzidos para `PriorityIntegrationError`, com mensagens locais genéricas. Exceções inesperadas, como `RuntimeError`, continuam propagadas.
- `PrioritySuggestionService.suggest()` captura somente `PriorityIntegrationError`. Em falha prevista ou cliente ausente, reutiliza `suggest_priority(titulo, descricao)` com os textos originais, sem modificar a função local.
- Resultado interno `PrioritySuggestion` é um dataclass imutável com `prioridade: TaskPriority` e `origem` igual a `ia` ou `local`; não é schema HTTP. `PrioritySuggestionService.from_env()` permite construir o serviço configurado sem depender de banco ou endpoint.
- Riscos para revisão: qualidade e latência do modelo ainda não foram avaliadas com chamadas reais; disponibilidade depende da conta. Textos enviados ao provedor podem conter dados sensíveis. `store=False` não deve ser interpretado como garantia de ausência total de retenção pelo provedor. Resposta incompleta/timeout e erros de configuração de credencial no provedor podem levar ao fallback. A heurística local preserva suas limitações de contexto e negação.

**Testes e verificações executados:**

- Instalado o SDK na `.venv` com `.venv/bin/python -m pip install --no-cache-dir openai`; a versão resolvida 3.29.0 foi fixada em `requirements.txt`. Foram instaladas suas dependências transitivas, sem alterar as versões diretas já declaradas do projeto.
- Executado `.venv/bin/python -m pytest -q tests/test_openai_priority_client.py tests/test_priority_suggestion_service.py` antes dos três casos de transporte simulado: **52 testes aprovados em 2,23 s**, com um aviso interno do Starlette/AnyIO decorrente da importação do cliente de testes existente.
- Acrescentados três casos com SDK/parser real e `httpx2.MockTransport`, retornando resposta estruturada válida, prioridade inválida e texto malformado. Confirmam o JSON Schema estrito enviado pelo SDK e a validação real, sem conexão externa.
- Total de 55 novos casos: 42 do cliente e 13 do serviço. Cobrem os três enums, payload/configuração, timeout/retries, erros HTTP e de transporte, recusas/incompletude, resposta inválida, configuração ausente, fallback, preservação de textos e propagação de defeitos inesperados. Os testes de configuração removem variáveis reais e usam exclusivamente credenciais fictícias.
- Executado `timeout 45s .venv/bin/python -m pytest -q`, fora da restrição que afetou o TestClient anteriormente: **324 testes aprovados em 5,95 s**, incluindo os 269 casos anteriores.
- Um aviso de depreciação interno do Starlette/AnyIO sobre `anyio.abc.BlockingPortal`, sem falhas.
- `.venv/bin/python -m pip check`: nenhuma incompatibilidade detectada. `git diff --check`: sem erros.
- `git status --short`: `requirements.txt` e `docs/prompts.md` modificados; novos `app/integrations/`, `app/services/priority_suggestion_service.py`, `tests/test_openai_priority_client.py` e `tests/test_priority_suggestion_service.py`.
- Nenhuma chamada real à OpenAI foi realizada; consulta da documentação e instalação do pacote não utilizaram a API de inferência. Nenhum commit foi realizado. A Etapa 2.8.2.2 não foi iniciada.

**Validação humana:** concluída e aprovada. O usuário confirmou a aprovação humana final da Etapa 2.8.2.1 — Cliente OpenAI e serviço de fallback, incluindo a verificação complementar, e autorizou o commit exclusivamente dos arquivos desta entrega com a mensagem `feat: adiciona integracao openai com fallback local`. A suíte completa anteriormente executada apresentou 324 testes aprovados, sem chamadas reais à OpenAI. A Etapa 2.8.2.2 depende de autorização posterior.

**Refinamentos realizados:** após os testes unitários iniciais, acrescentados três casos de transporte HTTP simulado para verificar também o parser real do SDK e o formato estruturado da requisição, sem ampliar o escopo funcional.

### Verificação complementar — Transporte HTTP, URL padrão e dependências

- Conferidos os metadados e o código original do SDK instalado `openai==3.29.0`: a dependência declarada é `httpx2<3,>=2.12.0`, e os módulos `openai._client` e `openai._base_client` importam `httpx2`. Portanto, o uso de `httpx2` nos testes e neste registro está correto e foi preservado. O `httpx==0.28.1` existente nas dependências de desenvolvimento atende ao TestClient, uma finalidade diferente.
- Confirmada no código do SDK a URL padrão `https://api.openai.com/v1` para autenticação por chave. Removido somente o argumento explícito `base_url` de `OpenAIPriorityClient.suggest()` e sua expectativa no teste do construtor.
- A fixture dos testes do cliente também remove temporariamente `OPENAI_BASE_URL`, impedindo interferência da configuração externa. O teste existente com MockTransport passou a verificar que a URL gerada pelo SDK é `https://api.openai.com/v1/responses`. Não houve requisição real.
- Conferido o conteúdo completo de `requirements.txt`: `fastapi==0.115.12`, `uvicorn==0.34.2`, `pydantic==2.14.1`, `SQLAlchemy==2.0.44` e `openai==3.29.0`. Nenhuma versão ou dependência foi alterada nesta verificação.
- Executado novamente `timeout 45s .venv/bin/python -m pytest -q`: **324 testes aprovados em 5,89 s**, com um aviso de depreciação interno do Starlette/AnyIO e sem falhas.
- `.venv/bin/python -m pip check`: nenhuma incompatibilidade detectada. `git diff --check`: sem erros.
- `git status --short`: `docs/prompts.md` e `requirements.txt` modificados; `app/integrations/`, `app/services/priority_suggestion_service.py`, `tests/test_openai_priority_client.py` e `tests/test_priority_suggestion_service.py` novos, todos pertencentes à entrega ainda sem commit. Nesta verificação, somente o cliente, seu teste e este documento receberam ajustes.
- Após esta verificação complementar, o usuário aprovou a revisão humana final e autorizou o commit da Etapa 2.8.2.1. Nenhum endpoint ou chamada real à OpenAI foi realizado; a Etapa 2.8.2.2 não foi iniciada.

## Etapa 2.8.2.2 — Endpoint HTTP de sugestão de prioridade

**Data:** registrado em 12/10/2026.

**Objetivo:** disponibilizar sugestão de prioridade por HTTP, reutilizando a integração e o fallback existentes, sem persistência ou alteração do CRUD.

**Prompt original:**

```text
Vamos iniciar a Etapa 2.8.2.2 — Endpoint HTTP de sugestão de prioridade do projeto micro-api-tarefas-python.

A Etapa 2.8.2.1 foi concluída e registrada no commit e029044, com 324 testes aprovados.

Antes de implementar, leia README.md, AGENTS.md, docs/prompts.md e os arquivos existentes da API, schemas, cliente OpenAI e serviço de sugestão.

Implemente exclusivamente:

1. Criar os schemas Pydantic de entrada e saída para a sugestão de prioridade.
2. Criar POST /tarefas/sugerir-prioridade, retornando HTTP 200.
3. Reutilizar PrioritySuggestionService.from_env() e o serviço de fallback já implementado.
4. Validar título obrigatório com 3 a 150 caracteres após trim e descrição opcional com até 2.000 caracteres, reutilizando as validações existentes.
5. Rejeitar campos extras e entradas inválidas com HTTP 422.
6. Retornar prioridade como TaskPriority e origem como "ia" ou "local".
7. Registrar o endpoint no FastAPI e disponibilizá-lo no Swagger.
8. Garantir que a rota estática /tarefas/sugerir-prioridade não seja interceptada pela rota dinâmica /tarefas/{task_id}.
9. Criar testes de API com mocks, sem chamadas reais à OpenAI, cobrindo sucesso, fallback, validações, documentação e preservação do CRUD.
10. Atualizar docs/prompts.md com o prompt, decisões, testes, resultados e validação humana pendente.

Restrições:
- Não alterar o cliente OpenAI nem a função local suggest_priority().
- Não modificar banco de dados, Repository ou TaskService.
- Não adicionar dependências desnecessárias.
- Não realizar chamadas reais à OpenAI.
- Não realizar commit.
- Não iniciar a próxima etapa.

Execute a suíte completa de testes, pip check, git diff --check e git status.

Apresente os arquivos criados ou alterados, os resultados dos testes e os riscos identificados.

Aguarde minha revisão humana antes de continuar.
```

**Arquivos criados:** `app/priority_schemas.py`, `app/api/priorities.py` e `tests/test_priority_api.py`.

**Arquivos alterados:** `app/main.py` para registrar o router estático antes do router de tarefas, e este documento. Nenhuma dependência ou camada existente de integração, validação de tarefas, negócio ou persistência foi alterada.

**Decisões técnicas:**

- `PrioritySuggestionRequest` reutiliza `TaskTitle` e `TaskDescription` existentes: título obrigatório com 3 a 150 caracteres após trim; descrição opcional, até 2.000 após trim, com texto vazio normalizado para `None`. `extra="forbid"` rejeita campos como ID, status e prioridade na entrada.
- `PrioritySuggestionResponse` usa `prioridade: TaskPriority`, `origem: Literal["ia", "local"]`, `extra="forbid"` e `from_attributes=True`, permitindo validar os atributos do resultado interno do Service sem mudar esse resultado ou os schemas anteriores.
- `POST /tarefas/sugerir-prioridade` é uma rota síncrona com HTTP 200 e response_model específico. Recebe apenas título e descrição validados, chama `PrioritySuggestionService.from_env()` e delega a sugestão. Não usa Depends(get_db), Repository ou TaskService; não salva nem altera tarefas.
- `app/main.py` registra o novo router antes das rotas dinâmicas por ID, com ordem explicitamente verificada no teste. A rota é documentada automaticamente no OpenAPI e Swagger, com tag `Sugestão de prioridade`.
- Entradas inválidas retornam 422 antes de construir o serviço. Falhas previstas do cliente continuam sendo tratadas pelo fallback existente e retornam 200 com origem local. Falhas inesperadas ou configurações inválidas mantêm o 500 padrão, sem detalhes internos.
- Riscos preservados para revisão: com chave configurada, o uso real do endpoint enviará título/descrição ao provedor e poderá gerar consumo; os testes não fizeram isso. Qualidade/latência reais do modelo não foram avaliadas. Sem configuração ou em falha prevista, o fallback mantém as limitações da heurística por palavras-chave. Configuração inválida de timeout não é mascarada como fallback.

**Testes e resultados reais:**

- Criados 31 casos de API, reutilizando o TestClient e SQLite temporário já existentes.
- Cobertos os três valores de prioridade com IA simulada, normalização dos textos enviados ao serviço, três resultados de fallback após falha prevista e fallback real sem configuração da chave.
- Cobertas descrição nula/vazia/somente espaços, limites válidos após trim, corpo obrigatório, doze entradas inválidas/extras com 422 e ausência de chamada ao serviço para entrada inválida.
- Verificados ordem da rota estática, OpenAPI (schemas, enums, campos extras, limites e respostas) e disponibilidade de Swagger. Um teste impede uso da dependência de sessão de banco pelo endpoint de sugestão.
- Um fluxo CRUD verifica que a sugestão não cria ou altera tarefas, nem substitui a prioridade de tarefa existente. Os testes anteriores de CRUD, conclusão e filtro continuam na suíte.
- Verificado HTTP 500 genérico para erro inesperado e rejeição de respostas inválidas de prioridade/origem pelo response_model.
- Chamadas de IA foram simuladas por mocks; um bloqueio adicional de `OpenAIPriorityClient.suggest` impede chamada real acidental nos testes deste arquivo. Variáveis de configuração reais são removidas temporariamente e restauradas pelo monkeypatch.
- Executado `timeout 45s .venv/bin/python -m pytest -q`, fora da restrição que afetou o TestClient anteriormente: **355 testes aprovados em 6,58 s**, incluindo os 324 casos anteriores.
- Um aviso de depreciação interno do Starlette/AnyIO sobre `anyio.abc.BlockingPortal`, sem falhas.
- `.venv/bin/python -m pip check`: nenhuma incompatibilidade detectada. `git diff --check`: sem erros.
- `git status --short`: `app/main.py` e `docs/prompts.md` modificados; novos `app/api/priorities.py`, `app/priority_schemas.py` e `tests/test_priority_api.py`.
- Nenhuma chamada real à OpenAI, dependência nova ou commit foi realizado. A próxima etapa não foi iniciada.

**Exemplo do contrato:**

```text
POST /tarefas/sugerir-prioridade
Entrada: {"titulo": "Corrigir falha urgente", "descricao": null}
Resposta local esperada sem chave: {"prioridade": "alta", "origem": "local"}
```

**Validação humana:** concluída e aprovada. O usuário confirmou a revisão humana final de `app/priority_schemas.py`, `app/api/priorities.py`, `tests/test_priority_api.py`, `app/main.py` e `docs/prompts.md`, sem necessidade de correções. A Etapa 2.8.2.2 — Endpoint HTTP de sugestão de prioridade foi aprovada para commit exclusivamente desses cinco arquivos, com a mensagem `feat: adiciona endpoint de sugestao de prioridade`. A suíte completa anteriormente executada apresentou 355 testes aprovados, sem chamadas reais à OpenAI. Nenhuma nova etapa de implementação foi autorizada nesta solicitação.

**Refinamentos realizados:** nenhuma correção foi necessária após a primeira execução da suíte completa. As validações e o serviço existentes foram reutilizados sem mudanças.~~

## Etapa 3.1 — README Final da Unidade V

**Data:** registrado em 12/10/2026.

**Objetivo:** atualizar exclusivamente o README para a entrega acadêmica da Unidade V, documentando funcionalidades implementadas, instalação, execução, testes, IA, limitações e demonstração.

**Prompt original:**

```text
Vamos iniciar a Etapa 3.1 — README Final da Unidade V.

Objetivo: atualizar exclusivamente o arquivo README.md do projeto micro-api-tarefas-python, transformando a documentação inicial em um README acadêmico completo.

Antes de editar, examine o código atual e os arquivos de dependências para documentar somente funcionalidades realmente implementadas.

O README deve conter:

1. Apresentação e objetivo do projeto.
2. Problema resolvido pela API.
3. Tecnologias e versões utilizadas.
4. Arquitetura em camadas e responsabilidades.
5. Pré-requisitos e instalação com Python 3.10.
6. Criação e ativação de ambiente virtual no Linux.
7. Instalação das dependências.
8. Execução com Uvicorn.
9. Acesso ao Swagger, OpenAPI e /health.
10. Endpoints CRUD, conclusão, filtro por status e sugestão de prioridade.
11. Exemplos reais de requisições e respostas JSON.
12. Configuração opcional da OpenAI por variáveis de ambiente, explicando que o projeto não carrega .env automaticamente.
13. Explicação do fallback local e suas limitações.
14. Como executar os testes automatizados.
15. Como ChatGPT e Codex auxiliaram no desenvolvimento, destacando revisão humana, testes e registro em docs/prompts.md.
16. Limitações conhecidas e possíveis melhorias futuras.
17. Orientações básicas de demonstração.

Restrições:
- Altere somente README.md.
- Não modifique código, testes, dependências ou docs/prompts.md.
- Não instale pacotes.
- Não faça chamadas reais à OpenAI.
- Não crie commits ou tags.
- Não publique nada no GitHub.
- Preserve a alteração local preexistente em docs/prompts.md.
- Não invente funcionalidades, resultados de testes ou métricas de produtividade.
- Utilize linguagem clara, profissional e adequada à entrega acadêmica.

Ao finalizar, apresente um resumo das alterações, o diff do README.md e o git status.

Aguarde minha revisão humana antes de qualquer commit.
```

O prompt foi acompanhado de uma referência ao arquivo `docs/prompts.md` no editor.

**Resultado obtido:**

- Examinados o código atual, os contratos HTTP, os serviços, a persistência e os arquivos de dependências antes da edição.
- Atualizado somente `README.md` na implementação desta etapa, com os 17 itens solicitados. A documentação inicial foi substituída por apresentação acadêmica, tecnologias/versões, arquitetura, instalação Linux, execução, contratos e exemplos HTTP/JSON, configuração opcional da OpenAI, fallback, testes, assistência de ChatGPT/Codex, limitações e roteiro de demonstração.
- Documentado que o projeto não carrega `.env` automaticamente, que sugestão não persiste tarefas e que chamadas reais podem gerar consumo. Exemplos são apresentados como contratos do código, não como nova execução da API.
- O diff informado do README apresentou 325 linhas adicionadas e 32 removidas; o diff completo foi mostrado ao usuário.
- Verificados links locais, equilíbrio dos blocos Markdown e validação dos payloads de criação, atualização e sugestão por meio dos schemas existentes, sem chamadas à API ou geração de bytecode.
- `git diff --check` passou. A suíte Pytest não foi reexecutada na edição do README; os 355 testes aprovados são identificados no documento como resultado histórico registrado da Etapa 2.8.2.2, sem alegação de nova execução ou métrica de produtividade.
- A alteração local preexistente em `docs/prompts.md` foi preservada durante a edição do README: seu SHA256 permaneceu `0403c6096e1dbfd3ce3f2e18eb31ed9d0d19036edf59b4db76e31402a41f2742` antes e depois.
- Após aprovação humana, este registro foi acrescentado ao final de `docs/prompts.md`, por autorização expressa, preservando integralmente os bytes anteriores e a alteração preexistente.

**Validação humana:** concluída e aprovada. O usuário informou que revisou o conteúdo completo de `README.md`, considerou-o adequado e não identificou correções obrigatórias. Autorizou o registro desta etapa e o commit exclusivamente de `README.md` e `docs/prompts.md`, com a mensagem `docs: finaliza README academico da Unidade V`. A próxima etapa depende de confirmação posterior.

**Refinamentos realizados:** nenhuma correção obrigatória foi solicitada na revisão humana. Não foram alterados código, testes, dependências ou funcionalidades, instalados pacotes, criadas tags, feitas chamadas à OpenAI ou publicações no GitHub.

## Etapa 3.2.1 — Criação do .env.example

**Data:** registrado em 12/10/2026.

**Objetivo:** documentar as variáveis de ambiente utilizadas pela aplicação em um arquivo de exemplo seguro, preservando os valores padrão e o mecanismo atual de configuração.

**Prompt original:**

```text
Vamos iniciar a Etapa 3.2.1 — Configuração de ambiente da Unidade V.

Objetivo: criar o arquivo .env.example no projeto micro-api-tarefas-python, documentando as variáveis de ambiente realmente utilizadas pela aplicação.

Instruções:

1. Confira no código quais variáveis de ambiente são utilizadas.
2. Crie exclusivamente o arquivo .env.example, sem credenciais reais.
3. Documente DATABASE_URL, OPENAI_API_KEY, OPENAI_MODEL e OPENAI_TIMEOUT_SECONDS, desde que confirmadas no código.
4. Utilize exemplos seguros e comentários explicativos.
5. Preserve os valores padrão efetivamente implementados.
6. Explique nos comentários que a aplicação não carrega automaticamente arquivos .env.
7. Não instale python-dotenv nem altere o mecanismo atual de configuração.
8. Não modifique código Python, testes, README.md, .gitignore ou docs/prompts.md nesta etapa.
9. Não execute chamadas reais à OpenAI.
10. Não crie commits, tags ou publique nada.

Ao finalizar:
- Mostre o conteúdo completo de .env.example.
- Confirme que não contém credenciais reais.
- Execute git status.
- Aguarde minha revisão humana antes de qualquer commit.
```

O prompt foi acompanhado de uma referência ao arquivo `README.md` no editor.

**Resultado obtido:**

- Conferidas as leituras de variáveis em `app/database.py` e `app/integrations/openai_priority_client.py`.
- Criado somente `.env.example`, documentando `DATABASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL` e `OPENAI_TIMEOUT_SECONDS`.
- O exemplo de DATABASE_URL ficou comentado para preservar o caminho absoluto de `tarefas.db` calculado pela aplicação. A alternativa relativa está identificada como opcional e dependente do diretório de execução.
- Mantidos `OPENAI_API_KEY` vazio, modelo `gpt-5-nano` e timeout `10`; comentários explicam o fallback local, a validação do timeout e que a aplicação não carrega `.env` automaticamente.
- O conteúdo completo foi apresentado ao usuário. Confirmada ausência de credenciais reais; o Git inicialmente mostrou apenas `?? .env.example`.
- Após aprovação humana, este registro foi acrescentado ao final de `docs/prompts.md`, sem modificar seu conteúdo anterior.
- Nesta preparação do commit, verificados o conteúdo seguro de `.env.example` e `git diff --check`. Não foram alterados código Python, testes, README, .gitignore ou dependências, nem executadas chamadas reais à OpenAI ou publicações no GitHub.

**Validação humana:** concluída e aprovada. O usuário informou que revisou o conteúdo de `.env.example` e o considerou adequado aos requisitos da Unidade V. Autorizou o registro desta etapa e o commit exclusivamente de `.env.example` e `docs/prompts.md`, com a mensagem `docs: adiciona exemplo de configuracao de ambiente`. A próxima etapa depende de confirmação posterior.

**Refinamentos realizados:** nenhuma correção foi solicitada; os padrões e o mecanismo de configuração da aplicação foram preservados.
