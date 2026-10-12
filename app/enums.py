"""Valores permitidos para status e prioridade das tarefas."""

from enum import Enum


class TaskStatus(str, Enum):
    PENDENTE = "pendente"
    CONCLUIDA = "concluida"


class TaskPriority(str, Enum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA = "alta"
