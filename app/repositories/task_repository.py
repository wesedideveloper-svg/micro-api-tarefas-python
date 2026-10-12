"""Persistência de tarefas sem controle da transação ou da sessão."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: TaskCreate) -> Task:
        task = Task(**data.model_dump())
        self.session.add(task)
        self.session.flush()
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        return self.session.get(Task, task_id)

    def list_all(self) -> list[Task]:
        return list(self.session.scalars(select(Task).order_by(Task.id)))

    def update(self, task_id: int, data: TaskUpdate) -> Task | None:
        """Atualiza apenas campos enviados; retorna None se o ID não existir."""
        task = self.get_by_id(task_id)
        if task is None:
            return None
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(task, field, value)
        self.session.flush()
        return task

    def delete(self, task_id: int) -> bool:
        """Retorna True ao excluir; False se o ID não existir."""
        task = self.get_by_id(task_id)
        if task is None:
            return False
        self.session.delete(task)
        self.session.flush()
        return True
