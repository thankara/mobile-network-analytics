from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, MappedAsDataclass, DeclarativeBase

from mobile_network_analytics.settings import get_db_settings


settings = get_db_settings()

engine = create_engine(settings.connection_string)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)


class Base(MappedAsDataclass, DeclarativeBase):
    pass


def get_db_session():
    """
    Get database session
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def get_db_session_context():
    """
    Context manager for handling database session and transactions.
    Commits transactions if successful or rolls back in the event of an error.
    """
    session = SessionLocal()
    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
