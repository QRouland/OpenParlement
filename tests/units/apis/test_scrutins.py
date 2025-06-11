from datetime import date
from unittest.mock import patch

@patch("app.apis.scrutins.scrutins_get_handler")
def test_scrutins_get_success_with_dates(mock_handler, client):
    mock_handler.return_value = [{"id": 1, "title": "Scrutin 1"}]

    response = client.get("/scrutins?start_date=2022-01-01&end_date=2022-01-31")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 1, "title": "Scrutin 1"}]
    mock_handler.assert_called_once_with(start_date=date(2022, 1, 1), end_date=date(2022, 1, 31))

@patch("app.apis.scrutins.scrutins_get_handler")
def test_scrutins_get_bad_start_date_format(mock_handler, client):
    response = client.get("/scrutins?start_date=01-01-2022&end_date=2022-01-31")

    assert response.status_code == 400
    assert b"Invalid 'start_date' date format." in response.data

@patch("app.apis.scrutins.scrutins_get_handler")
def test_scrutins_get_bad_end_date_format(mock_handler, client):
    response = client.get("/scrutins?start_date=2022-01-01&end_date=31-01-2022")

    assert response.status_code == 400
    assert b"Invalid 'end_date' date format." in response.data


@patch("app.apis.scrutins.scrutins_get_handler")
def test_scrutins_get_success_no_dates(mock_handler, client):
    mock_handler.return_value = [{"id": 2, "title": "Scrutin 2"}]

    response = client.get("/scrutins")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 2, "title": "Scrutin 2"}]
    mock_handler.assert_called_once_with(start_date=None, end_date=None)

@patch("app.apis.scrutins.scrutins_get_handler")
def test_scrutins_get_only_start_date(mock_handler, client):
    mock_handler.return_value = [{"id": 3, "title": "Scrutin 3"}]

    response = client.get("/scrutins?start_date=2022-01-01")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 3, "title": "Scrutin 3"}]
    mock_handler.assert_called_once_with(start_date=date(2022, 1, 1), end_date=None)

@patch("app.apis.scrutins.scrutins_get_handler")
def test_scrutins_get_only_end_date(mock_handler, client):
    mock_handler.return_value = [{"id": 4, "title": "Scrutin 4"}]

    response = client.get("/scrutins?end_date=2022-01-31")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 4, "title": "Scrutin 4"}]
    mock_handler.assert_called_once_with(start_date=None, end_date=date(2022, 1, 31))

@patch("app.apis.scrutins.scrutin_get_handler")
def test_scrutin_get_success(mock_handler, client):
    mock_handler.return_value = {"id": "1", "title": "Scrutin 1"}

    response = client.get("/scrutins/1")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"id": "1", "title": "Scrutin 1"}
    mock_handler.assert_called_once_with("1")

@patch("app.apis.scrutins.scrutin_get_handler")
def test_scrutin_get_not_found(mock_handler, client):
    mock_handler.return_value = None

    response = client.get("/scrutins/999")

    assert response.status_code == 404
    assert b"Scrutin with ID '999' not found." in response.data
    mock_handler.assert_called_once_with("999")
