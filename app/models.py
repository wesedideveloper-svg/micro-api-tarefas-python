"""Modelo de persistência das tarefas."""

from sqlalchemy import CheckConstraint, Enum, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from app.enums import TaskPriority, TaskStatus


class Task(Base):
    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "length(trim(titulo)) BETWEEN 3 AND 150 AND length(titulo) <= 150",
            name="ck_tasks_titulo_length",
        ),
        CheckConstraint(
            "descricao IS NULL OR length(descricao) <= 2000",
            name="ck_tasks_descricao_length",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    titulo: Mapped[str] = mapped_column(String(150), nullable=False)
    descricao: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(
            TaskStatus,
            values_callable=lambda enum: [member.value for member in enum],
            native_enum=False,
            create_constraint=True,
            name="ck_tasks_status",
        ),
        nullable=False,
        default=TaskStatus.PENDENTE,
        server_default=TaskStatus.PENDENTE.value,
    )
    prioridade: Mapped[TaskPriority] = mapped_column(
        Enum(
            TaskPriority,
            values_callable=lambda enum: [member.value for member in enum],
            native_enum=False,
            create_constraint=True,
            name="ck_tasks_prioridade",
        ),
        nullable=False,
        default=TaskPriority.MEDIA,
        server_default=TaskPriority.MEDIA.value,
    )
