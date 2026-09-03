class HandywrapperError(Exception):
    """Base class for all handywrapper errors."""


class HandywrapperAPIError(HandywrapperError):
    """Raised when hsd/hsw returns a non-2xx HTTP response."""

    def __init__(self, status_code, url, body):
        self.status_code = status_code
        self.url = url
        self.body = body
        super().__init__(f'{status_code} from {url}: {body}')


class HandywrapperConnectionError(HandywrapperError):
    """Raised when the node/wallet could not be reached."""


class HandywrapperDecodeError(HandywrapperError):
    """Raised when a 2xx response body was not valid JSON."""
