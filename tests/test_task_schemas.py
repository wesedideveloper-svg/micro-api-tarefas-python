import json
from types import SimpleNamespace

import pytest
from pydantic import ValidationError

from app.enums import TaskPriority, TaskStatus
from app.schemas import TaskCreate, TaskResponse, TaskUpdate


def test_create_defaults():
    task = TaskCreate(titulo="  Estudar Python  ")
    assert task.titulo == "Estudar Python"
    assert task.descricao is None
    assert task.prioridade is TaskPriority.MEDIA
    assert "status" not in task.model_dump()


@pytest.mark.parametrize("schema", [TaskCreate, TaskUpdate, TaskResponse])
@pytest.mark.parametrize("length", [3, 150])
def test_title_boundaries_after_trim(schema, length):
    payload = {"titulo": "  " + "a" * length + "  "}
    if schema is TaskResponse:
        payload.update(id=1, descricao=None, status="pendente", prioridade="media")
    assert schema(**payload).titulo == "a" * length


@pytest.mark.parametrize("schema", [TaskCreate, TaskUpdate])
@pytest.mark.parametrize(
    "title",
    ["", "   ", "ab", " a ", "  ab  ", "a" * 151,
     "  " + "a" * 151 + "  ", 123, [], None],
)
def test_invalid_title(schema, title):
    with pytest.raises(ValidationError):
        schema(titulo=title)


def test_create_requires_title():
    with pytest.raises(ValidationError):
        TaskCreate()


@pytest.mark.parametrize("schema", [TaskCreate, TaskUpdate, TaskResponse])
@pytest.mark.parametrize(
    ("description", "expected"),
    [(None, None), ("", None), (" \t\n ", None), ("  Texto  ", "Texto"),
     ("  " + "a" * 2000 + "  ", "a" * 2000)],
)
def test_description_normalization_and_limit(schema, description, expected):
    payload = {"titulo": "Tarefa", "descricao": description}
    if schema is TaskResponse:
        payload.update(id=1, status="pendente", prioridade="media")
    task = schema(**payload)
    assert task.descricao == expected


@pytest.mark.parametrize("schema", [TaskCreate, TaskUpdate])
@pytest.mark.parametrize("description", ["a" * 2001, 123, []])
def test_invalid_description(schema, description):
    with pytest.raises(ValidationError):
        schema(titulo="Tarefa", descricao=description)


@pytest.mark.parametrize("schema", [TaskCreate, TaskUpdate])
@pytest.mark.parametrize("priority", list(TaskPriority))
def test_valid_priorities(schema, priority):
    assert schema(titulo="Tarefa", prioridade=priority.value).prioridade is priority


@pytest.mark.parametrize("schema", [TaskCreate, TaskUpdate])
@pytest.mark.parametrize("priority", ["Alta", "urgente", "", 1, None])
def test_invalid_priority(schema, priority):
    with pytest.raises(ValidationError):
        schema(titulo="Tarefa", prioridade=priority)


@pytest.mark.parametrize("status", list(TaskStatus))
def test_update_valid_status(status):
    assert TaskUpdate(status=status.value).status is status


@pytest.mark.parametrize("status", ["Pendente", "em_andamento", "", 1, None])
def test_update_invalid_status(status):
    with pytest.raises(ValidationError):
        TaskUpdate(status=status)


@pytest.mark.parametrize("field", ["id", "status", "desconhecido"])
def test_create_forbids_extra_fields(field):
    with pytest.raises(ValidationError):
        TaskCreate.model_validate({"titulo": "Tarefa", field: "pendente"})


@pytest.mark.parametrize("field", ["id", "desconhecido"])
def test_update_forbids_extra_fields(field):
    with pytest.raises(ValidationError):
        TaskUpdate.model_validate({"titulo": "Tarefa", field: 1})


def test_update_rejects_empty_payload():
    with pytest.raises(ValidationError):
        TaskUpdate()


@pytest.mark.parametrize(
    "payload",
    [{"titulo": "Novo título"}, {"descricao": "Texto"},
     {"status": "concluida"}, {"prioridade": "alta"}],
)
def test_partial_update_includes_only_supplied_fields(payload):
    task = TaskUpdate(**payload)
    assert task.model_fields_set == set(payload)
    assert task.model_dump(exclude_unset=True) == payload
    assert task.model_dump(mode="json", exclude_unset=True) == payload


def test_update_distinguishes_omitted_description_from_null():
    omitted = TaskUpdate(titulo="Novo título")
    cleared = TaskUpdate(descricao=None)
    assert "descricao" not in omitted.model_dump(exclude_unset=True)
    assert cleared.model_dump(exclude_unset=True) == {"descricao": None}


def test_update_blank_description_clears_value():
    assert TaskUpdate(descricao="   ").model_dump(exclude_unset=True) == {
        "descricao": None
    }


def test_update_dump_preserves_normalized_and_explicit_default_values():
    task = TaskUpdate(
        titulo="  Novo título  ",
        descricao="  Texto  ",
        status="pendente",
        prioridade="media",
    )
    assert task.model_dump(exclude_unset=True) == {
        "titulo": "Novo título",
        "descricao": "Texto",
        "status": TaskStatus.PENDENTE,
        "prioridade": TaskPriority.MEDIA,
    }


def response_payload():
    return {
        "id": 1, "titulo": "Tarefa", "descricao": None,
        "status": "pendente", "prioridade": "media",
    }


def test_response_from_attributes_and_json_serialization():
    payload = response_payload()
    task = TaskResponse.model_validate(SimpleNamespace(**payload))
    assert task.status is TaskStatus.PENDENTE
    assert task.prioridade is TaskPriority.MEDIA
    assert task.model_dump(mode="json") == payload
    assert json.loads(task.model_dump_json()) == payload


@pytest.mark.parametrize("task_id", [0, -1, True, 1.5, "1", None])
def test_response_requires_positive_integer_id(task_id):
    payload = response_payload()
    payload["id"] = task_id
    with pytest.raises(ValidationError):
        TaskResponse(**payload)


@pytest.mark.parametrize("field", ["id", "titulo", "descricao", "status", "prioridade"])
def test_response_requires_all_fields(field):
    payload = response_payload()
    del payload[field]
    with pytest.raises(ValidationError):
        TaskResponse(**payload)


@pytest.mark.parametrize(
    ("field", "value"),
    [("titulo", "ab"), ("descricao", "a" * 2001),
     ("status", "invalido"), ("prioridade", "invalida"),
     ("desconhecido", "valor")],
)
def test_response_rejects_invalid_values_and_extra_fields(field, value):
    payload = response_payload()
    payload[field] = value
    with pytest.raises(ValidationError):
        TaskResponse(**payload)


def test_update_multiple_fields_json_serialization():
    payload = {
        "titulo": "Tarefa atualizada", "descricao": None,
        "status": "concluida", "prioridade": "alta",
    }
    assert json.loads(TaskUpdate(**payload).model_dump_json(exclude_unset=True)) == payload


def test_create_json_serialization():
    task = TaskCreate(titulo="Tarefa", descricao="Texto", prioridade="alta")
    assert json.loads(task.model_dump_json()) == {
        "titulo": "Tarefa", "descricao": "Texto", "prioridade": "alta"
    }
