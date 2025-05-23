from unittest.mock import patch


@patch("app.apis.deputes.deputes_get_handler")
def test_deputes_get_success(mock_handler, client):
    mock_handler.return_value = [{"id": 1, "name": "Jean Dupont"}]

    response = client.get("/deputes?first_name=Jean&last_name=Dupont")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 1, "name": "Jean Dupont"}]
    mock_handler.assert_called_once_with("Jean", "Dupont")


@patch("app.apis.deputes.deputes_get_handler")
def test_deputes_get_bad_request(mock_handler, client):
    mock_handler.return_value = None  # or []

    response = client.get("/deputes?first_name=Jean&last_name=Dupont")

    assert response.status_code == 400
    mock_handler.assert_called_once_with("Jean", "Dupont")


@patch("app.apis.deputes.deputes_get_handler")
def test_deputes_get_no_params(mock_handler, client):
    mock_handler.return_value = [{"id": 2, "name": "Generic Deputy"}]

    response = client.get("/deputes")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 2, "name": "Generic Deputy"}]
    mock_handler.assert_called_once_with(None, None)


@patch("app.apis.deputes.deputes_get_handler")
def test_deputes_get_only_first_name(mock_handler, client):
    mock_handler.return_value = [{"id": 3, "name": "Jean"}]

    response = client.get("/deputes?first_name=Jean")

    assert response.status_code == 200
    assert response.get_json() == [{"id": 3, "name": "Jean"}]
    mock_handler.assert_called_once_with("Jean", None)


@patch("app.apis.deputes.deputes_get_handler")
def test_deputes_get_only_last_name(mock_handler, client):
    mock_handler.return_value = [{"id": 4, "name": "Dupont"}]

    response = client.get("/deputes?last_name=Dupont")

    assert response.status_code == 200
    assert response.get_json() == [{"id": 4, "name": "Dupont"}]
    mock_handler.assert_called_once_with(None, "Dupont")


@patch("app.apis.deputes.depute_get_handler")
def test_depute_get_success(mock_handler, client):
    mock_handler.return_value = {"id": "123", "name": "Jean Dupont"}

    response = client.get("/deputes/123")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"id": "123", "name": "Jean Dupont"}
    mock_handler.assert_called_once_with("123")


@patch("app.apis.deputes.depute_get_handler")
def test_depute_get_not_found(mock_handler, client):
    mock_handler.return_value = None

    response = client.get("/deputes/999")

    assert response.status_code == 404
    assert b"Depute not found." in response.data
    mock_handler.assert_called_once_with("999")
