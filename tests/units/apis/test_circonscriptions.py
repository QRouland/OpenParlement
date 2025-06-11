from unittest.mock import patch

@patch("app.apis.circonscriptions.circonscriptions_get_handler")
def test_circonscriptions_get_success(mock_handler, client):
    mock_handler.return_value = [{"id": 1, "name": "Circonscription A"}]

    response = client.get("/circonscriptions")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 1, "name": "Circonscription A"}]
    mock_handler.assert_called_once_with()


@patch("app.apis.circonscriptions.circonscriptions_by_departement_handler")
def test_circonscriptions_by_departement_get_success(mock_handler, client):
    mock_handler.return_value = [{"id": 2, "name": "Circonscription B"}]

    response = client.get("/departements/01/circonscriptions")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 2, "name": "Circonscription B"}]
    mock_handler.assert_called_once_with("01")


@patch("app.apis.circonscriptions.circonscriptions_by_departement_handler")
def test_circonscriptions_by_departement_get_not_found(mock_handler, client):
    mock_handler.return_value = None

    response = client.get("/departements/99/circonscriptions")

    assert response.status_code == 404
    assert b"No circonscriptions found for this d\\u00e9partement." in response.data
    mock_handler.assert_called_once_with("99")


@patch("app.apis.circonscriptions.circonscription_get_handler")
def test_circonscription_get_success(mock_handler, client):
    mock_handler.return_value = {"id": "3", "name": "Circonscription C"}

    response = client.get("/departements/01/circonscriptions/1")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"id": "3", "name": "Circonscription C"}
    mock_handler.assert_called_once_with("01", "1")


@patch("app.apis.circonscriptions.circonscription_get_handler")
def test_circonscription_get_not_found(mock_handler, client):
    mock_handler.return_value = None

    response = client.get("/departements/99/circonscriptions/2")

    assert response.status_code == 404
    assert b"Circonscription not found." in response.data
    mock_handler.assert_called_once_with("99", "2")
