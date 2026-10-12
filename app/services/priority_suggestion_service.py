"""Coordenação da sugestão por IA e do fallback local, sem persistência."""

from dataclasses import dataclass
from typing import Literal

from app.enums import TaskPriority
from app.integrations.openai_priority_client import OpenAIPriorityClient, PriorityIntegrationError
from app.services.priority_service import suggest_priority


@dataclass(frozen=True)
class PrioritySuggestion:
    prioridade: TaskPriority
    origem: Literal["ia", "local"]


class PrioritySuggestionService:
    def __init__(self, client: OpenAIPriorityClient | None = None) -> None:
        self.client = client

    @classmethod
    def from_env(cls) -> "PrioritySuggestionService":
        return cls(OpenAIPriorityClient.from_env())

    def suggest(self, titulo: str, descricao: str | None = None) -> PrioritySuggestion:
        if self.client is not None:
            try:
                priority = self.client.suggest(titulo, descricao)
                return PrioritySuggestion(prioridade=priority, origem="ia")
            except PriorityIntegrationError:
                pass
        return PrioritySuggestion(
            prioridade=suggest_priority(titulo, descricao), origem="local"
        )
