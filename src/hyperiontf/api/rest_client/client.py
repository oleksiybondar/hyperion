import requests
from hyperiontf.logging import getLogger
from hyperiontf.typing import LoggerSource, HTTPMethod, AnyRequest, HTTPMethodType
from typing import Optional
from urllib.parse import urlparse, urlunparse
from .request import Request
from hyperiontf.configuration.config import config

# Setting up logging
logger = getLogger(LoggerSource.REST_CLIENT)


class Client:
    def __init__(
        self,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        netloc: Optional[str] = None,
        path: Optional[str] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        auth: Optional[dict] = None,
        follow_redirects: bool = config.rest.follow_redirects,
        log_redirects: bool = config.rest.log_redirects,
        post_redirect_get: bool = config.rest.log_redirects,
        accept_errors: bool = config.rest.accept_errors,
        redirections_limit: int = config.rest.redirections_limit,
        connection_timeout: int = config.rest.connection_timeout,
        request_timeout: int = config.rest.request_timeout,
        default_event_logging_level: str = "info",
        logger=logger,
    ):
        """
        Initializes the client object with the specified parameters.

        :param url: The base URL for the client.
        :param scheme: The URL scheme (e.g., "http" or "https").
        :param netloc: The network location (e.g., "www.example.com").
        :param path: The URL path.
        :param params: The URL parameters.
        :param query: The URL query string.
        :param fragment: The URL fragment.
        :param headers: The default headers for all requests made by this client.
        :param cookies: The default cookies for all requests made by this client.
        :param auth: The default authentication info for all requests made by this client.
        :param follow_redirects: If True, the client will automatically follow redirects.
        :param log_redirects: If True, the client will automatically log redirects, NOTE: slows down execution time
        :param post_redirect_get: If True, the client will automatically convert redirected POST requests into GET
        requests.
        :param accept_errors: If True, the client will not raise exceptions for HTTP error status codes.
        :param redirections_limit: The maximum number of redirects the client will follow for a single request.
        :param connection_timeout: The timeout for establishing a connection.
        :param request_timeout: The timeout for completing a request.
        """
        self.scheme, self.netloc, self.path, self.params, self.query, self.fragment = (
            self._parse_url(url)
            if url
            else (scheme, netloc, path, params, query, fragment)
        )

        self.headers = headers or {}
        self.cookies = cookies or {}
        self.auth = auth or {}
        self.follow_redirects = follow_redirects
        self.log_redirects = log_redirects
        self.post_redirect_get = post_redirect_get
        self.accept_errors = accept_errors
        self.redirections_limit = redirections_limit
        self.connection_timeout = connection_timeout
        self.request_timeout = request_timeout

        self.logger = logger
        self._default_event_logging_level = default_event_logging_level

        self.session = requests.Session()
        self.session.max_redirects = redirections_limit

    @property
    def default_event_logging_level(self) -> str:
        """
        Returns the default logging level for events.
        """
        return self._default_event_logging_level

    @default_event_logging_level.setter
    def default_event_logging_level(self, value: str):
        """
        Sets the default logging level for events.

        Parameters:
        value (str): The logging level to set. Must be either 'debug' or 'info'.

        Raises:
        ValueError: If the provided logging level is not 'debug' or 'info'.
        """
        if value not in ["debug", "info"]:
            raise ValueError("Logging level must be 'debug' or 'info'.")
        self._default_event_logging_level = value

    @staticmethod
    def _parse_url(url: str):
        """
        Parses the URL and extracts its components.

        :param url: The URL to parse.
        :return: Tuple of URL components (scheme, netloc, path, params, query, fragment).
        """
        url_parts = urlparse(url)
        return (
            url_parts.scheme,
            url_parts.netloc,
            url_parts.path,
            url_parts.params,
            url_parts.query,
            url_parts.fragment,
        )

    def get(
        self,
        payload: Optional[dict] = None,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        netloc: Optional[str] = None,
        path: Optional[str] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        auth: Optional[dict] = None,
        follow_redirects: Optional[bool] = None,
        log_redirects: Optional[bool] = None,
        post_redirect_get: Optional[bool] = None,
        accept_errors: Optional[bool] = None,
        redirections_limit: Optional[int] = None,
        connection_timeout: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ):
        """
        Creates and execute `request` using "GET".

        :param payload: The data to send with the request (for POST or PUT requests).
        :param url: The URL for this request.
        :param scheme: The URL scheme (e.g., "http" or "https").
        :param netloc: The network location (e.g., "www.example.com").
        :param path: The URL path.
        :param params: The URL parameters.
        :param query: The URL query string.
        :param fragment: The URL fragment.
        :param headers: The headers for this request.
        :param cookies: The cookies for this request.
        :param auth: The authentication details for this request (e.g., {'username': 'user', 'password': 'pass'}).
        :param follow_redirects: If True, the request will automatically follow redirects.
        :param log_redirects: If True, the client will automatically log redirects, NOTE: slows down execution time
        :param post_redirect_get: If True, the request will automatically convert redirected POST requests into GET
        requests.
        :param accept_errors: If True, the request will not raise exceptions for HTTP error status codes.
        :param redirections_limit: The maximum number of redirects the request will follow.
        :param connection_timeout: The timeout for establishing a connection for this request.
        :param request_timeout: The timeout for completing this request.
        """
        request = self.request(
            method=HTTPMethod.GET,
            payload=payload,
            url=url,
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=params,
            query=query,
            fragment=fragment,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            log_redirects=log_redirects,
            post_redirect_get=post_redirect_get,
            accept_errors=accept_errors,
            redirections_limit=redirections_limit,
            connection_timeout=connection_timeout,
            request_timeout=request_timeout,
        )
        return request.execute()

    # Wrapper method for POST with default method="POST"
    def post(
        self,
        payload: Optional[dict] = None,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        netloc: Optional[str] = None,
        path: Optional[str] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        auth: Optional[dict] = None,
        follow_redirects: Optional[bool] = None,
        log_redirects: Optional[bool] = None,
        post_redirect_get: Optional[bool] = None,
        accept_errors: Optional[bool] = None,
        redirections_limit: Optional[int] = None,
        connection_timeout: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ):
        """
        Creates and execute `request` using "POST".

        :param payload: The data to send with the request (for POST or PUT requests).
        :param url: The URL for this request.
        :param scheme: The URL scheme (e.g., "http" or "https").
        :param netloc: The network location (e.g., "www.example.com").
        :param path: The URL path.
        :param params: The URL parameters.
        :param query: The URL query string.
        :param fragment: The URL fragment.
        :param headers: The headers for this request.
        :param cookies: The cookies for this request.
        :param auth: The authentication details for this request (e.g., {'username': 'user', 'password': 'pass'}).
        :param follow_redirects: If True, the request will automatically follow redirects.
        :param log_redirects: If True, the client will automatically log redirects, NOTE: slows down execution time
        :param post_redirect_get: If True, the request will automatically convert redirected POST requests into GET
        requests.
        :param accept_errors: If True, the request will not raise exceptions for HTTP error status codes.
        :param redirections_limit: The maximum number of redirects the request will follow.
        :param connection_timeout: The timeout for establishing a connection for this request.
        :param request_timeout: The timeout for completing this request.
        """
        request = self.request(
            method=HTTPMethod.POST,
            payload=payload,
            url=url,
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=params,
            query=query,
            fragment=fragment,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            log_redirects=log_redirects,
            post_redirect_get=post_redirect_get,
            accept_errors=accept_errors,
            redirections_limit=redirections_limit,
            connection_timeout=connection_timeout,
            request_timeout=request_timeout,
        )
        return request.execute()

    # Wrapper method for PUT with default method="PUT"
    def put(
        self,
        payload: Optional[dict] = None,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        netloc: Optional[str] = None,
        path: Optional[str] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        auth: Optional[dict] = None,
        follow_redirects: Optional[bool] = None,
        log_redirects: Optional[bool] = None,
        post_redirect_get: Optional[bool] = None,
        accept_errors: Optional[bool] = None,
        redirections_limit: Optional[int] = None,
        connection_timeout: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ):
        """
        Creates and execute `request` using "PUT".

        :param payload: The data to send with the request (for POST or PUT requests).
        :param url: The URL for this request.
        :param scheme: The URL scheme (e.g., "http" or "https").
        :param netloc: The network location (e.g., "www.example.com").
        :param path: The URL path.
        :param params: The URL parameters.
        :param query: The URL query string.
        :param fragment: The URL fragment.
        :param headers: The headers for this request.
        :param cookies: The cookies for this request.
        :param auth: The authentication details for this request (e.g., {'username': 'user', 'password': 'pass'}).
        :param follow_redirects: If True, the request will automatically follow redirects.
        :param log_redirects: If True, the client will automatically log redirects, NOTE: slows down execution time
        :param post_redirect_get: If True, the request will automatically convert redirected POST requests into GET
        requests.
        :param accept_errors: If True, the request will not raise exceptions for HTTP error status codes.
        :param redirections_limit: The maximum number of redirects the request will follow.
        :param connection_timeout: The timeout for establishing a connection for this request.
        :param request_timeout: The timeout for completing this request.
        """
        request = self.request(
            method=HTTPMethod.PUT,
            payload=payload,
            url=url,
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=params,
            query=query,
            fragment=fragment,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            log_redirects=log_redirects,
            post_redirect_get=post_redirect_get,
            accept_errors=accept_errors,
            redirections_limit=redirections_limit,
            connection_timeout=connection_timeout,
            request_timeout=request_timeout,
        )
        return request.execute()

    # Wrapper method for DELETE with default method="DELETE"
    def delete(
        self,
        payload: Optional[dict] = None,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        netloc: Optional[str] = None,
        path: Optional[str] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        auth: Optional[dict] = None,
        follow_redirects: Optional[bool] = None,
        log_redirects: Optional[bool] = None,
        post_redirect_get: Optional[bool] = None,
        accept_errors: Optional[bool] = None,
        redirections_limit: Optional[int] = None,
        connection_timeout: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ):
        """
        Creates and execute `request` using "DELETE".

        :param payload: The data to send with the request (for POST or PUT requests).
        :param url: The URL for this request.
        :param scheme: The URL scheme (e.g., "http" or "https").
        :param netloc: The network location (e.g., "www.example.com").
        :param path: The URL path.
        :param params: The URL parameters.
        :param query: The URL query string.
        :param fragment: The URL fragment.
        :param headers: The headers for this request.
        :param cookies: The cookies for this request.
        :param auth: The authentication details for this request (e.g., {'username': 'user', 'password': 'pass'}).
        :param follow_redirects: If True, the request will automatically follow redirects.
        :param log_redirects: If True, the client will automatically log redirects, NOTE: slows down execution time
        :param post_redirect_get: If True, the request will automatically convert redirected POST requests into GET
        requests.
        :param accept_errors: If True, the request will not raise exceptions for HTTP error status codes.
        :param redirections_limit: The maximum number of redirects the request will follow.
        :param connection_timeout: The timeout for establishing a connection for this request.
        :param request_timeout: The timeout for completing this request.
        """
        request = self.request(
            method=HTTPMethod.DELETE,
            payload=payload,
            url=url,
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=params,
            query=query,
            fragment=fragment,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            log_redirects=log_redirects,
            post_redirect_get=post_redirect_get,
            accept_errors=accept_errors,
            redirections_limit=redirections_limit,
            connection_timeout=connection_timeout,
            request_timeout=request_timeout,
        )
        return request.execute()

    # Wrapper method for PATCH with default method="PATCH"
    def patch(
        self,
        payload: Optional[dict] = None,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        netloc: Optional[str] = None,
        path: Optional[str] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        auth: Optional[dict] = None,
        follow_redirects: Optional[bool] = None,
        log_redirects: Optional[bool] = None,
        post_redirect_get: Optional[bool] = None,
        accept_errors: Optional[bool] = None,
        redirections_limit: Optional[int] = None,
        connection_timeout: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ):
        """
        Creates and execute `request` using "PATCH".

        :param payload: The data to send with the request (for POST or PUT requests).
        :param url: The URL for this request.
        :param scheme: The URL scheme (e.g., "http" or "https").
        :param netloc: The network location (e.g., "www.example.com").
        :param path: The URL path.
        :param params: The URL parameters.
        :param query: The URL query string.
        :param fragment: The URL fragment.
        :param headers: The headers for this request.
        :param cookies: The cookies for this request.
        :param auth: The authentication details for this request (e.g., {'username': 'user', 'password': 'pass'}).
        :param follow_redirects: If True, the request will automatically follow redirects.
        :param log_redirects: If True, the client will automatically log redirects, NOTE: slows down execution time
        :param post_redirect_get: If True, the request will automatically convert redirected POST requests into GET
        requests.
        :param accept_errors: If True, the request will not raise exceptions for HTTP error status codes.
        :param redirections_limit: The maximum number of redirects the request will follow.
        :param connection_timeout: The timeout for establishing a connection for this request.
        :param request_timeout: The timeout for completing this request.
        """
        request = self.request(
            method=HTTPMethod.PATCH,
            payload=payload,
            url=url,
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=params,
            query=query,
            fragment=fragment,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            log_redirects=log_redirects,
            post_redirect_get=post_redirect_get,
            accept_errors=accept_errors,
            redirections_limit=redirections_limit,
            connection_timeout=connection_timeout,
            request_timeout=request_timeout,
        )
        return request.execute()

    # Wrapper method for HEAD with default method="HEAD"
    def head(
        self,
        payload: Optional[dict] = None,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        netloc: Optional[str] = None,
        path: Optional[str] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        auth: Optional[dict] = None,
        follow_redirects: Optional[bool] = None,
        log_redirects: Optional[bool] = None,
        post_redirect_get: Optional[bool] = None,
        accept_errors: Optional[bool] = None,
        redirections_limit: Optional[int] = None,
        connection_timeout: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ):
        """
        Creates and execute `request` using "HEAD".

        :param payload: The data to send with the request (for POST or PUT requests).
        :param url: The URL for this request.
        :param scheme: The URL scheme (e.g., "http" or "https").
        :param netloc: The network location (e.g., "www.example.com").
        :param path: The URL path.
        :param params: The URL parameters.
        :param query: The URL query string.
        :param fragment: The URL fragment.
        :param headers: The headers for this request.
        :param cookies: The cookies for this request.
        :param auth: The authentication details for this request (e.g., {'username': 'user', 'password': 'pass'}).
        :param follow_redirects: If True, the request will automatically follow redirects.
        :param log_redirects: If True, the client will automatically log redirects, NOTE: slows down execution time
        :param post_redirect_get: If True, the request will automatically convert redirected POST requests into GET
        requests.
        :param accept_errors: If True, the request will not raise exceptions for HTTP error status codes.
        :param redirections_limit: The maximum number of redirects the request will follow.
        :param connection_timeout: The timeout for establishing a connection for this request.
        :param request_timeout: The timeout for completing this request.
        """
        request = self.request(
            method=HTTPMethod.HEAD,
            payload=payload,
            url=url,
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=params,
            query=query,
            fragment=fragment,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            log_redirects=log_redirects,
            post_redirect_get=post_redirect_get,
            accept_errors=accept_errors,
            redirections_limit=redirections_limit,
            connection_timeout=connection_timeout,
            request_timeout=request_timeout,
        )
        return request.execute()

    # Wrapper method for DELETE with default method="OPTIONS"
    def options(
        self,
        payload: Optional[dict] = None,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        netloc: Optional[str] = None,
        path: Optional[str] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        auth: Optional[dict] = None,
        follow_redirects: Optional[bool] = None,
        log_redirects: Optional[bool] = None,
        post_redirect_get: Optional[bool] = None,
        accept_errors: Optional[bool] = None,
        redirections_limit: Optional[int] = None,
        connection_timeout: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ):
        """
        Creates and execute `request` using "OPTIONS".

        :param payload: The data to send with the request (for POST or PUT requests).
        :param url: The URL for this request.
        :param scheme: The URL scheme (e.g., "http" or "https").
        :param netloc: The network location (e.g., "www.example.com").
        :param path: The URL path.
        :param params: The URL parameters.
        :param query: The URL query string.
        :param fragment: The URL fragment.
        :param headers: The headers for this request.
        :param cookies: The cookies for this request.
        :param auth: The authentication details for this request (e.g., {'username': 'user', 'password': 'pass'}).
        :param follow_redirects: If True, the request will automatically follow redirects.
        :param log_redirects: If True, the client will automatically log redirects, NOTE: slows down execution time
        :param post_redirect_get: If True, the request will automatically convert redirected POST requests into GET
        requests.
        :param accept_errors: If True, the request will not raise exceptions for HTTP error status codes.
        :param redirections_limit: The maximum number of redirects the request will follow.
        :param connection_timeout: The timeout for establishing a connection for this request.
        :param request_timeout: The timeout for completing this request.
        """
        request = self.request(
            method=HTTPMethod.OPTIONS,
            payload=payload,
            url=url,
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=params,
            query=query,
            fragment=fragment,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            log_redirects=log_redirects,
            post_redirect_get=post_redirect_get,
            accept_errors=accept_errors,
            redirections_limit=redirections_limit,
            connection_timeout=connection_timeout,
            request_timeout=request_timeout,
        )
        return request.execute()

    def request(
        self,
        method: HTTPMethodType,
        payload: Optional[dict] = None,
        parent_request: Optional[AnyRequest] = None,
        url: Optional[str] = None,
        scheme: Optional[str] = None,
        netloc: Optional[str] = None,
        path: Optional[str] = None,
        params: Optional[str] = None,
        query: Optional[str] = None,
        fragment: Optional[str] = None,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        auth: Optional[dict] = None,
        follow_redirects: Optional[bool] = None,
        log_redirects: Optional[bool] = None,
        post_redirect_get: Optional[bool] = None,
        accept_errors: Optional[bool] = None,
        redirections_limit: Optional[int] = None,
        connection_timeout: Optional[int] = None,
        request_timeout: Optional[int] = None,
    ):
        """
        Creates the request object with the specified parameters.

        :param method: The HTTP method for this request (e.g., "GET", "POST").
        :param payload: The data to send with the request (for POST or PUT requests).
        :param parent_request: Parent request object, usually used fot binding requests with redirections
        :param url: The URL for this request.
        :param scheme: The URL scheme (e.g., "http" or "https").
        :param netloc: The network location (e.g., "www.example.com").
        :param path: The URL path.
        :param params: The URL parameters.
        :param query: The URL query string.
        :param fragment: The URL fragment.
        :param headers: The headers for this request.
        :param cookies: The cookies for this request.
        :param auth: The authentication details for this request (e.g., {'username': 'user', 'password': 'pass'}).
        :param follow_redirects: If True, the request will automatically follow redirects.
        :param log_redirects: If True, the client will automatically log redirects, NOTE: slows down execution time
        :param post_redirect_get: If True, the request will automatically convert redirected POST requests into GET
        requests.
        :param accept_errors: If True, the request will not raise exceptions for HTTP error status codes.
        :param redirections_limit: The maximum number of redirects the request will follow.
        :param connection_timeout: The timeout for establishing a connection for this request.
        :param request_timeout: The timeout for completing this request.
        """
        return Request(
            self,
            method=method,
            payload=payload,
            url=url,
            scheme=scheme,
            netloc=netloc,
            path=path,
            params=params,
            query=query,
            fragment=fragment,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            log_redirects=log_redirects,
            post_redirect_get=post_redirect_get,
            accept_errors=accept_errors,
            redirections_limit=redirections_limit,
            connection_timeout=connection_timeout,
            request_timeout=request_timeout,
        )

    @property
    def _base_url(self):
        return urlunparse((self.scheme, self.netloc, "", "", "", ""))

    __full_name__ = _base_url
