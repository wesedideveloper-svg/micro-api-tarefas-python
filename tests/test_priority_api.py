from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from app import main
from app.database import get_db
from app.enums import TaskPriority
from app.integrations.openai_priority_client import OpenAIPriorityClient, PriorityIntegrationError
from app.services.priority_suggestion_service import PrioritySuggestionService


URL = "/tarefas/sugerir-prioridade"


@pytest.fixture(autouse=True)
def prevent_real_openai_calls(monkeypatch):
    monkeypatch.setattr(
        OpenAIPriorityClient, "suggest",
        Mock(side_effect=AssertionError("Chamada externa proibida neste teste")),
    )
    for name in ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_TIMEOUT_SECONDS"):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def service_factory(monkeypatch):
    ai_client = Mock(spec=OpenAIPriorityClient)
    ai_client.suggest.return_value = TaskPriority.MEDIA
    factory = Mock(return_value=PrioritySuggestionService(ai_client))
    monkeypatch.setattr(PrioritySuggestionService, "from_env", factory)
    return factory, ai_client


@pytest.mark.parametrize("priority", list(TaskPriority))
def test_ai_success_returns_200_and_normalized_inputs(client, service_factory, priority):
    factory, ai_client = service_factory
    ai_client.suggest.return_value = priority
    response = client.post(URL, json={"titulo": "  Tarefa  ", "descricao": "  Descrição  "})
    assert response.status_code == 200
    assert response.json() == {"prioridade": priority.value, "origem": "ia"}
    factory.assert_called_once_with()
    ai_client.suggest.assert_called_once_with("Tarefa", "Descrição")


@pytest.mark.parametrize(
    ("title", "description", "expected"),
    [("Urgente", None, "alta"), ("Tarefa", "Opcional", "baixa"),
     ("Organizar documentos", None, "media")],
)
def test_expected_ai_failure_returns_real_local_fallback(
    client, service_factory, title, description, expected
):
    _, ai_client = service_factory
    ai_client.suggest.side_effect = PriorityIntegrationError("Falha prevista")
    response = client.post(URL, json={"titulo": title, "descricao": description})
    assert response.status_code == 200
    assert response.json() == {"prioridade": expected, "origem": "local"}


def test_missing_configuration_uses_local_fallback_without_external_call(client):
    response = client.post(URL, json={"titulo": "Atividade opcional"})
    assert response.status_code == 200
    assert response.json() == {"prioridade": "baixa", "origem": "local"}
    OpenAIPriorityClient.suggest.assert_not_called()


@pytest.mark.parametrize("description", [None, "", " \t\n "])
def test_description_null_or_blank_is_normalized(client, service_factory, description):
    _, ai_client = service_factory
    assert client.post(URL, json={"titulo": "Tarefa", "descricao": description}).status_code == 200
    ai_client.suggest.assert_called_once_with("Tarefa", None)


@pytest.mark.parametrize("length", [3, 150])
def test_valid_boundaries_are_checked_after_trim(client, service_factory, length):
    _, ai_client = service_factory
    response = client.post(URL, json={
        "titulo": "  " + "a" * length + "  ",
        "descricao": "  " + "b" * 2000 + "  ",
    })
    assert response.status_code == 200
    ai_client.suggest.assert_called_once_with("a" * length, "b" * 2000)


@pytest.mark.parametrize("payload", [
    {}, {"titulo": None}, {"titulo": "   "}, {"titulo": " ab "},
    {"titulo": "a" * 151}, {"titulo": 123},
    {"titulo": "Tarefa", "descricao": "a" * 2001},
    {"titulo": "Tarefa", "descricao": 123},
    {"titulo": "Tarefa", "prioridade": "alta"},
    {"titulo": "Tarefa", "status": "pendente"},
    {"titulo": "Tarefa", "id": 1}, {"titulo": "Tarefa", "extra": True},
])
def test_invalid_body_returns_422_before_service_configuration(client, service_factory, payload):
    factory, ai_client = service_factory
    response = client.post(URL, json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()
    factory.assert_not_called()
    ai_client.suggest.assert_not_called()


def test_body_is_required(client, service_factory):
    factory, _ = service_factory
    assert client.post(URL).status_code == 422
    factory.assert_not_called()


def test_route_order_and_openapi_documentation(client):
    paths = [route.path for route in main.app.routes]
    assert paths.index(URL) < paths.index("/tarefas/{task_id}")
    schema = client.get("/openapi.json").json()
    operation = schema["paths"][URL]["post"]
    assert operation["requestBody"]["required"] is True
    assert {"200", "422"} <= set(operation["responses"])
    models = schema["components"]["schemas"]
    request = models["PrioritySuggestionRequest"]
    response = models["PrioritySuggestionResponse"]
    assert request["required"] == ["titulo"]
    assert request["additionalProperties"] is False
    assert request["properties"]["titulo"]["minLength"] == 3
    assert request["properties"]["titulo"]["maxLength"] == 150
    assert response["additionalProperties"] is False
    assert response["properties"]["prioridade"]["$ref"] == "#/components/schemas/TaskPriority"
    assert response["properties"]["origem"]["enum"] == ["ia", "local"]
    assert client.get("/docs").status_code == 200


def test_suggestion_does_not_depend_on_database_session(client, monkeypatch, service_factory):
    def forbidden_db():
        raise AssertionError("Sugestão solicitou sessão de banco")

    monkeypatch.setitem(main.app.dependency_overrides, get_db, forbidden_db)
    assert client.post(URL, json={"titulo": "Tarefa"}).status_code == 200


def test_suggestion_preserves_tasks_and_existing_crud(client, service_factory):
    _, ai_client = service_factory
    ai_client.suggest.return_value = TaskPriority.ALTA
    created = client.post("/tarefas", json={"titulo": "Original", "prioridade": "baixa"})
    assert created.status_code == 201
    task = created.json()
    assert client.post(URL, json={"titulo": "Urgente"}).json() == {
        "prioridade": "alta", "origem": "ia"
    }
    assert client.get("/tarefas").json() == [task]
    assert client.get(f"/tarefas/{task['id']}").json() == task
    assert client.patch(f"/tarefas/{task['id']}", json={"titulo": "Atualizada"}).status_code == 200
    assert client.delete(f"/tarefas/{task['id']}").status_code == 204
    assert client.get("/tarefas").json() == []


def test_unexpected_error_returns_generic_500(client, service_factory):
    _, ai_client = service_factory
    ai_client.suggest.side_effect = RuntimeError("segredo interno")
    response = client.post(URL, json={"titulo": "Tarefa"})
    assert response.status_code == 500
    assert response.text == "Internal Server Error"


@pytest.mark.parametrize(
    "result", [SimpleNamespace(prioridade="invalida", origem="ia"),
               SimpleNamespace(prioridade="alta", origem="invalida")],
)
def test_response_contract_rejects_invalid_service_output(client, service_factory, result):
    factory, _ = service_factory
    factory.return_value = Mock(suggest=Mock(return_value=result))
    response = client.post(URL, json={"titulo": "Tarefa"})
    assert response.status_code == 500
    assert response.text == "Internal Server Error"
