# Micro-API de Gerenciamento de Tarefas

API RESTful desenvolvida em Python com FastAPI para gerenciamento de tarefas, utilizando SQLite para persistência de dados e integração com Inteligência Artificial Generativa para sugestão de prioridades. Projeto desenvolvido no contexto da pós-graduação em Engenharia de Software com Inteligência Artificial Generativa.

## Apresentação e objetivo

O projeto centraliza o cadastro e o acompanhamento de tarefas, permitindo consultar pendências, atualizar informações, concluir atividades e solicitar uma sugestão de prioridade. Seu objetivo acadêmico é aplicar arquitetura em camadas, validação de dados, persistência, testes automatizados e uso supervisionado de IA durante o desenvolvimento.

O problema tratado é a organização de atividades por status e prioridade por meio de um contrato HTTP reutilizável. A aplicação oferece uma API e documentação interativa, sem interface própria de gerenciamento.

As funcionalidades implementadas são CRUD de tarefas, conclusão, filtro por status e sugestão de prioridade pela OpenAI com fallback local. A versão declarada pela aplicação é `0.1.0`.

## Tecnologias e versões

| Tecnologia | Versão utilizada | Finalidade |
|---|---|---|
| Python | 3.10; ambiente de desenvolvimento 3.10.12 | Linguagem e biblioteca padrão |
| FastAPI | 0.115.12 | Rotas, validação HTTP e OpenAPI/Swagger |
| Uvicorn | 0.34.2 | Servidor ASGI |
| Pydantic | 2.14.1 | Contratos e validações de entrada e saída |
| SQLAlchemy | 2.0.44 | Mapeamento e operações de persistência |
| SQLite | Fornecido pelo Python; versão depende do ambiente | Banco local em arquivo |
| OpenAI SDK | 3.29.0 | Responses API e saída estruturada |
| Pytest | 8.3.5 | Testes automatizados |
| HTTPX | 0.28.1 | Suporte ao TestClient |

As dependências diretas estão fixadas em [requirements.txt](requirements.txt) e [requirements-dev.txt](requirements-dev.txt). O SDK OpenAI também utiliza a dependência transitiva `httpx2`; ela é distinta do HTTPX usado nos testes HTTP da aplicação.

Git é utilizado para versionamento. IntelliJ IDEA, Codex e ChatGPT apoiaram o desenvolvimento e a revisão. Este README não pressupõe que o projeto já tenha sido publicado no GitHub.

## Arquitetura e organização

```text
Operações de tarefas: API → TaskService → TaskRepository → SQLite
Sugestão de prioridade: API → PrioritySuggestionService → Cliente OpenAI
                                                     ↘ Fallback local
```

| Camada | Responsabilidade |
|---|---|
| API | Receber dados, aplicar schemas, chamar serviços e produzir respostas HTTP |
| Service | Coordenar operações, commit/rollback e exceção de tarefa inexistente |
| Repository | Consultar e persistir modelos SQLAlchemy, sem commit/rollback próprio |
| SQLite | Armazenar tarefas e aplicar restrições de integridade |
| Integração OpenAI | Executar a chamada externa e validar a prioridade retornada |

O serviço de sugestão não utiliza Repository nem salva tarefas. O gerenciamento de sessões por requisição está em `app/database.py`; a tradução de `TaskNotFoundError` para HTTP 404 está na API.

```text
app/
├── main.py                   # Aplicação e inicialização das tabelas
├── database.py               # Engine, sessões e Base declarativa
├── models.py                 # Modelo Task
├── enums.py                  # Status e prioridades
├── schemas.py                # Contratos CRUD e validações compartilhadas
├── priority_schemas.py       # Contratos da sugestão
├── api/                      # Rotas de tarefas e sugestão
├── services/                 # Operações, sugestão e fallback
├── repositories/             # Persistência de tarefas
└── integrations/             # Cliente OpenAI
tests/                       # Testes das camadas e da API
docs/prompts.md              # Prompts, resultados e revisões humanas
```

## Pré-requisitos e instalação no Linux

É necessário Python 3.10 com os módulos `venv` e `pip` disponíveis, acesso ao índice de pacotes para instalação e permissão de escrita no diretório do banco. `curl` é necessário apenas para executar os exemplos pelo terminal. Não é necessário instalar um servidor SQLite separado ou possuir uma chave OpenAI para usar o CRUD e a sugestão local.

Após obter o código, entre na raiz do projeto e crie um ambiente virtual:

```bash
cd micro-api-tarefas-python
python3.10 --version
python3.10 -m venv .venv
source .venv/bin/activate
python --version
```

Instale as dependências da aplicação:

```bash
python -m pip install -r requirements.txt
```

Para desenvolver ou executar testes, instale as dependências de desenvolvimento, que também incluem as da aplicação:

```bash
python -m pip install -r requirements-dev.txt
python -m pip check
```

Em uma nova sessão do terminal, ative novamente o ambiente com `source .venv/bin/activate`. Para sair dele, use `deactivate`.

### Comandos com Makefile

Com `make` disponível, execute na raiz do projeto:

| Comando | Ação |
|---|---|
| `make install` | Instalar `requirements.txt` |
| `make install-dev` | Instalar `requirements-dev.txt` |
| `make run` | Iniciar a API com Uvicorn e `--reload` |
| `make test` | Executar os testes com Pytest |
| `make check` | Verificar dependências com `pip check` |

O [Makefile](Makefile) usa `PYTHON ?= python`: por padrão, utiliza o interpretador `python` do ambiente ativo. Ative a `.venv` antes de executar os comandos ou selecione o interpretador explicitamente, por exemplo: `make test PYTHON=.venv/bin/python`. Os comandos diretos documentados neste README continuam disponíveis.

## Execução e banco de dados

Com o ambiente ativado, execute na raiz:

```bash
python -m uvicorn app.main:app --reload
```

O servidor utiliza por padrão `http://127.0.0.1:8000`. A opção `--reload` é destinada ao desenvolvimento e à demonstração local.

Na inicialização do FastAPI, o lifespan executa `Base.metadata.create_all(bind=engine)`. Isso cria a tabela `tasks` se ela não existir. A importação dos módulos não abre conexão nem cria tabelas.

O banco padrão é `tarefas.db`, na raiz do projeto, com caminho absoluto derivado da localização do código. Para escolher outro arquivo SQLite, defina a variável antes de iniciar o servidor:

```bash
export DATABASE_URL="sqlite:///./tarefas_demo.db"
python -m uvicorn app.main:app --reload
```

Caminhos relativos da URL são resolvidos a partir do diretório de execução. Os dados permanecem no arquivo entre reinicializações; bancos locais com extensão `.db`, `.sqlite` ou `.sqlite3` são ignorados pelo Git. `create_all()` não migra tabelas existentes.

## Documentação interativa e saúde

- Swagger UI: <http://127.0.0.1:8000/docs>
- Especificação OpenAPI: <http://127.0.0.1:8000/openapi.json>
- Saúde: <http://127.0.0.1:8000/health>

```bash
curl http://127.0.0.1:8000/health
```

Resposta HTTP 200:

```json
{"status": "ok"}
```

`/health` confirma o funcionamento da rota; não verifica a disponibilidade da OpenAI.

## Contratos e endpoints

Uma tarefa contém `id`, `titulo`, `descricao`, `status` e `prioridade`. O ID é gerado pelo banco. O título é obrigatório, com 3 a 150 caracteres após remoção de espaços nas extremidades. A descrição é opcional, com até 2.000 caracteres após essa normalização; texto vazio vira `null`.

Status válidos: `pendente` e `concluida`. Prioridades válidas: `baixa`, `media` e `alta`. Valores de enum são enviados em minúsculas. Campos desconhecidos são rejeitados.

Na criação, a tarefa nasce pendente e a prioridade padrão é média; `id` e `status` não podem ser informados. No PATCH, campos omitidos são preservados; `descricao: null` remove a descrição. Título, status e prioridade não aceitam `null`, e atualização vazia é rejeitada.

| Método | Caminho | Operação | Sucesso |
|---|---|---|---|
| POST | `/tarefas` | Criar tarefa | 201 + tarefa |
| GET | `/tarefas` | Listar todas, em ordem crescente de ID | 200 + lista |
| GET | `/tarefas?status=pendente` | Filtrar; também aceita `concluida` | 200 + lista |
| GET | `/tarefas/{task_id}` | Consultar por ID | 200 + tarefa |
| PATCH | `/tarefas/{task_id}` | Atualizar parcialmente | 200 + tarefa |
| DELETE | `/tarefas/{task_id}` | Excluir definitivamente | 204 sem corpo |
| PATCH | `/tarefas/{task_id}/concluir` | Concluir sem corpo obrigatório | 200 + tarefa |
| POST | `/tarefas/sugerir-prioridade` | Sugerir com título e descrição | 200 + prioridade e origem |

IDs nas URLs devem ser inteiros positivos. Tarefa inexistente retorna 404; entradas inválidas, status de filtro inválido e campos extras retornam 422. Erros internos inesperados mantêm HTTP 500 com resposta genérica.

### Exemplos HTTP e JSON

Os comandos abaixo são exemplos do contrato implementado, não evidência de uma nova execução. O ID `1` pressupõe que essa tarefa exista; substitua pelo ID retornado no seu ambiente. Os exemplos seguem a sequência de criação, atualização, conclusão e exclusão.

**Criar:**

```bash
curl -i -X POST http://127.0.0.1:8000/tarefas \
  -H 'Content-Type: application/json' \
  -d '{"titulo":"Revisar projeto","descricao":"Preparar demonstracao"}'
```

Resposta HTTP 201, considerando ID gerado igual a 1:

```json
{"id":1,"titulo":"Revisar projeto","descricao":"Preparar demonstracao","status":"pendente","prioridade":"media"}
```

**Consultar e listar:**

```bash
curl http://127.0.0.1:8000/tarefas/1
curl http://127.0.0.1:8000/tarefas
curl 'http://127.0.0.1:8000/tarefas?status=pendente'
```

A consulta retorna o objeto acima com HTTP 200. Antes das alterações seguintes, a listagem e o filtro pendente retornam, se apenas essa tarefa estiver cadastrada:

```json
[{"id":1,"titulo":"Revisar projeto","descricao":"Preparar demonstracao","status":"pendente","prioridade":"media"}]
```

Lista vazia ou filtro sem correspondências retornam HTTP 200 com `[]`.

**Atualizar parcialmente e remover a descrição:**

```bash
curl -X PATCH http://127.0.0.1:8000/tarefas/1 \
  -H 'Content-Type: application/json' \
  -d '{"prioridade":"alta","descricao":null}'
```

Resposta HTTP 200:

```json
{"id":1,"titulo":"Revisar projeto","descricao":null,"status":"pendente","prioridade":"alta"}
```

**Concluir:**

```bash
curl -X PATCH http://127.0.0.1:8000/tarefas/1/concluir
```

Resposta HTTP 200:

```json
{"id":1,"titulo":"Revisar projeto","descricao":null,"status":"concluida","prioridade":"alta"}
```

Repetir a conclusão retorna a tarefa concluída sem erro, preservando título, descrição e prioridade.

**Solicitar sugestão local:** com `OPENAI_API_KEY` ausente e timeout configurado corretamente, execute:

```bash
curl -X POST http://127.0.0.1:8000/tarefas/sugerir-prioridade \
  -H 'Content-Type: application/json' \
  -d '{"titulo":"Corrigir falha urgente","descricao":null}'
```

Resposta HTTP 200:

```json
{"prioridade":"alta","origem":"local"}
```

Esse endpoint não cria tarefa nem aplica a prioridade a uma tarefa existente. Com uma resposta válida do provedor, `origem` será `ia`; a classificação pode variar.

**Excluir:**

```bash
curl -i -X DELETE http://127.0.0.1:8000/tarefas/1
```

Resposta HTTP 204, sem JSON ou corpo. Consultar novamente esse ID retorna HTTP 404:

```json
{"detail":"Tarefa 1 não encontrada."}
```

Para demonstrar HTTP 422, tente criar uma tarefa com `{"titulo":"ab"}`. A resposta contém uma lista `detail` de erros de validação; seu texto específico é produzido pelo FastAPI/Pydantic.

## Configuração opcional da OpenAI

| Variável | Padrão | Comportamento |
|---|---|---|
| `OPENAI_API_KEY` | Ausente | Sem chave, utiliza sugestão local |
| `OPENAI_MODEL` | `gpt-5-nano` | Modelo da chamada; valor explicitamente vazio desabilita a IA |
| `OPENAI_TIMEOUT_SECONDS` | `10` | Número positivo e finito para timeout do transporte |
| `OPENAI_BASE_URL` | Padrão do SDK | Sobrescreve o endereço do provedor se definida; normalmente deve permanecer ausente |

O arquivo [.env.example](.env.example) documenta `DATABASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL` e `OPENAI_TIMEOUT_SECONDS`, sem credenciais reais. O exemplo de `DATABASE_URL` está comentado para preservar o padrão calculado pela aplicação; a chave está vazia, com modelo `gpt-5-nano` e timeout de 10 segundos.

**O projeto não carrega `.env` automaticamente.** Copiar `.env.example` para `.env` não ativa a configuração: as variáveis devem estar no ambiente do processo que inicia o Uvicorn. Não há dependência de dotenv, e o Makefile também não carrega `.env`.

Para configurar no Bash sem escrever a chave no comando do histórico:

```bash
read -r -s -p "Chave OpenAI: " OPENAI_API_KEY
printf '\n'
export OPENAI_API_KEY
export OPENAI_MODEL="gpt-5-nano"
export OPENAI_TIMEOUT_SECONDS="10"
python -m uvicorn app.main:app --reload
```

Para uma demonstração exclusivamente local, em um novo início do servidor:

```bash
unset OPENAI_API_KEY
export OPENAI_TIMEOUT_SECONDS="10"
python -m uvicorn app.main:app --reload
```

A integração utiliza a Responses API com saída estruturada e validação por `TaskPriority`, retries automáticos desativados e `store=False`. Falhas previstas de comunicação, timeout, erro HTTP do provedor, recusa, resposta incompleta ou inválida acionam o fallback. Configuração inválida de timeout e defeitos inesperados não são mascarados como fallback.

Chamadas reais exigem acesso ao modelo e podem gerar cobrança, além de enviar título e descrição ao provedor. Não inclua dados sensíveis ou credenciais nesses campos. O timeout não representa garantia absoluta de duração total, e `store=False` não garante ausência de toda retenção pelo provedor. A qualidade e a latência da classificação não foram avaliadas com inferência real nas etapas registradas.

## Fallback local

O fallback é a função determinística `suggest_priority()`, usada sem configuração de IA ou quando ocorre uma falha prevista. Ela compara palavras inteiras do título e da descrição sem diferenciar maiúsculas e minúsculas.

| Prioridade | Palavras-chave |
|---|---|
| Alta | `urgente`, `emergência`, `emergencia`, `crítico`, `critico` |
| Média | `importante`, `prazo`, `revisar` |
| Baixa | `opcional`, `rotina`, `depois` |

A precedência é **alta > média > baixa**. Sem correspondência, o resultado é `media`. As variantes sem acento são explícitas; não há reconhecimento automático de flexões ou sinônimos.

A heurística não interpreta negações ou contexto: por exemplo, “não é urgente” ainda sugere alta. A sugestão deve ser revisada por uma pessoa antes de ser aplicada pelo CRUD.

## Testes automatizados

Na raiz, com o ambiente ativado e `requirements-dev.txt` instalado:

```bash
python -m pytest -q
python -m pip check
```

Os testes cobrem schemas, enums, modelos, Repository, Service, fallback local, cliente OpenAI e contratos HTTP. Utilizam SQLite temporário, sessões isoladas e substituição de dependências; a inicialização do FastAPI também usa banco de teste. Chamadas ao provedor são simuladas por mocks e transporte HTTP simulado, sem consumir créditos da API.

O último resultado registrado para a implementação até a Etapa 2.8.2.2 é **355 testes aprovados**, com um aviso de depreciação interno do Starlette/AnyIO. Esse resultado está documentado em [docs/prompts.md](docs/prompts.md); não representa uma nova execução feita para editar este README nem uma medição percentual de cobertura.

As dependências diretas estão fixadas, mas as transitivas não possuem um arquivo de lock completo. Uma instalação nova deverá ser validada antes da submissão.

## Uso de IA no desenvolvimento

Codex auxiliou na leitura do projeto, planejamento, implementação incremental, testes e verificações do Git. ChatGPT apoiou discussões técnicas e revisões dos arquivos, conforme relatado pelo responsável pelo projeto.

As entregas foram submetidas à revisão humana antes dos commits autorizados. Código gerado não foi considerado correto apenas por sua origem: houve testes automatizados, refinamentos e validação manual relatada. Os principais prompts, decisões, resultados e aprovações estão em [docs/prompts.md](docs/prompts.md), seguindo as orientações de [AGENTS.md](AGENTS.md).

A assistência no desenvolvimento é distinta da funcionalidade de sugestão: essa funcionalidade chama a OpenAI apenas quando configurada e solicitada pelo endpoint, com fallback local. Não há alegação de ganho quantitativo de produtividade.

## Limitações conhecidas e melhorias futuras

- Escopo acadêmico e execução local; não há autenticação, autorização, paginação, busca por título ou frontend.
- SQLite é um banco em arquivo; não foram realizados testes de carga ou avaliação de uso concorrente em produção.
- `create_all()` não atualiza a estrutura de tabelas existentes; migrações com Alembic não foram implementadas.
- Uma falha de leitura/refresh após commit pode retornar 500 mesmo com a operação de escrita já confirmada.
- A classificação por IA não é determinística; o fallback é limitado às palavras-chave documentadas.
- A prioridade sugerida não é aplicada automaticamente; o usuário decide se deseja utilizá-la ao criar ou atualizar uma tarefa.
- Não há pipeline CI definido nesta entrega.

Possíveis melhorias futuras incluem validação em ambiente limpo, fixação das dependências transitivas, pipeline de testes e versão de entrega. Autenticação, paginação e migrações exigem novas etapas de requisitos e revisão; não fazem parte das funcionalidades atuais.

## Roteiro básico de demonstração

1. Apresentar o objetivo, a arquitetura e os arquivos de dependências.
2. Iniciar a API sem chave OpenAI, com timeout válido, e acessar `/health` e `/docs`.
3. Criar uma tarefa pelo Swagger; usar o ID retornado para consultar e atualizar parcialmente.
4. Remover a descrição com `null`, concluir a tarefa e repetir a conclusão.
5. Comparar a lista completa com os filtros `pendente` e `concluida`.
6. Solicitar uma sugestão com “urgente” e outra com “opcional”, mostrando `origem: local` e ausência de persistência da sugestão.
7. Demonstrar uma entrada inválida (422), excluir a tarefa (204) e consultá-la novamente (404).
8. Executar os testes e mostrar os resultados efetivamente obtidos, além do registro de revisão humana.

Se desejar separar dados da demonstração, utilize um novo arquivo via `DATABASE_URL`, sem apagar o banco de desenvolvimento. Não é necessário fazer chamadas reais à OpenAI para apresentar o fluxo, o fallback ou os testes da integração.

## Licença

Este projeto está sob a [licença MIT](LICENSE).
