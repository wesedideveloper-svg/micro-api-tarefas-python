from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.enums import TaskPriority, TaskStatus
from app.models import Task
from app.repositories.task_repository import TaskRepository
from app.schemas import TaskCreate, TaskUpdate


@pytest.fixture
def database_factory(tmp_path):
    engines = []

    def create_database():
        engine = create_engine(f"sqlite:///{tmp_path / f'repository_{len(engines)}.db'}")
        engines.append(engine)
        Base.metadata.create_all(engine)
        return sessionmaker(bind=engine, autoflush=False)

    yield create_database
    for engine in engines:
        engine.dispose()


@pytest.fixture
def repository(database_factory):
    with database_factory()() as session:
        yield TaskRepository(session)


def test_create_returns_task_with_id_and_defaults(repository):
    task = repository.create(TaskCreate(titulo="Estudar Python"))
    assert isinstance(task, Task)
    assert task.id > 0
    assert task.titulo == "Estudar Python"
    assert task.descricao is None
    assert task.status is TaskStatus.PENDENTE
    assert task.prioridade is TaskPriority.MEDIA


def test_create_preserves_validated_data(repository):
    task = repository.create(
        TaskCreate(titulo="Tarefa", descricao="Descrição", prioridade="alta")
    )
    assert task.descricao == "Descrição"
    assert task.prioridade is TaskPriority.ALTA


def test_get_by_id_existing_and_missing(repository):
    task = repository.create(TaskCreate(titulo="Tarefa"))
    assert repository.get_by_id(task.id) is task
    assert repository.get_by_id(task.id + 1) is None


def test_list_empty(repository):
    assert repository.list_all() == []


def test_list_orders_by_id(repository):
    repository.session.add_all([
        Task(id=30, titulo="Terceira"),
        Task(id=10, titulo="Primeira"),
        Task(id=20, titulo="Segunda"),
    ])
    repository.session.flush()
    assert [task.id for task in repository.list_all()] == [10, 20, 30]


@pytest.mark.parametrize("status", list(TaskStatus))
def test_list_filters_by_status_in_id_order(repository, status):
    repository.session.add_all([
        Task(id=30, titulo="Terceira", status=status),
        Task(id=10, titulo="Primeira", status=status),
        Task(id=20, titulo="Outra", status=(
            TaskStatus.CONCLUIDA if status is TaskStatus.PENDENTE else TaskStatus.PENDENTE
        )),
    ])
    repository.session.flush()
    assert [task.id for task in repository.list_all(status)] == [10, 30]


@pytest.mark.parametrize(
    ("changes", "expected"),
    [
        ({"titulo": "Novo título"}, {"titulo": "Novo título"}),
        ({"descricao": "Nova descrição"}, {"descricao": "Nova descrição"}),
        ({"status": "concluida"}, {"status": TaskStatus.CONCLUIDA}),
        ({"prioridade": "alta"}, {"prioridade": TaskPriority.ALTA}),
        ({"descricao": None}, {"descricao": None}),
    ],
)
def test_update_changes_only_supplied_fields(repository, changes, expected):
    task = repository.create(TaskCreate(titulo="Original", descricao="Descrição"))
    original = {
        "titulo": task.titulo, "descricao": task.descricao,
        "status": task.status, "prioridade": task.prioridade,
    }
    updated = repository.update(task.id, TaskUpdate(**changes))
    assert updated is task
    repository.session.expire_all()
    recovered = repository.get_by_id(task.id)
    for field, value in (original | expected).items():
        assert getattr(recovered, field) == value


def test_update_missing_task(repository):
    assert repository.update(999, TaskUpdate(titulo="Novo título")) is None
    assert repository.list_all() == []


def test_delete_existing_and_missing_task(repository):
    task = repository.create(TaskCreate(titulo="Tarefa"))
    task_id = task.id
    assert repository.delete(task_id) is True
    assert repository.get_by_id(task_id) is None
    assert repository.list_all() == []
    assert repository.delete(task_id) is False


@pytest.mark.parametrize("operation", ["create", "update", "delete"])
@pytest.mark.parametrize("commit", [False, True])
def test_transaction_is_controlled_by_caller(database_factory, operation, commit):
    sessions = database_factory()
    with sessions() as setup:
        task = TaskRepository(setup).create(
            TaskCreate(titulo="Original", descricao="Descrição")
        )
        task_id = task.id
        setup.commit()

    with sessions() as session:
        repository = TaskRepository(session)
        if operation == "create":
            repository.create(TaskCreate(titulo="Nova tarefa"))
        elif operation == "update":
            repository.update(task_id, TaskUpdate(titulo="Atualizada", descricao=None))
        else:
            repository.delete(task_id)
        if commit:
            session.commit()

    with sessions() as verification:
        tasks = TaskRepository(verification).list_all()
        if not commit:
            assert [(task.titulo, task.descricao) for task in tasks] == [
                ("Original", "Descrição")
            ]
        elif operation == "create":
            assert [task.titulo for task in tasks] == ["Original", "Nova tarefa"]
        elif operation == "update":
            assert [(task.titulo, task.descricao) for task in tasks] == [
                ("Atualizada", None)
            ]
        else:
            assert tasks == []


def test_repository_does_not_manage_received_session(repository, monkeypatch):
    with monkeypatch.context() as patch:
        guards = []
        for method in ("commit", "rollback", "close"):
            guard = Mock(side_effect=AssertionError(f"Repository chamou {method}"))
            guards.append(guard)
            patch.setattr(repository.session, method, guard)
        task = repository.create(TaskCreate(titulo="Tarefa"))
        assert repository.get_by_id(task.id) is task
        assert repository.list_all() == [task]
        repository.update(task.id, TaskUpdate(titulo="Atualizada"))
        assert repository.delete(task.id) is True
        for guard in guards:
            guard.assert_not_called()


def test_repositories_use_independent_temporary_databases(database_factory):
    first_sessions, second_sessions = database_factory(), database_factory()
    with first_sessions() as first, second_sessions() as second:
        assert first.bind.url.database != second.bind.url.database
        first_repository, second_repository = TaskRepository(first), TaskRepository(second)
        first_repository.create(TaskCreate(titulo="Primeiro banco"))
        first.commit()
        assert second_repository.list_all() == []
        second_repository.create(TaskCreate(titulo="Segundo banco"))
        second.commit()
        assert [task.titulo for task in first_repository.list_all()] == ["Primeiro banco"]
        assert [task.titulo for task in second_repository.list_all()] == ["Segundo banco"]
