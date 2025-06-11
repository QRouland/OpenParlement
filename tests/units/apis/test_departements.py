from unittest.mock import patch

@patch("app.apis.departements.departements_get_handler")
def test_departements_get_success(mock_handler, client):
    mock_handler.return_value = [{"code": "01", "name": "Ain"}]

    response = client.get("/departements")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"code": "01", "name": "Ain"}]
    mock_handler.assert_called_once_with()

@patch("app.apis.departements.departement_get_handler")
def test_departement_get_success(mock_handler, client):
    mock_handler.return_value = {"code": "02", "name": "Aisne"}

    response = client.get("/departements/02")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"code": "02", "name": "Aisne"}
    mock_handler.assert_called_once_with("02")

@patch("app.apis.departements.departement_get_handler")
def test_departement_get_not_found(mock_handler, client):
    mock_handler.return_value = None

    response = client.get("/departements/99")

    assert response.status_code == 404
    assert b"D\\u00e9partement with code '99' not found." in response.data
    mock_handler.assert_called_once_with("99")
