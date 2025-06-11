from unittest.mock import patch

@patch("app.apis.votes.votes_get_handler")
def test_votes_get_success(mock_handler, client):
    mock_handler.return_value = [{"id": 1, "scrutin": "A", "depute": "B"}]

    response = client.get("/votes")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 1, "scrutin": "A", "depute": "B"}]
    mock_handler.assert_called_once_with()


@patch("app.apis.votes.vote_get_handler")
def test_vote_get_success(mock_handler, client):
    mock_handler.return_value = {"id": "2", "scrutin": "C", "depute": "D"}

    response = client.get("/votes/2")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"id": "2", "scrutin": "C", "depute": "D"}
    mock_handler.assert_called_once_with("2")


@patch("app.apis.votes.vote_get_handler")
def test_vote_get_not_found(mock_handler, client):
    mock_handler.return_value = None

    response = client.get("/votes/99")

    assert response.status_code == 404
    assert b"Vote with ID '99' not found." in response.data
    mock_handler.assert_called_once_with("99")


@patch("app.apis.votes.scrutin_votes_get_handler")
def test_votes_by_scrutin_success(mock_handler, client):
    mock_handler.return_value = [{"id": 1, "scrutin": "E", "depute": "F"}]

    response = client.get("/scrutins/3/votes")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 1, "scrutin": "E", "depute": "F"}]
    mock_handler.assert_called_once_with("3")


@patch("app.apis.votes.scrutin_votes_get_handler")
def test_votes_by_scrutin_not_found(mock_handler, client):
    mock_handler.return_value = None

    response = client.get("/scrutins/99/votes")

    assert response.status_code == 404
    assert b"No votes found for scrutin with ID '99'." in response.data
    mock_handler.assert_called_once_with("99")


@patch("app.apis.votes.depute_votes_get_handler")
def test_votes_by_depute_success(mock_handler, client):
    mock_handler.return_value = [{"id": 1, "scrutin": "G", "depute": "H"}]

    response = client.get("/deputes/4/votes")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 1, "scrutin": "G", "depute": "H"}]
    mock_handler.assert_called_once_with("4")


@patch("app.apis.votes.depute_votes_get_handler")
def test_votes_by_depute_not_found(mock_handler, client):
    mock_handler.return_value = None

    response = client.get("/deputes/99/votes")

    assert response.status_code == 404
    assert b"D\\u00e9put\\u00e9 with ID '99' not found." in response.data
    mock_handler.assert_called_once_with("99")


@patch("app.apis.votes.depute_scrutin_vote_get_handler")
def test_vote_by_depute_and_scrutin_success(mock_handler, client):
    mock_handler.return_value = {"id": "5", "scrutin": "I", "depute": "J"}

    response = client.get("/deputes/6/votes/7")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == {"id": "5", "scrutin": "I", "depute": "J"}
    mock_handler.assert_called_once_with("6", "7")


@patch("app.apis.votes.depute_scrutin_vote_get_handler")
def test_vote_by_depute_and_scrutin_not_found(mock_handler, client):
    mock_handler.return_value = None

    response = client.get("/deputes/99/votes/98")

    assert response.status_code == 404
    assert b"Vote not found for d\\u00e9put\\u00e9 '99' on scrutin '98'." in response.data
    mock_handler.assert_called_once_with("99", "98")


@patch("app.apis.votes.depute_votes_stats_get_handler")
def test_votes_stats_by_depute_success(mock_handler, client):
    mock_handler.return_value = [{"id": 1, "scrutin": "K", "depute": "L"}]

    response = client.get("/deputes/8/votes/stats")

    assert response.status_code == 200
    assert response.is_json
    assert response.get_json() == [{"id": 1, "scrutin": "K", "depute": "L"}]
    mock_handler.assert_called_once_with("8")


@patch("app.apis.votes.depute_votes_stats_get_handler")
def test_votes_stats_by_depute_not_found(mock_handler, client):
    mock_handler.return_value = None

    response = client.get("/deputes/99/votes/stats")

    assert response.status_code == 404
    assert b"D\\u00e9put\\u00e9 with ID '99' not found." in response.data
    mock_handler.assert_called_once_with("99")