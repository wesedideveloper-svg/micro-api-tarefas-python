"""Contratos HTTP específicos para sugestão de prioridade."""

from typing import Literal

from pydantic import BaseModel, ConfigDict

from app.enums import TaskPriority
from app.schemas import TaskDescription, TaskTitle


class PrioritySuggestionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    titulo: TaskTitle
    descricao: TaskDescription = None


class PrioritySuggestionResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    prioridade: TaskPriority
    origem: Literal["ia", "local"]
