# Roteiro de demonstração acadêmica — Unidade V

Projeto: **micro-api-tarefas-python**. Duração estimada: **4 minutos e 45 segundos**.

## Preparação antes da apresentação

Na raiz do projeto, com a `.venv` existente e as dependências já instaladas, execute:

```bash
source .venv/bin/activate
unset OPENAI_API_KEY
export OPENAI_TIMEOUT_SECONDS="10"
make run
```

Remova a chave do ambiente **antes de iniciar o servidor**. Se ele já estiver rodando com uma chave, encerre-o com `Ctrl+C` e reinicie com os comandos acima. Sem chave e com timeout válido, o serviço utiliza o fallback local sem criar uma chamada à OpenAI. Não é necessário configurar uma chave fictícia nem provocar falhas de rede. A aplicação e o Makefile não carregam `.env` automaticamente.

Abra <http://127.0.0.1:8000/docs>. No Swagger, expanda a operação, clique em **Try it out**, preencha os dados e clique em **Execute**. Deixe um segundo terminal na raiz do projeto com a `.venv` ativada para demonstrar os testes.

O banco pode conter tarefas anteriores: anote o `id` retornado na criação e use esse valor nas operações seguintes. Não suponha que seja `1` e não exclua tarefas anteriores.

## 1. Objetivo acadêmico — 0:00 a 0:20 (20 segundos)

**Fala sugerida:** “Este projeto acadêmico é uma API REST para organizar tarefas por status e prioridade. Ele permite cadastrar, consultar, atualizar, concluir e excluir tarefas. O objetivo foi praticar arquitetura em camadas, validação, persistência e testes, com apoio de IA e revisão humana.”

## 2. Arquitetura e execução — 0:20 a 0:45 (25 segundos)

Mostre brevemente os comandos de preparação e o servidor iniciado com `make run`.

**Fala sugerida:** “A API recebe e valida as requisições. O Service coordena as operações e controla commit e rollback. O Repository executa a persistência com SQLAlchemy, e o SQLite armazena os dados. A sugestão de prioridade tem um serviço separado e não salva tarefas.”

Fluxo principal: **FastAPI → Service → Repository → SQLite**.

Abra o Swagger em <http://127.0.0.1:8000/docs> e execute `GET /health`: HTTP 200 com `{"status":"ok"}`.

## 3. Criação e consulta — 0:45 a 1:25 (40 segundos)

Execute `POST /tarefas` com:

```json
{
  "titulo": "Preparar apresentação acadêmica",
  "descricao": "Organizar exemplos para o professor"
}
```

Mostre o HTTP **201** e anote o `id` real da resposta. Confirme `status: "pendente"` e `prioridade: "media"`, valores padrão da criação.

Execute `GET /tarefas/{task_id}` usando esse ID. Mostre o HTTP **200** e os mesmos dados. Execute `GET /tarefas` sem filtro: a lista pode conter outras tarefas, ordenadas por ID crescente.

**Fala sugerida:** “O ID é gerado pelo banco. A tarefa começa pendente, e o contrato de entrada rejeita campos que não pertencem à criação.”

## 4. Atualização e conclusão — 1:25 a 2:05 (40 segundos)

Execute `PATCH /tarefas/{task_id}` com o ID anotado e:

```json
{
  "prioridade": "alta",
  "descricao": null
}
```

Mostre o HTTP **200**: a prioridade mudou para `alta`, a descrição foi removida e o título foi preservado. Campos omitidos não são alterados.

Execute `PATCH /tarefas/{task_id}/concluir` com o mesmo ID, sem corpo. Confirme HTTP **200**, `status: "concluida"` e preservação dos demais campos. Repita a operação para mostrar que uma tarefa já concluída continua retornando HTTP 200.

## 5. Filtro por status — 2:05 a 2:25 (20 segundos)

Em `GET /tarefas`, execute com o parâmetro `status` igual a `concluida`: localize o ID da tarefa demonstrada. Depois execute com `pendente`: esse ID não deve aparecer.

**Fala sugerida:** “O filtro é opcional e executado no banco. Sem filtro, todas as tarefas são retornadas; sem correspondências, a resposta é uma lista vazia com HTTP 200.”

Outras tarefas podem aparecer nos resultados. Não espere listas vazias ou uma quantidade fixa de registros.

## 6. Sugestão de prioridade com fallback local — 2:25 a 3:00 (35 segundos)

Execute `POST /tarefas/sugerir-prioridade` com:

```json
{
  "titulo": "Corrigir falha urgente",
  "descricao": null
}
```

Resposta esperada, HTTP **200**:

```json
{
  "prioridade": "alta",
  "origem": "local"
}
```

Se houver tempo, repita com:

```json
{
  "titulo": "Organizar atividade opcional",
  "descricao": null
}
```

Resposta esperada: `{"prioridade":"baixa","origem":"local"}`.

**Fala sugerida:** “A integração OpenAI está implementada, mas esta demonstração usa exclusivamente o fallback local, pois iniciamos sem chave. Ele classifica por palavras-chave, com precedência alta, média e baixa; sem correspondência, sugere média. O endpoint apenas sugere: não cria nem altera uma tarefa.”

## 7. Validação e tarefa inexistente — 3:00 a 3:35 (35 segundos)

Execute `POST /tarefas` com:

```json
{
  "titulo": "ab"
}
```

Mostre HTTP **422** e a lista de erros em `detail`: o título exige de 3 a 150 caracteres após remover espaços das extremidades. A descrição aceita até 2.000 caracteres, e campos extras são rejeitados.

Para demonstrar 404 sem adivinhar um ID inexistente, execute `DELETE /tarefas/{task_id}` **somente para a tarefa criada nesta apresentação**. Mostre HTTP **204**, sem corpo. Em seguida, consulte o mesmo ID com `GET /tarefas/{task_id}`: HTTP **404**, com `detail` informando que a tarefa não foi encontrada.

## 8. Testes automatizados — 3:35 a 4:00 (25 segundos)

No segundo terminal, com a `.venv` ativada, execute:

```bash
make test
```

Mostre o resumo efetivamente obtido. Na validação técnica da Etapa 3.3 foram aprovados **355 testes**, com um aviso de depreciação interno do Starlette/AnyIO e sem falhas; esse registro não substitui o resultado da execução durante a apresentação.

**Fala sugerida:** “Os testes cobrem contratos, persistência, serviços e endpoints. Usam SQLite temporário e mocks para a OpenAI, sem acessar o banco de desenvolvimento nem consumir créditos.”

## 9. Assistência de IA e revisão humana — 4:00 a 4:20 (20 segundos)

**Fala sugerida:** “ChatGPT apoiou discussões e revisões, e Codex auxiliou no planejamento, implementação incremental e verificações. Cada entrega passou por testes e revisão humana antes do commit autorizado. Os principais prompts, decisões e aprovações estão em `docs/prompts.md`.”

## 10. Limitações e encerramento — 4:20 a 4:45 (25 segundos)

**Fala sugerida:** “A API atende ao escopo acadêmico local. Ainda não possui autenticação, paginação, frontend ou migrações. O fallback não interpreta contexto ou negações, e a sugestão precisa de avaliação humana. Melhorias futuras podem incluir CI, dependências transitivas fixadas, migrações e autenticação. A entrega demonstra funcionalidades implementadas, documentação e validação automatizada.”

Não é necessário realizar chamadas reais à OpenAI para demonstrar o projeto. A qualidade da classificação com inferência real não foi avaliada nas etapas registradas.
