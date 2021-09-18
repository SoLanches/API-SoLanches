from unittest import mock
import pytest

@pytest.fixture
def client(rest):
    client = rest.app.test_client()
    return client

@pytest.fixture
def cardapio_cadastrado():
    cardapio_json = {
    "_id": "6b6aae29176271992b0278509f15a63900f1f1a9",
    "created_at": 1631415578.674395,
    "destaques": [],
    "produtos": []
    }
    return cardapio_json


def test_status(client):
    expected_keys = ["status", "timestamp", "started_at", "service"]
    response = client.get('/status')
    status = response.json
    assert response.status_code == 200
    assert all(key in status for key in expected_keys)
    assert type(status['status']) is str
    assert type(status['timestamp']) is float
    assert type(status['started_at']) is float
    assert type(status['service']) is str
    assert status['status'] == 'operacional'
    assert status['service'] == 'api-solanches'


@mock.patch('solanches.rest.controller.get_cardapio')
def test_get_cardapio_sucesso(mock_get_cardapio, client, cardapio_cadastrado):
    expected_return = cardapio_cadastrado
    mock_get_cardapio.return_value = expected_return

    response = client.get('/comercio/solanches/cardapio')
    response_json = response.json

    assert response.status_code == 200
    assert isinstance(response_json, dict)
    assert response_json == expected_return


@mock.patch('solanches.rest.controller.get_cardapio')
def test_get_cardapio_exception_controller(mock_get_cardapio, client):
    exception_msg = 'Exception no controller'
    expected_error = Exception(exception_msg)
    mock_get_cardapio.side_effect = expected_error

    response = client.get('/comercio/solanches/cardapio')
    response_json = response.json

    assert response.status_code == 400
    assert response_json['message'] == exception_msg



