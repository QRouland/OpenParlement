from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = None
Session = None


def init_db(uri, echo=False):
    global engine, Session
    engine = create_engine(uri, echo=echo)
    Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    global Session
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
