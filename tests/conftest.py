from app import create_app
import os
import tempfile
from unittest.mock import patch, MagicMock

import pytest

from app import create_app
from app.db import init_db


@pytest.fixture(scope="session")
def test_db_uri():
    # Using SQLite in-memory for simplicity or temp file for persistence across threads
    db_fd, db_path = tempfile.mkstemp()
    uri = f"sqlite:///{db_path}"
    yield uri
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="session")
def app(test_db_uri):
    os.putenv("FLASK_DB_URL", test_db_uri)

    app = create_app()

    # # Create tables
    # Base.metadata.create_all(bind=engine)

    yield app

    # Drop tables
    # Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def flask_request_context(app):
    with app.test_request_context():
        yield


def make_session_scope_patch(module_path):
    mock_session = MagicMock()
    mock_ctx = MagicMock()
    mock_ctx.__enter__.return_value = mock_session
    mock_ctx.__exit__.return_value = None

    patcher = patch(f"{module_path}.session_scope", return_value=mock_ctx)
    return patcher, mock_session


@pytest.fixture
def patch_session_scope():
    """
    Usage:
    patcher, mock_session = patch_session_scope("app.scrutins")
    with patcher:
        ...
    """
    return make_session_scope_patch
