from unittest.mock import Mock

import pytest

from app.enums import TaskPriority
from app.integrations.openai_priority_client import OpenAIPriorityClient, PriorityIntegrationError
from app.services import priority_suggestion_service as module
from app.services.priority_suggestion_service import PrioritySuggestionService


@pytest.mark.parametrize("priority", list(TaskPriority))
def test_ai_success_does_not_use_fallback(monkeypatch, priority):
    client = Mock(spec=OpenAIPriorityClient)
    client.suggest.return_value = priority
    fallback = Mock(side_effect=AssertionError("Fallback após sucesso"))
    monkeypatch.setattr(module, "suggest_priority", fallback)
    result = PrioritySuggestionService(client).suggest("Título", "Descrição")
    assert result.prioridade is priority and result.origem == "ia"
    client.suggest.assert_called_once_with("Título", "Descrição")
    fallback.assert_not_called()


@pytest.mark.parametrize("configured", [False, True])
@pytest.mark.parametrize(
    ("title", "description", "expected"),
    [("Urgente", None, TaskPriority.ALTA), ("Tarefa", "Opcional", TaskPriority.BAIXA),
     ("", None, TaskPriority.MEDIA)],
)
def test_expected_failure_or_missing_client_uses_local_fallback(
    configured, title, description, expected
):
    client = Mock(spec=OpenAIPriorityClient) if configured else None
    if client is not None:
        client.suggest.side_effect = PriorityIntegrationError("Falha prevista")
    result = PrioritySuggestionService(client).suggest(title, description)
    assert result.prioridade is expected and result.origem == "local"


def test_fallback_preserves_original_texts(monkeypatch):
    client = Mock(spec=OpenAIPriorityClient)
    client.suggest.side_effect = PriorityIntegrationError("Falha prevista")
    fallback = Mock(return_value=TaskPriority.MEDIA)
    monkeypatch.setattr(module, "suggest_priority", fallback)
    PrioritySuggestionService(client).suggest("  TÍTULO  ", "Descrição! ")
    fallback.assert_called_once_with("  TÍTULO  ", "Descrição! ")


def test_unexpected_failure_propagates_without_fallback(monkeypatch):
    client = Mock(spec=OpenAIPriorityClient)
    failure = RuntimeError("Defeito simulado")
    client.suggest.side_effect = failure
    fallback = Mock()
    monkeypatch.setattr(module, "suggest_priority", fallback)
    with pytest.raises(RuntimeError) as error:
        PrioritySuggestionService(client).suggest("Título")
    assert error.value is failure
    fallback.assert_not_called()


def test_from_environment_without_key_uses_local_service(monkeypatch):
    for name in ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_TIMEOUT_SECONDS"):
        monkeypatch.delenv(name, raising=False)
    result = PrioritySuggestionService.from_env().suggest("Urgente")
    assert result.prioridade is TaskPriority.ALTA and result.origem == "local"


def test_configuration_errors_are_not_disguised_as_fallback(monkeypatch):
    monkeypatch.setenv("OPENAI_TIMEOUT_SECONDS", "invalido")
    with pytest.raises(ValueError):
        PrioritySuggestionService.from_env()
