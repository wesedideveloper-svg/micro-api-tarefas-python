# Registro dos principais prompts de desenvolvimento

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
