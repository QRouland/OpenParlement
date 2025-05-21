from contextlib import contextmanager

from models import Base


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    from app import Session
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
