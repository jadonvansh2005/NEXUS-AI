"""
UPSS HTTP Exceptions
"""

from __future__ import annotations


class HTTPClientError(Exception):
    """Base HTTP exception."""
    pass


class HTTPTimeoutError(HTTPClientError):
    """Raised when request times out."""
    pass


class HTTPAuthenticationError(HTTPClientError):
    """Authentication failed."""
    pass


class HTTPRateLimitError(HTTPClientError):
    """Rate limit exceeded."""
    pass


class HTTPConnectionError(HTTPClientError):
    """Unable to connect."""
    pass


class HTTPResponseError(HTTPClientError):
    """Unexpected response."""
    pass