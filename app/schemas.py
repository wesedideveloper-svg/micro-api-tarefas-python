"""Contratos de criação, atualização e resposta das tarefas."""

from typing import Annotated

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from app.enums import TaskPriority, TaskStatus


def trim_title(value: object) -> object:
    return value.strip() if isinstance(value, str) else value


def normalize_description(value: object) -> object:
    if isinstance(value, str):
        return value.strip() or None
    return value


TaskTitle = Annotated[
    str, Field(min_length=3, max_length=150), BeforeValidator(trim_title)
]
TaskDescription = Annotated[
    str | None, Field(max_length=2000), BeforeValidator(normalize_description)
]


class TaskCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: TaskTitle
    descricao: TaskDescription = None
    prioridade: TaskPriority = TaskPriority.MEDIA


class TaskUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: TaskTitle | None = None
    descricao: TaskDescription = None
    status: TaskStatus | None = None
    prioridade: TaskPriority | None = None

    @field_validator("titulo", "status", "prioridade", mode="before")
    @classmethod
    def reject_explicit_null(cls, value: object) -> object:
        if value is None:
            raise ValueError("O campo não pode receber null.")
        return value

    @model_validator(mode="after")
    def require_update_fields(self) -> "TaskUpdate":
        if not self.model_fields_set:
            raise ValueError("Informe ao menos um campo para atualização.")
        return self


class TaskResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: Annotated[int, Field(gt=0, strict=True)]
    titulo: TaskTitle
    descricao: TaskDescription
    status: TaskStatus
    prioridade: TaskPriority
