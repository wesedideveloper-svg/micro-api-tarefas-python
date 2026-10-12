import os
import subprocess
import sys

import pytest
from sqlalchemy import inspect

from app import main
from app.services.task_service import TaskService


def test_post_defaults_and_get_existing_task(client):
    response = client.post("/tarefas", json={"titulo": "  Estudar Python  "})
    assert response.status_code == 201
    task = response.json()
    assert task == {
        "id": task["id"], "titulo": "Estudar Python", "descricao": None,
        "status": "pendente", "prioridade": "media",
    }
    assert type(task["id"]) is int and task["id"] > 0
    recovered = client.get(f"/tarefas/{task['id']}")
    assert recovered.status_code == 200
    assert recovered.json() == task


def test_list_empty_and_ordered_with_persistence_between_requests(client):
    response = client.get("/tarefas")
    assert response.status_code == 200
    assert response.json() == []
    tasks = [client.post("/tarefas", json={"titulo": title}).json()
             for title in ("Primeira", "Segunda")]
    response = client.get("/tarefas")
    assert response.status_code == 200
    assert response.json() == tasks
    assert [task["id"] for task in response.json()] == sorted(task["id"] for task in tasks)


@pytest.mark.parametrize("description", ["Nova descrição", None])
def test_patch_partial_and_description_removal(client, description):
    task = client.post("/tarefas", json={
        "titulo": "Original", "descricao": "Descrição", "prioridade": "alta"
    }).json()
    response = client.patch(f"/tarefas/{task['id']}", json={"descricao": description})
    assert response.status_code == 200
    expected = task | {"descricao": description}
    assert response.json() == expected
    assert client.get(f"/tarefas/{task['id']}").json() == expected


def test_patch_title_status_and_priority(client):
    task_id = client.post("/tarefas", json={"titulo": "Original"}).json()["id"]
    changes = {"titulo": "Atualizada", "status": "concluida", "prioridade": "alta"}
    response = client.patch(f"/tarefas/{task_id}", json=changes)
    assert response.status_code == 200
    assert response.json() == {"id": task_id, "descricao": None, **changes}
    assert client.get(f"/tarefas/{task_id}").json() == response.json()


def test_delete_returns_empty_204_and_persists(client):
    task_id = client.post("/tarefas", json={"titulo": "Tarefa"}).json()["id"]
    response = client.delete(f"/tarefas/{task_id}")
    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/tarefas/{task_id}").status_code == 404
    assert client.get("/tarefas").json() == []


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_missing_task_returns_404(client, method):
    kwargs = {"json": {"titulo": "Atualizada"}} if method == "patch" else {}
    response = client.request(method, "/tarefas/999", **kwargs)
    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa 999 não encontrada."}


@pytest.mark.parametrize("payload", [
    {}, {"titulo": "ab"}, {"titulo": "Tarefa", "prioridade": "urgente"},
    {"titulo": "Tarefa", "status": "pendente"},
    {"titulo": "Tarefa", "id": 1}, {"titulo": "Tarefa", "extra": True},
])
def test_invalid_post_returns_422_without_persistence(client, payload):
    response = client.post("/tarefas", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()
    assert client.get("/tarefas").json() == []


@pytest.mark.parametrize("payload", [
    {}, {"titulo": None}, {"status": "invalido"}, {"prioridade": None}, {"extra": True},
])
def test_invalid_patch_returns_422_without_changes(client, payload):
    task = client.post("/tarefas", json={"titulo": "Original"}).json()
    response = client.patch(f"/tarefas/{task['id']}", json=payload)
    assert response.status_code == 422
    assert client.get(f"/tarefas/{task['id']}").json() == task


@pytest.mark.parametrize("task_id", ["texto", "0", "-1"])
def test_invalid_path_returns_422(client, task_id):
    assert client.get(f"/tarefas/{task_id}").status_code == 422


def test_swagger_and_openapi_document_crud(client):
    docs = client.get("/docs")
    assert docs.status_code == 200
    assert "swagger-ui" in docs.text
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    assert set(schema["paths"]["/tarefas"]) == {"post", "get"}
    assert set(schema["paths"]["/tarefas/{task_id}"]) == {"get", "patch", "delete"}
    assert "201" in schema["paths"]["/tarefas"]["post"]["responses"]
    deletion = schema["paths"]["/tarefas/{task_id}"]["delete"]["responses"]["204"]
    assert "content" not in deletion


def test_unexpected_error_returns_500_without_sensitive_details(client, monkeypatch):
    def fail(self, status=None):
        raise RuntimeError("segredo: senha-de-teste")

    monkeypatch.setattr(TaskService, "list_all", fail)
    response = client.get("/tarefas")
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
    assert "senha-de-teste" not in response.text


def test_lifespan_creates_tasks_in_temporary_database(client, tmp_path):
    assert main.engine.url.database == str(tmp_path / "api.db")
    assert inspect(main.engine).has_table("tasks")


def test_import_main_does_not_connect_or_create_tables(tmp_path):
    database_file = tmp_path / "not_created.db"
    environment = os.environ.copy()
    environment["DATABASE_URL"] = f"sqlite:///{database_file}"
    result = subprocess.run(
        [sys.executable, "-c", "from unittest.mock import patch\n"
         "with patch('sqlite3.dbapi2.connect', side_effect=AssertionError('connection')), "
         "patch('sqlalchemy.MetaData.create_all', side_effect=AssertionError('tables')):\n"
         "    import app.main\n"],
        env=environment, capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert not database_file.exists()


@pytest.mark.parametrize("already_completed", [False, True])
def test_complete_task_without_body_preserves_fields_and_persists(client, already_completed):
    task = client.post("/tarefas", json={
        "titulo": "Tarefa", "descricao": "Descrição", "prioridade": "alta"
    }).json()
    if already_completed:
        client.patch(f"/tarefas/{task['id']}", json={"status": "concluida"})
    response = client.patch(f"/tarefas/{task['id']}/concluir")
    assert response.status_code == 200
    assert response.json() == task | {"status": "concluida"}
    assert client.get(f"/tarefas/{task['id']}").json() == response.json()


def test_complete_missing_task_returns_404(client):
    response = client.patch("/tarefas/999/concluir")
    assert response.status_code == 404
    assert response.json() == {"detail": "Tarefa 999 não encontrada."}


@pytest.mark.parametrize("status", ["pendente", "concluida"])
def test_list_filters_by_status_and_keeps_id_order(client, status):
    tasks = [client.post("/tarefas", json={"titulo": f"Tarefa {index}"}).json()
             for index in range(4)]
    for index in (1, 3):
        tasks[index] = client.patch(f"/tarefas/{tasks[index]['id']}/concluir").json()
    response = client.get("/tarefas", params={"status": status})
    assert response.status_code == 200
    assert response.json() == [task for task in tasks if task["status"] == status]
    assert client.get("/tarefas").json() == tasks


@pytest.mark.parametrize("status", ["invalido", "PENDENTE", ""])
def test_invalid_status_filter_returns_422(client, status):
    response = client.get("/tarefas", params={"status": status})
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["query", "status"]


@pytest.mark.parametrize("status", ["pendente", "concluida"])
def test_status_filter_without_matches_returns_empty_list(client, status):
    task_id = client.post("/tarefas", json={"titulo": "Tarefa"}).json()["id"]
    if status == "pendente":
        client.patch(f"/tarefas/{task_id}/concluir")
    response = client.get("/tarefas", params={"status": status})
    assert response.status_code == 200
    assert response.json() == []


def test_openapi_documents_completion_and_optional_enum_filter(client):
    schema = client.get("/openapi.json").json()
    completion = schema["paths"]["/tarefas/{task_id}/concluir"]["patch"]
    assert "requestBody" not in completion
    assert {"200", "404", "422"} <= set(completion["responses"])
    parameters = schema["paths"]["/tarefas"]["get"]["parameters"]
    status = next(parameter for parameter in parameters if parameter["name"] == "status")
    assert status["in"] == "query" and status["required"] is False
    assert {"$ref": "#/components/schemas/TaskStatus"} in status["schema"]["anyOf"]
    assert schema["components"]["schemas"]["TaskStatus"]["enum"] == ["pendente", "concluida"]
