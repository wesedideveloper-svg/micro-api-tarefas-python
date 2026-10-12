import pytest

from app.enums import TaskPriority
from app.services.priority_service import suggest_priority


@pytest.mark.parametrize(
    ("title", "expected"),
    [
        ("Correção urgente", TaskPriority.ALTA),
        ("Atender emergência", TaskPriority.ALTA),
        ("Atender emergencia", TaskPriority.ALTA),
        ("Incidente crítico", TaskPriority.ALTA),
        ("Incidente critico", TaskPriority.ALTA),
        ("Entrega importante", TaskPriority.MEDIA),
        ("Verificar prazo", TaskPriority.MEDIA),
        ("Revisar documentação", TaskPriority.MEDIA),
        ("Leitura opcional", TaskPriority.BAIXA),
        ("Organizar rotina", TaskPriority.BAIXA),
        ("Fazer depois", TaskPriority.BAIXA),
    ],
)
def test_classifies_documented_keywords(title, expected):
    assert suggest_priority(title) is expected


@pytest.mark.parametrize(
    ("description", "expected"),
    [("Urgente!", TaskPriority.ALTA), ("IMPORTANTE", TaskPriority.MEDIA),
     ("Atividade OPCIONAL.", TaskPriority.BAIXA)],
)
def test_description_participates_in_case_insensitive_comparison(description, expected):
    assert suggest_priority("Tarefa", description) is expected


@pytest.mark.parametrize(
    ("title", "expected"),
    [("URGENTE!", TaskPriority.ALTA), ("PrAzO", TaskPriority.MEDIA),
     ("  ROTINA.  ", TaskPriority.BAIXA), ("EMERGÊNCIA", TaskPriority.ALTA)],
)
def test_title_is_case_insensitive_and_accepts_punctuation(title, expected):
    assert suggest_priority(title) is expected


@pytest.mark.parametrize(
    ("title", "description"),
    [("Tarefa comum", None), ("", None), ("", ""), (" \t\n ", "   "),
     ("Organizar documentos", "Arquivar notas")],
)
def test_no_match_and_empty_texts_default_to_medium(title, description):
    assert suggest_priority(title, description) is TaskPriority.MEDIA


@pytest.mark.parametrize(
    ("title", "description", "expected"),
    [
        ("Opcional", "Urgente", TaskPriority.ALTA),
        ("Urgente", "Opcional", TaskPriority.ALTA),
        ("Importante", "Crítico", TaskPriority.ALTA),
        ("Depois", "Importante", TaskPriority.MEDIA),
        ("Prazo", "Rotina", TaskPriority.MEDIA),
        ("Rotina importante urgente", None, TaskPriority.ALTA),
    ],
)
def test_priority_precedence_overrides_keyword_order(title, description, expected):
    assert suggest_priority(title, description) is expected


@pytest.mark.parametrize("title", ["urgentemente", "rotinas", "prazos"])
def test_keywords_must_match_whole_words(title):
    assert suggest_priority(title) is TaskPriority.MEDIA


def test_suggestion_is_deterministic_and_returns_enum():
    results = [suggest_priority("Opcional", "Urgente") for _ in range(3)]
    assert all(result is TaskPriority.ALTA for result in results)
