"""Operações de tarefas e controle de transações, sem dependência de HTTP."""

from sqlalchemy.orm import Session

from app.enums import TaskStatus
from app.models import Task
from app.repositories.task_repository import TaskRepository
from app.schemas import TaskCreate, TaskUpdate


class TaskNotFoundError(Exception):
    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Tarefa {task_id} não encontrada.")


class TaskService:
    def __init__(self, session: Session) -> None:
        self.session = session
        self.repository = TaskRepository(session)

    def create(self, data: TaskCreate) -> Task:
        try:
            task = self.repository.create(data)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        self.session.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Task:
        task = self.repository.get_by_id(task_id)
        if task is None:
            raise TaskNotFoundError(task_id)
        return task

    def list_all(self, status: TaskStatus | None = None) -> list[Task]:
        return self.repository.list_all(status)

    def complete(self, task_id: int) -> Task:
        return self.update(task_id, TaskUpdate(status=TaskStatus.CONCLUIDA))

    def update(self, task_id: int, data: TaskUpdate) -> Task:
        try:
            task = self.repository.update(task_id, data)
            if task is None:
                raise TaskNotFoundError(task_id)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
        self.session.refresh(task)
        return task

    def delete(self, task_id: int) -> None:
        try:
            if not self.repository.delete(task_id):
                raise TaskNotFoundError(task_id)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
