"""Sugestão local por palavras inteiras, sem análise semântica ou acesso externo."""

import re

from app.enums import TaskPriority


# A ordem define a precedência: alta > media > baixa.
PRIORITY_KEYWORDS = (
    (TaskPriority.ALTA, frozenset({"urgente", "emergência", "emergencia", "crítico", "critico"})),
    (TaskPriority.MEDIA, frozenset({"importante", "prazo", "revisar"})),
    (TaskPriority.BAIXA, frozenset({"opcional", "rotina", "depois"})),
)


def suggest_priority(titulo: str, descricao: str | None = None) -> TaskPriority:
    """Compara título e descrição sem distinguir maiúsculas; padrão: media.

    As palavras-chave estão em PRIORITY_KEYWORDS. Texto vazio ou descrição
    ausente não produz correspondência. A primeira prioridade encontrada vence.
    """
    words = set(re.findall(r"\b\w+\b", f"{titulo} {descricao or ''}".casefold()))
    for priority, keywords in PRIORITY_KEYWORDS:
        if words & keywords:
            return priority
    return TaskPriority.MEDIA
