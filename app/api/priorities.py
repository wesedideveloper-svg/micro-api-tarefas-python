"""Sugestão de prioridade sem criação ou alteração de tarefas."""

from fastapi import APIRouter

from app.priority_schemas import PrioritySuggestionRequest, PrioritySuggestionResponse
from app.services.priority_suggestion_service import PrioritySuggestion, PrioritySuggestionService


router = APIRouter(prefix="/tarefas", tags=["Sugestão de prioridade"])


@router.post(
    "/sugerir-prioridade",
    response_model=PrioritySuggestionResponse,
    status_code=200,
    summary="Sugerir prioridade de tarefa",
    description="Sugere uma prioridade usando IA ou fallback local, sem salvar a tarefa.",
)
def suggest_task_priority(data: PrioritySuggestionRequest) -> PrioritySuggestion:
    service = PrioritySuggestionService.from_env()
    return service.suggest(data.titulo, data.descricao)
