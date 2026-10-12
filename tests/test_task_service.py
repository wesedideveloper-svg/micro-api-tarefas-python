from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.enums import TaskPriority, TaskStatus
from app.schemas import TaskCreate, TaskUpdate
from app.services.task_service import TaskNotFoundError, TaskService


@pytest.fixture
def sessions(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'service.db'}")
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine, autoflush=False)
    engine.dispose()


@pytest.fixture
def service(sessions):
    with sessions() as session:
        yield TaskService(session)


def test_create_commits_and_returns_refreshed_task(service, sessions):
    task = service.create(TaskCreate(titulo="Tarefa", descricao="Descrição"))
    assert task.id > 0
    assert task.status is TaskStatus.PENDENTE
    assert task.prioridade is TaskPriority.MEDIA
    with sessions() as verification:
        persisted = TaskService(verification).get_by_id(task.id)
        assert (persisted.titulo, persisted.descricao) == (task.titulo, task.descricao)


def test_get_existing_task(service):
    task = service.create(TaskCreate(titulo="Tarefa"))
    assert service.get_by_id(task.id) is task


@pytest.mark.parametrize("operation", ["get_by_id", "update", "delete"])
def test_missing_task_raises_application_exception(service, monkeypatch, operation):
    with monkeypatch.context() as patch:
        commit = Mock(side_effect=AssertionError("Commit para tarefa inexistente"))
        rollback = Mock(wraps=service.session.rollback)
        patch.setattr(service.session, "commit", commit)
        patch.setattr(service.session, "rollback", rollback)
        with pytest.raises(TaskNotFoundError) as error:
            if operation == "update":
                service.update(999, TaskUpdate(titulo="Atualizada"))
            else:
                getattr(service, operation)(999)
        assert error.value.task_id == 999
        commit.assert_not_called()
        assert rollback.call_count == (0 if operation == "get_by_id" else 1)


def test_list_empty(service):
    assert service.list_all() == []


def test_reads_do_not_commit_and_list_is_ordered(service, monkeypatch):
    tasks = [service.create(TaskCreate(titulo=title)) for title in ("Primeira", "Segunda")]
    with monkeypatch.context() as patch:
        commit = Mock(side_effect=AssertionError("Commit em leitura"))
        patch.setattr(service.session, "commit", commit)
        assert service.get_by_id(tasks[0].id) is tasks[0]
        assert [task.id for task in service.list_all()] == sorted(task.id for task in tasks)
        commit.assert_not_called()


@pytest.mark.parametrize("description", ["Nova descrição", None])
def test_partial_update_commits_and_preserves_omitted_fields(service, sessions, description):
    task = service.create(TaskCreate(titulo="Original", descricao="Descrição"))
    updated = service.update(task.id, TaskUpdate(descricao=description))
    assert updated is task
    assert updated.titulo == "Original"
    assert updated.descricao == description
    with sessions() as verification:
        persisted = TaskService(verification).get_by_id(task.id)
        assert persisted.titulo == "Original"
        assert persisted.descricao == description


def test_delete_commits(service, sessions):
    task_id = service.create(TaskCreate(titulo="Tarefa")).id
    assert service.delete(task_id) is None
    with sessions() as verification:
        with pytest.raises(TaskNotFoundError):
            TaskService(verification).get_by_id(task_id)


@pytest.mark.parametrize("operation", ["create", "update", "delete"])
@pytest.mark.parametrize("failure_point", ["repository", "commit"])
def test_write_failure_rolls_back_and_propagates_original_exception(
    service, sessions, monkeypatch, operation, failure_point
):
    task_id = service.create(TaskCreate(titulo="Original", descricao="Descrição")).id
    original_operation = getattr(service.repository, operation)
    failure = RuntimeError("Falha simulada")

    def fail_after_flush(*args):
        original_operation(*args)
        raise failure

    with monkeypatch.context() as patch:
        rollback = Mock(wraps=service.session.rollback)
        commit = Mock(wraps=service.session.commit)
        patch.setattr(service.session, "rollback", rollback)
        if failure_point == "repository":
            patch.setattr(service.repository, operation, fail_after_flush)
        else:
            commit.side_effect = failure
        patch.setattr(service.session, "commit", commit)
        with pytest.raises(RuntimeError) as error:
            if operation == "create":
                service.create(TaskCreate(titulo="Não confirmada"))
            elif operation == "update":
                service.update(task_id, TaskUpdate(titulo="Alterada", descricao=None))
            else:
                service.delete(task_id)
        assert error.value is failure
        rollback.assert_called_once_with()
        assert commit.call_count == (0 if failure_point == "repository" else 1)

    with sessions() as verification:
        tasks = TaskService(verification).list_all()
        assert [(task.id, task.titulo, task.descricao) for task in tasks] == [
            (task_id, "Original", "Descrição")
        ]
    assert service.get_by_id(task_id).titulo == "Original"


@pytest.mark.parametrize("operation", ["create", "update"])
def test_create_and_update_refresh_after_commit(service, monkeypatch, operation):
    task = service.create(TaskCreate(titulo="Original"))
    calls = []
    original_commit, original_refresh = service.session.commit, service.session.refresh

    def commit():
        original_commit()
        calls.append("commit")

    def refresh(task):
        calls.append("refresh")
        original_refresh(task)

    with monkeypatch.context() as patch:
        patch.setattr(service.session, "commit", commit)
        patch.setattr(service.session, "refresh", refresh)
        if operation == "create":
            returned = service.create(TaskCreate(titulo="Criada"))
        else:
            returned = service.update(task.id, TaskUpdate(titulo="Atualizada"))
        assert calls == ["commit", "refresh"]
        assert returned.titulo == ("Criada" if operation == "create" else "Atualizada")


@pytest.mark.parametrize("operation", ["create", "update"])
def test_refresh_failure_propagates_without_undoing_commit(
    service, sessions, monkeypatch, operation
):
    if operation == "update":
        task_id = service.create(TaskCreate(titulo="Original", descricao="Descrição")).id
    failure = RuntimeError("Falha no refresh")
    with monkeypatch.context() as patch:
        refresh = Mock(side_effect=failure)
        rollback = Mock(wraps=service.session.rollback)
        commit = Mock(wraps=service.session.commit)
        patch.setattr(service.session, "refresh", refresh)
        patch.setattr(service.session, "rollback", rollback)
        patch.setattr(service.session, "commit", commit)
        with pytest.raises(RuntimeError) as error:
            if operation == "create":
                service.create(TaskCreate(titulo="Confirmada", descricao="Descrição"))
            else:
                service.update(task_id, TaskUpdate(titulo="Confirmada", descricao=None))
        assert error.value is failure
        commit.assert_called_once_with()
        refresh.assert_called_once()
        rollback.assert_not_called()
    with sessions() as verification:
        tasks = TaskService(verification).list_all()
        assert len(tasks) == 1
        assert tasks[0].titulo == "Confirmada"
        assert tasks[0].descricao == ("Descrição" if operation == "create" else None)
        if operation == "update":
            assert tasks[0].id == task_id


def test_service_does_not_close_received_session(service, monkeypatch):
    with monkeypatch.context() as patch:
        close = Mock(side_effect=AssertionError("Service fechou a sessão"))
        patch.setattr(service.session, "close", close)
        task = service.create(TaskCreate(titulo="Tarefa"))
        service.get_by_id(task.id)
        service.list_all()
        service.update(task.id, TaskUpdate(titulo="Atualizada"))
        service.delete(task.id)
        close.assert_not_called()


def test_service_uses_isolated_temporary_database(service, sessions, tmp_path):
    assert service.session.bind.url.database == str(tmp_path / "service.db")
    assert service.list_all() == []
    service.create(TaskCreate(titulo="Tarefa deste teste"))
    second_engine = create_engine(f"sqlite:///{tmp_path / 'independent.db'}")
    try:
        Base.metadata.create_all(second_engine)
        with sessionmaker(bind=second_engine)() as other:
            assert TaskService(other).list_all() == []
        with sessions() as verification:
            assert len(TaskService(verification).list_all()) == 1
    finally:
        second_engine.dispose()
