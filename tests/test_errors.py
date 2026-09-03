import pytest
import responses
import requests.exceptions

from handywrapper.exceptions import (
    HandywrapperAPIError,
    HandywrapperConnectionError,
    HandywrapperDecodeError,
)


@responses.activate
def test_non_2xx_raises_api_error(hsd_client):
    responses.add(responses.GET, 'http://x:testkey@127.0.0.1:12037/mempool',
                   json={'error': {'message': 'bad request'}}, status=400)

    with pytest.raises(HandywrapperAPIError) as exc:
        hsd_client.getMemPool()

    assert exc.value.status_code == 400
    assert exc.value.body == {'error': {'message': 'bad request'}}


@responses.activate
def test_non_2xx_non_json_body_falls_back_to_text(hsd_client):
    responses.add(responses.GET, 'http://x:testkey@127.0.0.1:12037/mempool',
                   body='internal error', status=500, content_type='text/plain')

    with pytest.raises(HandywrapperAPIError) as exc:
        hsd_client.getMemPool()

    assert exc.value.status_code == 500
    assert exc.value.body == 'internal error'


@responses.activate
def test_connection_error_raises_handywrapper_connection_error(hsd_client):
    responses.add(responses.GET, 'http://x:testkey@127.0.0.1:12037/mempool',
                   body=requests.exceptions.ConnectionError('refused'))

    with pytest.raises(HandywrapperConnectionError):
        hsd_client.getMemPool()


@responses.activate
def test_2xx_non_json_body_raises_decode_error(hsd_client):
    responses.add(responses.GET, 'http://x:testkey@127.0.0.1:12037/mempool',
                   body='not json', status=200, content_type='text/plain')

    with pytest.raises(HandywrapperDecodeError):
        hsd_client.getMemPool()


@responses.activate
def test_successful_response_returns_parsed_json(hsd_client):
    responses.add(responses.GET, 'http://x:testkey@127.0.0.1:12037/mempool',
                   json=['abc'], status=200)

    assert hsd_client.getMemPool() == ['abc']


@responses.activate
def test_bool_query_params_serialize_lowercase(hsd_client):
    # Bug-fix regression: `requests` stringifies a Python bool to "True"/"False"
    # in a query string, but hsd's Validator.bool() only accepts lowercase
    # 'true'/'false' (or '1'/'0') and 400s on anything else.
    responses.add(responses.GET, 'http://x:testkey@127.0.0.1:12037/mempool/invalid',
                   json={}, status=200)

    hsd_client.getMemPoolInvalid(verbose=True)

    assert 'verbose=true' in responses.calls[0].request.url
    assert 'verbose=True' not in responses.calls[0].request.url
