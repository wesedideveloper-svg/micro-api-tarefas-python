import os
import subprocess
import sys
from unittest.mock import Mock

import pytest
from sqlalchemy import create_engine, event, inspect, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from app import database
from app.database import Base
from app.enums import TaskPriority, TaskStatus
from app.models import Task


@pytest.fixture
def db_engine(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()


def test_table_structure(db_engine):
    inspector = inspect(db_engine)
    assert inspector.get_table_names() == ["tasks"]
    assert {column["name"] for column in inspector.get_columns("tasks")} == {
        "id", "titulo", "descricao", "status", "prioridade"
    }
    assert inspector.get_pk_constraint("tasks")["constrained_columns"] == ["id"]


def test_persist_and_retrieve_task(db_engine):
    sessions = sessionmaker(bind=db_engine)
    with sessions() as session:
        task = Task(
            titulo="Estudar Python", descricao="Revisar conceitos",
            status=TaskStatus.CONCLUIDA, prioridade=TaskPriority.ALTA,
        )
        session.add(task)
        session.commit()
        task_id = task.id
        assert isinstance(task_id, int) and task_id > 0
    with sessions() as session:
        recovered = session.get(Task, task_id)
        assert recovered.titulo == "Estudar Python"
        assert recovered.descricao == "Revisar conceitos"
        assert recovered.status is TaskStatus.CONCLUIDA
        assert recovered.prioridade is TaskPriority.ALTA


def test_orm_defaults_optional_description_and_generated_ids(db_engine):
    with sessionmaker(bind=db_engine)() as session:
        first, second = Task(titulo="Primeira"), Task(titulo="Segunda")
        session.add_all([first, second])
        session.commit()
        assert first.id > 0 and second.id > 0 and first.id != second.id
        assert first.descricao is None
        assert first.status is TaskStatus.PENDENTE
        assert first.prioridade is TaskPriority.MEDIA


def test_database_defaults_for_raw_insert(db_engine):
    with db_engine.begin() as connection:
        connection.execute(text("INSERT INTO tasks (titulo) VALUES ('Tarefa')"))
        row = connection.execute(
            text("SELECT descricao, status, prioridade FROM tasks")
        ).one()
        assert tuple(row) == (None, "pendente", "media")


@pytest.mark.parametrize("status", list(TaskStatus))
@pytest.mark.parametrize("priority", list(TaskPriority))
def test_enums_are_stored_as_text_values(db_engine, status, priority):
    with sessionmaker(bind=db_engine)() as session:
        session.add(Task(titulo="Tarefa", status=status, prioridade=priority))
        session.commit()
    with db_engine.connect() as connection:
        row = connection.execute(text("SELECT status, prioridade FROM tasks")).one()
        assert tuple(row) == (status.value, priority.value)


@pytest.mark.parametrize(
    ("column", "value"),
    [
        ("status", "invalido"), ("status", "PENDENTE"), ("status", None),
        ("prioridade", "urgente"), ("prioridade", "MEDIA"), ("prioridade", None),
        ("titulo", None), ("titulo", ""), ("titulo", "   "),
        ("titulo", "ab"), ("titulo", "  ab  "), ("titulo", "a" * 151),
        ("descricao", "a" * 2001),
    ],
)
def test_database_rejects_invalid_data(db_engine, column, value):
    # Os nomes das colunas vêm exclusivamente dos casos definidos neste teste.
    with pytest.raises(IntegrityError):
        with db_engine.begin() as connection:
            connection.execute(
                text(f"INSERT INTO tasks (titulo, {column}) VALUES (:title, :value)")
                if column != "titulo"
                else text("INSERT INTO tasks (titulo) VALUES (:value)"),
                {"title": "Tarefa", "value": value},
            )


@pytest.mark.parametrize("title", ["abc", "a" * 150])
@pytest.mark.parametrize("description", [None, "a" * 2000])
def test_database_accepts_length_boundaries(db_engine, title, description):
    with db_engine.begin() as connection:
        connection.execute(
            text("INSERT INTO tasks (titulo, descricao) VALUES (:title, :description)"),
            {"title": title, "description": description},
        )


@pytest.mark.parametrize(
    ("field", "value", "constraint"),
    [
        ("status", "invalido", "ck_tasks_status"),
        ("prioridade", "urgente", "ck_tasks_prioridade"),
    ],
)
def test_invalid_enum_via_orm_is_rejected_by_sqlite_check(
    db_engine, field, value, constraint
):
    with sessionmaker(bind=db_engine)() as session:
        task = Task(titulo="Tarefa", **{field: value})
        assert getattr(task, field) == value
        session.add(task)
        with pytest.raises(IntegrityError) as error:
            session.flush()
        assert "CHECK constraint failed" in str(error.value.orig)
        assert constraint in str(error.value.orig)
        session.rollback()
        assert session.scalar(select(Task)) is None


@pytest.mark.parametrize("raise_error", [False, True])
def test_get_db_closes_session_and_rolls_back_uncommitted_data(
    db_engine, monkeypatch, raise_error
):
    monkeypatch.setattr(database, "SessionLocal", sessionmaker(bind=db_engine))
    returned_connections = []
    event.listen(db_engine, "checkin", lambda *args: returned_connections.append(True))
    provider = database.get_db()
    session = next(provider)
    close_spy = Mock(wraps=session.close)
    monkeypatch.setattr(session, "close", close_spy)
    session.add(Task(titulo="Não confirmada"))
    session.flush()
    if raise_error:
        with pytest.raises(RuntimeError, match="Erro simulado"):
            provider.throw(RuntimeError("Erro simulado"))
    else:
        with pytest.raises(StopIteration):
            next(provider)
    close_spy.assert_called_once_with()
    assert not session.in_transaction()
    assert not session.identity_map
    assert returned_connections
    with sessionmaker(bind=db_engine)() as verification:
        assert verification.scalar(select(Task)) is None


def test_independent_temporary_databases(db_engine, tmp_path):
    assert db_engine.url.database == str(tmp_path / "test.db")
    second_engine = create_engine(f"sqlite:///{tmp_path / 'second.db'}")
    assert second_engine.url.database != db_engine.url.database
    try:
        Base.metadata.create_all(second_engine)
        with sessionmaker(bind=db_engine)() as first:
            first.add(Task(titulo="Primeiro banco"))
            first.commit()
        with sessionmaker(bind=second_engine)() as second:
            assert second.scalar(select(Task)) is None
            second.add(Task(titulo="Segundo banco"))
            second.commit()
        with sessionmaker(bind=db_engine)() as first:
            assert [task.titulo for task in first.scalars(select(Task))] == [
                "Primeiro banco"
            ]
        with sessionmaker(bind=second_engine)() as second:
            assert [task.titulo for task in second.scalars(select(Task))] == [
                "Segundo banco"
            ]
    finally:
        second_engine.dispose()


def test_import_does_not_connect_or_create_database(tmp_path):
    database_file = tmp_path / "not_created.db"
    environment = os.environ.copy()
    environment["DATABASE_URL"] = f"sqlite:///{database_file}"
    result = subprocess.run(
        [sys.executable, "-c",
         "import sqlite3; from unittest.mock import patch; "
         "guard = patch('sqlite3.dbapi2.connect', side_effect=AssertionError('connection')); "
         "guard.start(); "
         "tables_guard = patch('sqlalchemy.MetaData.create_all', "
         "side_effect=AssertionError('tables')); tables_guard.start(); "
         "import app.database; import app.models; "
         "assert app.database.engine.url.database == " + repr(str(database_file))],
        env=environment, capture_output=True, text=True, timeout=10,
    )
    assert result.returncode == 0, result.stderr
    assert not database_file.exists()
