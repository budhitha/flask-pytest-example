import json

from flask import Flask

from handlers.routes import configure_routes

_app = Flask(__name__)
configure_routes(_app)

_url = {'base': '/', 'post': '/post/test'}


def test_base_route():
    client = _app.test_client()

    response = client.get(_url['base'])
    assert response.get_data() == b'Hello, World!'
    assert response.status_code == 200


def test_post_route__success():
    client = _app.test_client()

    mock_request_headers = {
        'authorization-sha256': '123'
    }

    mock_request_data = {
        'request_id': '123',
        'payload': {
            'py': 'pi',
            'java': 'script'
        }
    }

    response = client.post(_url['post'], data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 200


def test_post_route__failure__unauthorized():
    client = _app.test_client()

    mock_request_headers = {}

    mock_request_data = {
        'request_id': '123',
        'payload': {
            'py': 'pi',
            'java': 'script'
        }
    }

    response = client.post(_url['post'], data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 401


def test_post_route__failure__bad_request():
    client = _app.test_client()

    mock_request_headers = {
        'authorization-sha256': '123'
    }

    mock_request_data = {}

    response = client.post(_url['post'], data=json.dumps(mock_request_data), headers=mock_request_headers)
    assert response.status_code == 400
