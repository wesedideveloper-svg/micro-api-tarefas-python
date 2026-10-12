import json
from types import SimpleNamespace
from unittest.mock import patch

import httpx2
import pytest
from openai import APIConnectionError, APIResponseValidationError, APIStatusError, APITimeoutError

from app.enums import TaskPriority
from app.integrations import openai_priority_client as integration
from app.integrations.openai_priority_client import OpenAIPriorityClient, PriorityIntegrationError


@pytest.fixture(autouse=True)
def isolated_configuration(monkeypatch):
    for name in ("OPENAI_API_KEY", "OPENAI_MODEL", "OPENAI_TIMEOUT_SECONDS", "OPENAI_BASE_URL"):
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def sdk():
    # Autospec também verifica a assinatura real do construtor do SDK.
    with patch.object(integration, "OpenAI", autospec=True) as factory:
        yield factory, factory.return_value.__enter__.return_value


@pytest.mark.parametrize("priority", list(TaskPriority))
def test_structured_response_returns_validated_enum(sdk, priority):
    factory, client = sdk
    client.responses.parse.return_value = SimpleNamespace(
        status="completed", output_parsed=SimpleNamespace(prioridade=priority.value)
    )
    adapter = OpenAIPriorityClient("fake-test-key", model="gpt-5-nano", timeout=3.5)
    assert adapter.suggest("Título", "Descrição") is priority
    factory.assert_called_once_with(
        api_key="fake-test-key", timeout=3.5, max_retries=0,
    )
    arguments = client.responses.parse.call_args.kwargs
    assert arguments["model"] == "gpt-5-nano"
    assert arguments["store"] is False
    assert arguments["max_output_tokens"] == 1024
    assert json.loads(arguments["input"]) == {"titulo": "Título", "descricao": "Descrição"}
    schema = arguments["text_format"].model_json_schema()
    assert schema["additionalProperties"] is False
    assert schema["$defs"]["TaskPriority"]["enum"] == ["baixa", "media", "alta"]
    factory.return_value.__exit__.assert_called_once()


def test_optional_description_is_sent_as_null(sdk):
    _, client = sdk
    client.responses.parse.return_value = SimpleNamespace(
        status="completed", output_parsed=SimpleNamespace(prioridade="media")
    )
    OpenAIPriorityClient("fake-test-key").suggest("Tarefa")
    assert json.loads(client.responses.parse.call_args.kwargs["input"])["descricao"] is None


@pytest.mark.parametrize("status", ["incomplete", "failed", "cancelled", "in_progress"])
def test_non_completed_response_is_expected_failure(sdk, status):
    _, client = sdk
    client.responses.parse.return_value = SimpleNamespace(status=status, output_parsed=None)
    with pytest.raises(PriorityIntegrationError):
        OpenAIPriorityClient("fake-test-key").suggest("Tarefa")


def test_missing_or_refused_output_is_expected_failure(sdk):
    _, client = sdk
    client.responses.parse.return_value = SimpleNamespace(status="completed", output_parsed=None)
    with pytest.raises(PriorityIntegrationError):
        OpenAIPriorityClient("fake-test-key").suggest("Tarefa")


@pytest.mark.parametrize("value", ["urgente", "ALTA", "", None, 1])
def test_invalid_priority_is_expected_failure(sdk, value):
    _, client = sdk
    client.responses.parse.return_value = SimpleNamespace(
        status="completed", output_parsed=SimpleNamespace(prioridade=value)
    )
    with pytest.raises(PriorityIntegrationError):
        OpenAIPriorityClient("fake-test-key").suggest("Tarefa")


@pytest.mark.parametrize("status_code", [400, 401, 403, 404, 429, 500])
def test_provider_http_errors_are_expected_failures(sdk, status_code):
    _, client = sdk
    response = httpx2.Response(status_code, request=httpx2.Request("POST", "https://example.test"))
    failure = APIStatusError("Simulado", response=response, body=None)
    client.responses.parse.side_effect = failure
    with pytest.raises(PriorityIntegrationError) as error:
        OpenAIPriorityClient("fake-test-key").suggest("Tarefa")
    assert error.value.__cause__ is failure
    assert str(error.value) == "Falha na comunicação com o provedor."


@pytest.mark.parametrize("error_type", [APIConnectionError, APITimeoutError])
def test_connection_and_timeout_failures(sdk, error_type):
    _, client = sdk
    failure = error_type(request=httpx2.Request("POST", "https://example.test"))
    client.responses.parse.side_effect = failure
    with pytest.raises(PriorityIntegrationError) as error:
        OpenAIPriorityClient("fake-test-key").suggest("Tarefa")
    assert error.value.__cause__ is failure


def test_sdk_response_validation_error_is_expected(sdk):
    _, client = sdk
    failure = APIResponseValidationError(
        response=httpx2.Response(200, request=httpx2.Request("POST", "https://example.test")),
        body={},
    )
    client.responses.parse.side_effect = failure
    with pytest.raises(PriorityIntegrationError) as error:
        OpenAIPriorityClient("fake-test-key").suggest("Tarefa")
    assert error.value.__cause__ is failure


def test_parse_validation_failure_is_expected(sdk):
    _, client = sdk

    def invalid_output(**kwargs):
        return kwargs["text_format"].model_validate({"prioridade": "invalida"})

    client.responses.parse.side_effect = invalid_output
    with pytest.raises(PriorityIntegrationError):
        OpenAIPriorityClient("fake-test-key").suggest("Tarefa")


def test_unexpected_bug_is_not_hidden(sdk):
    _, client = sdk
    failure = RuntimeError("Defeito simulado")
    client.responses.parse.side_effect = failure
    with pytest.raises(RuntimeError) as error:
        OpenAIPriorityClient("fake-test-key").suggest("Tarefa")
    assert error.value is failure


def test_configuration_defaults_and_no_configuration(monkeypatch, sdk):
    factory, _ = sdk
    assert OpenAIPriorityClient.from_env() is None
    monkeypatch.setenv("OPENAI_API_KEY", "fake-test-key")
    adapter = OpenAIPriorityClient.from_env()
    assert adapter.model == "gpt-5-nano" and adapter.timeout == 10.0
    factory.assert_not_called()


def test_custom_model_and_timeout(monkeypatch):
    monkeypatch.setenv("OPENAI_API_KEY", "fake-test-key")
    monkeypatch.setenv("OPENAI_MODEL", "modelo-configurado")
    monkeypatch.setenv("OPENAI_TIMEOUT_SECONDS", "2.5")
    adapter = OpenAIPriorityClient.from_env()
    assert adapter.model == "modelo-configurado" and adapter.timeout == 2.5


@pytest.mark.parametrize("value", ["texto", "0", "-1", "nan", "inf", ""])
def test_invalid_timeout_is_configuration_error(monkeypatch, value):
    monkeypatch.setenv("OPENAI_TIMEOUT_SECONDS", value)
    with pytest.raises(ValueError):
        OpenAIPriorityClient.from_env()


@pytest.mark.parametrize("name", ["OPENAI_API_KEY", "OPENAI_MODEL"])
def test_blank_configuration_disables_ai(monkeypatch, name):
    monkeypatch.setenv("OPENAI_API_KEY", "fake-test-key")
    monkeypatch.setenv(name, "   ")
    assert OpenAIPriorityClient.from_env() is None


@pytest.mark.parametrize("timeout", [0.0, -1.0, float("nan"), float("inf")])
def test_constructor_rejects_invalid_timeout(timeout):
    with pytest.raises(ValueError):
        OpenAIPriorityClient("fake-test-key", timeout=timeout)


@pytest.mark.parametrize("output", ['{"prioridade":"alta"}', '{"prioridade":"urgente"}', 'texto inválido'])
def test_real_sdk_parsing_with_simulated_http_transport(monkeypatch, output):
    original_sdk = integration.OpenAI
    requests = []

    def respond(request):
        assert str(request.url) == "https://api.openai.com/v1/responses"
        body = json.loads(request.content)
        requests.append(body)
        assert body["text"]["format"]["type"] == "json_schema"
        assert body["text"]["format"]["strict"] is True
        return httpx2.Response(200, json={
            "id": "resp_test", "object": "response", "created_at": 0,
            "status": "completed", "model": "gpt-5-nano", "error": None,
            "incomplete_details": None, "parallel_tool_calls": False,
            "tools": [], "tool_choice": "auto",
            "output": [{
                "id": "msg_test", "type": "message", "role": "assistant",
                "status": "completed", "content": [{
                    "type": "output_text", "text": output, "annotations": []
                }],
            }],
        })

    def mocked_sdk(**kwargs):
        return original_sdk(
            http_client=httpx2.Client(transport=httpx2.MockTransport(respond)), **kwargs
        )

    monkeypatch.setattr(integration, "OpenAI", mocked_sdk)
    adapter = OpenAIPriorityClient("fake-test-key")
    if output == '{"prioridade":"alta"}':
        assert adapter.suggest("Tarefa") is TaskPriority.ALTA
    else:
        with pytest.raises(PriorityIntegrationError):
            adapter.suggest("Tarefa")
    assert len(requests) == 1
