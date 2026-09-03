import requests

from .exceptions import (
    HandywrapperAPIError,
    HandywrapperConnectionError,
    HandywrapperDecodeError,
)


class HTTPClient:

    API_KEY = ''
    ADDRESS = ''
    PORT = ''
    TIMEOUT = 30

    def __init__(self, api_key:str, ip_address:str='127.0.0.1', port:int=0, timeout:int=30):
        """
        DESCRIPTION:

            Initialization of the HTTPClient base class shared by hsd and hsw.

        PARAMS:

        (*) Denotes required argument

        (*) api_key    : API key.

        ( ) ip_address : Node/wallet ip. Default = '127.0.0.1'.

        ( ) port       : Node/wallet port.

        ( ) timeout    : Request timeout in seconds. Default = 30
        """

        self.API_KEY = api_key
        self.ADDRESS = ip_address
        self.PORT = str(port)
        self.TIMEOUT = timeout
    ### END METHOD ################################### __init__(self, api_key:str, ip_address:str='127.0.0.1', port:int=0, timeout:int=30)

    def _request(self, method:str, endpoint:str, json_body:dict=None, params:dict=None):
        """
        DESCRIPTION:

            Send an HTTP request to the API and return the parsed JSON
            response. Raises HandywrapperConnectionError if the node/wallet
            could not be reached, HandywrapperAPIError on a non-2xx response,
            and HandywrapperDecodeError if a 2xx response body isn't JSON.

        PARAMS:

        (*) Denotes required argument

        (*) method    : HTTP method (GET, POST, PUT, PATCH, DELETE).

        (*) endpoint  : API endpoint to send the request to.

        ( ) json_body : Request body, sent as JSON.

        ( ) params    : Query string parameters.
        """

        url = f'http://x:{self.API_KEY}@{self.ADDRESS}:{self.PORT}{endpoint}'

        try:
            response = requests.request(method, url, json=json_body, params=params, timeout=self.TIMEOUT)
        except requests.exceptions.RequestException as e:
            raise HandywrapperConnectionError(str(e)) from e

        if not response.ok:
            try:
                body = response.json()
            except ValueError:
                body = response.text
            raise HandywrapperAPIError(response.status_code, url, body)

        try:
            return response.json()
        except ValueError as e:
            raise HandywrapperDecodeError(f'Non-JSON response from {url}') from e
    ### END METHOD ################################### _request(self, method:str, endpoint:str, json_body:dict=None, params:dict=None)

    def get(self, endpoint:str, params:dict=None):
        """
        DESCRIPTION:

            GET (json) response from API

        PARAMS:

        (*) Denotes required argument

        (*) endpoint : API endpoint to send GET request.

        ( ) params   : Query string parameters.
        """

        return self._request('GET', endpoint, params=params)
    ### END METHOD ################################### get(self, endpoint:str, params:dict=None)

    def post(self, endpoint:str, json_body:dict=None):
        """
        DESCRIPTION:

            Send POST (json) message to API

        PARAMS:

        (*) Denotes required argument

        (*) endpoint  : API endpoint to send POST message.

        ( ) json_body : Message to be sent.
        """

        return self._request('POST', endpoint, json_body=json_body)
    ### END METHOD ################################### post(self, endpoint:str, json_body:dict=None)

    def put(self, endpoint:str, json_body:dict=None):
        """
        DESCRIPTION:

            Send PUT (json) message to API

        PARAMS:

        (*) Denotes required argument

        (*) endpoint  : API endpoint to send PUT message.

        ( ) json_body : Message to be sent.
        """

        return self._request('PUT', endpoint, json_body=json_body)
    ### END METHOD ################################### put(self, endpoint:str, json_body:dict=None)

    def patch(self, endpoint:str, json_body:dict=None):
        """
        DESCRIPTION:

            Send PATCH (json) message to API

        PARAMS:

        (*) Denotes required argument

        (*) endpoint  : API endpoint to send PATCH message.

        ( ) json_body : Message to be sent.
        """

        return self._request('PATCH', endpoint, json_body=json_body)
    ### END METHOD ################################### patch(self, endpoint:str, json_body:dict=None)

    def delete(self, endpoint:str, json_body:dict=None):
        """
        DESCRIPTION:

            Send DELETE (json) message to API

        PARAMS:

        (*) Denotes required argument

        (*) endpoint  : API endpoint to send DELETE message.

        ( ) json_body : Message to be sent.
        """

        return self._request('DELETE', endpoint, json_body=json_body)
    ### END METHOD ################################### delete(self, endpoint:str, json_body:dict=None)
