from enum import Enum

import pytest

from app.enums import TaskPriority, TaskStatus


@pytest.mark.parametrize(
    ("enum_type", "expected_values"),
    [
        (TaskStatus, {"pendente", "concluida"}),
        (TaskPriority, {"baixa", "media", "alta"}),
    ],
)
def test_enum_values(enum_type, expected_values):
    assert issubclass(enum_type, str)
    assert issubclass(enum_type, Enum)
    assert {member.value for member in enum_type} == expected_values


@pytest.mark.parametrize(
    ("member", "value"),
    [
        (TaskStatus.PENDENTE, "pendente"),
        (TaskStatus.CONCLUIDA, "concluida"),
        (TaskPriority.BAIXA, "baixa"),
        (TaskPriority.MEDIA, "media"),
        (TaskPriority.ALTA, "alta"),
    ],
)
def test_enum_member_matches_value(member, value):
    assert member.value == value
    assert member == value
    assert type(member)(value) is member


@pytest.mark.parametrize("enum_type", [TaskStatus, TaskPriority])
def test_enum_rejects_invalid_value(enum_type):
    with pytest.raises(ValueError):
        enum_type("invalido")
