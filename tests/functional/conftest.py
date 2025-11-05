from typing import Generator, Any
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False)


@pytest.fixture(scope="function")
def override_settings(monkeypatch):
    """
    Overrides db settings for testing
    :param monkeypatch:
    :return:
    """
    monkeypatch.setenv("DB_NAME", "test_db")
    monkeypatch.setenv("DB_USERNAME", "test_user")
    monkeypatch.setenv("DB_PASSWORD", "test_password")
    monkeypatch.setenv("DB_HOST", "localhost")
    monkeypatch.setenv("DB_PORT", "5432")


@pytest.fixture(scope="function")
def engine(override_settings) -> Generator[Engine, Any, None]:
    """
    Creates an in-memory sqlite db for testing.
    """
    import mobile_network_analytics.models as models
    from mobile_network_analytics.db.base import Base

    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def db_session(engine) -> Generator[Any, Any, None]:
    """
    Creates a database session for testing.
    """

    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


# --- FastAPI client fixture ---
@pytest.fixture(scope="function")
def client(db_session) -> Generator[Any, Any, None]:
    from mobile_network_analytics.api.main import app
    from mobile_network_analytics.db.db import get_db_session

    # override dependency so app never uses the real MySQL engine
    def override_get_db_session():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db_session] = override_get_db_session
    yield TestClient(app)
