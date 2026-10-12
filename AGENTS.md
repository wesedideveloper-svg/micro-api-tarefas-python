# Instruções para o Codex — Micro-API de Tarefas

## 1. Objetivo
Desenvolver uma Micro-API RESTful de Gerenciamento de Tarefas, como miniprojeto acadêmico da pós-graduação em Engenharia de Software com Inteligência Artificial Generativa.

## 2. Tecnologias
- Python 3.10
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- Pytest
- Git

## 3. Arquitetura
Organizar a aplicação em camadas:

API → Service → Repository → SQLite

Manter separadas as responsabilidades de cada camada.

## 4. Funcionalidades
- Criar tarefas
- Listar tarefas
- Consultar tarefa por ID
- Atualizar tarefas
- Excluir tarefas
- Marcar tarefas como concluídas
- Filtrar tarefas por status
- Sugerir prioridade com IA, utilizando fallback local quando necessário

## 5. Regras de desenvolvimento
- Priorizar soluções simples e adequadas ao escopo acadêmico.
- Implementar uma funcionalidade por vez.
- Não adicionar bibliotecas ou funcionalidades sem justificativa.
- Utilizar validação de dados com Pydantic.
- Aplicar boas práticas de organização, nomenclatura e tratamento de erros.
- Criar testes automatizados com Pytest.
- Documentar as funcionalidades implementadas.
- Não armazenar credenciais diretamente no código.
- Não executar commits automaticamente.
- Não alterar arquivos fora do escopo solicitado.

## 6. Uso da inteligência artificial
- Utilizar IA como assistente de desenvolvimento.
- Explicar as alterações propostas.
- Permitir revisão humana antes de mudanças importantes.
- Registrar os principais prompts utilizados no desenvolvimento.
- Não considerar código gerado como correto sem validação e testes.

## 7. Processo de implementação
1. Criar a estrutura inicial da aplicação.
2. Implementar modelos e validações.
3. Configurar persistência SQLite.
4. Implementar Repository e Service.
5. Implementar endpoints REST.
6. Criar testes automatizados.
7. Integrar sugestão de prioridade com IA.
8. Revisar, refatorar e documentar.

## 8. Orientação final

Antes de implementar qualquer funcionalidade, analisar o README.md e este AGENTS.md. Em caso de dúvida sobre requisitos.