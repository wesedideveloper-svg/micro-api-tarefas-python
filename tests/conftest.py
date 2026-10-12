"""Cliente HTTP isolado do banco de desenvolvimento, inclusive no lifespan."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import main
from app.database import get_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'api.db'}", connect_args={"check_same_thread": False}
    )
    sessions = sessionmaker(bind=engine, autoflush=False)

    def override_get_db():
        with sessions() as session:
            yield session

    monkeypatch.setattr(main, "engine", engine)
    original_overrides = main.app.dependency_overrides.copy()
    main.app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(main.app, raise_server_exceptions=False) as test_client:
            yield test_client
    finally:
        main.app.dependency_overrides.clear()
        main.app.dependency_overrides.update(original_overrides)
        engine.dispose()
