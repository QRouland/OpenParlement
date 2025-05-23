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
    class TestConfig:
        HOST = "127.0.0.1:5000"
        DB_URL = "sqlite://"
        DB_ECHO = False
        MAX_PER_PAGE = 200
        DEFAULT_PER_PAGE = 100
        ACTEURS_FOLDER = "data/acteurs"
        ORGANES_FOLDER = "data/organes"
        SCRUTINS_FOLDER = "data/scrutins"
        ACTEURS_ORGANES_URL = (
            "https://data.assemblee-nationale.fr/static/openData/repository/17/amo/deputes_actifs_mandats_actifs_organes/"
            "AMO10_deputes_actifs_mandats_actifs_organes.json.zip"
        )
        SCRUTINS_URL = "https://data.assemblee-nationale.fr/static/openData/repository/17/loi/scrutins/Scrutins.json.zip"

    app = create_app(config_class=TestConfig, load_env=False)

    # Initialize the test database engine and session
    init_db(test_db_uri)

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
