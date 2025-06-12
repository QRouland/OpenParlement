from inspect import isclass

import pytest
from unittest.mock import patch, MagicMock

from app.handlers.deputes import deputes_get_handler, depute_get_handler, DeputeSchema
from app.models.depute import Depute
from tests.utils import stmt_to_string


@pytest.fixture(autouse=True)
def mock_normalize():
    with patch("app.utils.normalize", side_effect=lambda x: x.lower()) as mock:
        yield mock


@pytest.fixture
def mock_pagined_query():
    with patch("app.handlers.deputes.pagined_query") as mock:
        mock.return_value = [{"id": 1, "name": "Test"}]
        yield mock


@pytest.fixture
def mock_query_one():
    with patch('app.handlers.deputes.query_one') as mocked_method:
        yield mocked_method

def test_deputes_get_handler_no_filters(
    flask_request_context, patch_session_scope, mock_pagined_query
):
    patcher, mock_session = patch_session_scope("app.handlers.deputes")
    with patcher:
        result = deputes_get_handler()

        assert result == [{"id": 1, "name": "Test"}]
        mock_pagined_query.assert_called_once()
        args, kwargs = mock_pagined_query.call_args
        assert args[0] == mock_session
        assert (
            stmt_to_string(args[1])
            == "SELECT depute.id, depute.last_name, depute.last_name_normalize, depute.first_name, "
               "depute.first_name_normalize, depute.gp_id, depute.circonscription_departement_code, "
               "depute.circonscription_code "
               "FROM depute"
        )
        assert (
            stmt_to_string(args[2])
            == "SELECT count(*) AS count_1 FROM depute"
        )
        assert isinstance(args[3], DeputeSchema)
        assert args[3].many == True
        assert  str(args[4]) == str(Depute.last_name)


def test_deputes_get_handler_first_name_only(
    flask_request_context, patch_session_scope, mock_pagined_query
):
    patcher, mock_session = patch_session_scope("app.handlers.deputes")
    with patcher:
        result = deputes_get_handler(first_name="Jean")

        assert result == [{"id": 1, "name": "Test"}]
        mock_pagined_query.assert_called_once()
        args, kwargs = mock_pagined_query.call_args
        assert args[0] == mock_session
        assert (
            stmt_to_string(args[1])
            == "SELECT depute.id, depute.last_name, depute.last_name_normalize, depute.first_name,"
               " depute.first_name_normalize, depute.gp_id, depute.circonscription_departement_code, "
               "depute.circonscription_code "
               "FROM depute "
               "WHERE depute.first_name_normalize = 'jean'"
        )
        assert (
            stmt_to_string(args[2])
            == "SELECT count(*) AS count_1 FROM depute WHERE depute.first_name_normalize = 'jean'"
        )
        assert isinstance(args[3], DeputeSchema)
        assert args[3].many == True
        assert  str(args[4]) == str(Depute.last_name)


def test_deputes_get_handler_last_name_only(
    flask_request_context, patch_session_scope, mock_pagined_query
):
    patcher, mock_session = patch_session_scope("app.handlers.deputes")
    with patcher:
        result = deputes_get_handler(last_name="Dupont")

        assert result == [{"id": 1, "name": "Test"}]
        mock_pagined_query.assert_called_once()
        args, kwargs = mock_pagined_query.call_args
        assert args[0] == mock_session
        assert (
            stmt_to_string(args[1])
            == "SELECT depute.id, depute.last_name, depute.last_name_normalize, depute.first_name, "
               "depute.first_name_normalize, depute.gp_id, depute.circonscription_departement_code, "
               "depute.circonscription_code "
               "FROM depute "
               "WHERE depute.last_name_normalize = 'dupont'"
        )
        assert (
            stmt_to_string(args[2])
            == "SELECT count(*) AS count_1 FROM depute WHERE depute.last_name_normalize = 'dupont'"
        )
        assert isinstance(args[3], DeputeSchema)
        assert args[3].many == True
        assert  str(args[4]) == str(Depute.last_name)


def test_deputes_get_handler_both_names(
    flask_request_context, patch_session_scope, mock_pagined_query
):
    patcher, mock_session = patch_session_scope("app.handlers.deputes")
    with patcher:
        result = deputes_get_handler(first_name="Jean", last_name="Dupont")

        assert result == [{"id": 1, "name": "Test"}]
        mock_pagined_query.assert_called_once()
        args, kwargs = mock_pagined_query.call_args
        assert args[0] == mock_session
        assert (
            stmt_to_string(args[1])
            == "SELECT depute.id, depute.last_name, depute.last_name_normalize, depute.first_name, "
               "depute.first_name_normalize, depute.gp_id, depute.circonscription_departement_code, "
               "depute.circonscription_code "
               "FROM depute "
               "WHERE depute.first_name_normalize = 'jean' AND depute.last_name_normalize = 'dupont'"
        )
        assert (
            stmt_to_string(args[2])
            == "SELECT count(*) AS count_1 FROM depute "
               "WHERE depute.first_name_normalize = 'jean' AND depute.last_name_normalize = 'dupont'"
        )
        assert isinstance(args[3], DeputeSchema)
        assert args[3].many == True
        assert  str(args[4]) == str(Depute.last_name)



@patch("app.handlers.deputes.query_one")
def test_depute_get_handler_success(mock_query_one):
    mock_query_one.return_value = {"id": 1, "name": "Test"}

    result = depute_get_handler(depute_id="1")

    assert result == {"id": 1, "name": "Test"}
    mock_query_one.assert_called_once()


@pytest.mark.parametrize("depute_id, res", [
    ( "1",  {"id": 1, "name": "Test"}),
    ("99", None),
])
def test_depute_get_handler(mock_query_one, patch_session_scope, depute_id, res):
    patcher, mock_session = patch_session_scope("app.handlers.deputes")
    with patcher:
        mock_query_one.return_value = res
        result = depute_get_handler(depute_id=depute_id)

        assert result == res
        mock_query_one.assert_called_once()
        args, kwargs = mock_query_one.call_args
        assert args[0] == mock_session
        assert args[1] == Depute
        assert  stmt_to_string(args[2]) == f"depute.id = '{depute_id}'"
        assert isinstance(args[3], DeputeSchema)
        assert args[3].many == False
