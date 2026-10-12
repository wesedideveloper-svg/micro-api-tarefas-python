"""Endpoints CRUD de tarefas, delegando as operações ao Service."""

from typing import Annotated

from fastapi import APIRouter, Depends, Path, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService


router = APIRouter(prefix="/tarefas", tags=["Tarefas"])
DatabaseSession = Annotated[Session, Depends(get_db)]
TaskId = Annotated[int, Path(gt=0)]
NOT_FOUND = {404: {"description": "Tarefa não encontrada"}}


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED,
             summary="Criar tarefa")
def create_task(data: TaskCreate, session: DatabaseSession) -> Task:
    return TaskService(session).create(data)


@router.get("", response_model=list[TaskResponse], summary="Listar tarefas")
def list_tasks(session: DatabaseSession) -> list[Task]:
    return TaskService(session).list_all()


@router.get("/{task_id}", response_model=TaskResponse, responses=NOT_FOUND,
            summary="Consultar tarefa")
def get_task(task_id: TaskId, session: DatabaseSession) -> Task:
    return TaskService(session).get_by_id(task_id)


@router.patch("/{task_id}", response_model=TaskResponse, responses=NOT_FOUND,
              summary="Atualizar tarefa parcialmente")
def update_task(task_id: TaskId, data: TaskUpdate, session: DatabaseSession) -> Task:
    return TaskService(session).update(task_id, data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT,
               response_class=Response, responses=NOT_FOUND, summary="Excluir tarefa")
def delete_task(task_id: TaskId, session: DatabaseSession) -> Response:
    TaskService(session).delete(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
