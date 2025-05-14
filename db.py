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


def init_db() -> None:
    from app import engine
    from loader.depute import load_from_json
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    load_from_json()
