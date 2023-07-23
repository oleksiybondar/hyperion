import time

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
from hyperiontf.logging import getLogger

from hyperiontf.typing import LoggerSource, HTTPMethodType
from hyperiontf.typing import AuthType, TokenType, ContentType, HTTPHeader
from hyperiontf.typing import AnyResponse, AnyRequest
from hyperiontf.typing import ConnectionErrorException
from typing import Optional, Union, Any
from urllib.parse import urlparse, urlunparse
from .response import Response
import json

logger = getLogger(LoggerSource.REST_CLIENT)


class Request:
    def __init__(
        self,
        client: Any,
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
        Initializes the request object with the specified parameters.

        :param client: The client that this request belongs to.
        :type client: AnyClient
        :param method: The HTTP method for this request (e.g., "GET", "POST").
        :type method: HTTPMethod
        :param payload: The data to send with the request (for POST or PUT requests).
        :type payload: Optional[dict]
        :param parent_request: The request that this request is based on (for following redirects or dependent requests).
        :type parent_request: Optional[AnyRequest]
        :param url: The URL for this request.
        :type url: str
        :param scheme: The URL scheme (e.g., "http" or "https").
        :type scheme: str
        :param netloc: The network location (e.g., "www.example.com").
        :type netloc: str
        :param path: The URL path.
        :type path: str
        :param params: The URL parameters.
        :type params: str
        :param query: The URL query string.
        :type query: str
        :param fragment: The URL fragment.
        :type fragment: str
        :param headers: The headers for this request.
        :type headers: Optional[dict]
        :param cookies: The cookies for this request.
        :type cookies: Optional[dict]
        :param auth: The authentication details for this request (e.g., {'username': 'user', 'password': 'pass'}).
        :type auth: Optional[dict]
        :param follow_redirects: If True, the request will automatically follow redirects.
        :type follow_redirects: bool
        :param log_redirects: If True, the client will automatically log redirects. NOTE: slows down execution time.
        :type log_redirects: bool
        :param post_redirect_get: If True, the request will automatically convert redirected POST requests into GET requests.
        :type post_redirect_get: bool
        :param accept_errors: If True, the request will not raise exceptions for HTTP error status codes.
        :type accept_errors: bool
        :param redirections_limit: The maximum number of redirects the request will follow.
        :type redirections_limit: int
        :param connection_timeout: The timeout for establishing a connection for this request.
        :type connection_timeout: int
        :param request_timeout: The timeout for completing this request.
        :type request_timeout: int
        """
        # Implementation...
        self.client = client
        self.method = method
        self.payload = payload
        self.parent_request = parent_request

        if url:
            # Parse url
            url_parts = urlparse(url)
            self.scheme = url_parts.scheme
            self.netloc = url_parts.netloc
            self.path = url_parts.path
            self.params = url_parts.params
            self.query = url_parts.query
            self.fragment = url_parts.fragment
        else:
            self.scheme = scheme or self.client.scheme
            self.netloc = netloc or self.client.netloc
            self.path = path or self.client.path
            self.params = params or self.client.params
            self.query = query or self.client.query
            self.fragment = fragment or self.client.fragment

        self.headers = (
            {**self.client.headers, **headers}
            if headers
            else self.client.headers.copy()
        )
        self.cookies = (
            {**self.client.cookies, **cookies}
            if cookies
            else self.client.cookies.copy()
        )
        self.auth = {**self.client.auth, **auth} if auth else self.client.auth.copy()
        self.follow_redirects = (
            follow_redirects
            if follow_redirects is not None
            else self.client.follow_redirects
        )
        self.log_redirects = (
            log_redirects if log_redirects is not None else self.client.log_redirects
        )
        self.post_redirect_get = (
            post_redirect_get
            if post_redirect_get is not None
            else self.client.post_redirect_get
        )
        self.accept_errors = (
            accept_errors if accept_errors is not None else self.client.accept_errors
        )
        self.redirections_limit = (
            redirections_limit
            if redirections_limit is not None
            else self.client.redirections_limit
        )
        self.connection_timeout = (
            connection_timeout
            if connection_timeout is not None
            else self.client.connection_timeout
        )
        self.request_timeout = (
            request_timeout
            if request_timeout is not None
            else self.client.request_timeout
        )

        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None

    def execute(self) -> AnyResponse:
        """
        Executes the request and returns the response.

        :return: The response from the server.
        :rtype: requests.Response
        """
        request_params = self._prepare_request_params()

        self._log_request(request_params)
        # Make the request
        self.start_time = time.time()

        try:
            raw_response = self._session.request(**request_params)
        except requests.exceptions.RequestException as e:
            raise ConnectionErrorException(
                f"[{self.client.__full_name__}] An error occurred while making the HTTP request: {str(e)}"
            )

        self.end_time = time.time()
        response = Response.create_response(self, raw_response)

        # If there are files in the payload, close them after the request is made
        self._close_file_streams(request_params)

        if self.log_redirects and self.follow_redirects:
            return response.follow_redirects()

        return response

    @property
    def full_url(self) -> str:
        """
        Returns the full URL for the request.

        :return: The full URL.
        :rtype: str
        """
        return urlunparse(
            (
                self.scheme,
                self.netloc,
                self.path,
                self.params,
                self.query,
                self.fragment,
            )
        )

    @property
    def _base_url(self) -> str:
        """
        Returns the base URL for the request.

        :return: The base URL.
        :rtype: str
        """
        return urlunparse((self.scheme, self.netloc, "", "", "", ""))

    @property
    def _session(self) -> Union[requests.Session, Any]:
        """
        Returns the appropriate HTTP session for the request.
        If the scheme and netloc match the client's, the client's session is returned.
        Otherwise, the default requests session is returned.

        :return: The HTTP session.
        :rtype: Union[requests.Session, requests]
        """
        if self.scheme == self.client.scheme and self.netloc == self.client.netloc:
            return self.client.session
        else:
            return requests

    def _prepare_request_params(self) -> dict:
        """
        Prepares the request parameters for making the HTTP request.

        :return: The prepared request parameters.
        :rtype: dict
        """
        request_params = self._create_base_request_params()

        # Process authentication
        self._process_auth(request_params)

        # Process payload and update headers if needed
        self._process_payload(request_params)

        # Update request parameters dictionary with cookies and headers
        self._update_request_params_with_cookies_and_headers(request_params)

        return request_params

    def _create_base_request_params(self) -> dict:
        """
        Creates the base request parameters.

        :return: The base request parameters.
        :rtype: dict
        """
        allow_redirects = self.follow_redirects and not self.log_redirects

        request_params = {
            "method": self.method,
            "url": self.full_url,
            "timeout": (self.connection_timeout, self.request_timeout),
            "allow_redirects": allow_redirects,
            "stream": True,
        }
        return request_params

    def _process_auth(self, request_params: dict):
        """
        Process the authentication details and update the request parameters accordingly.

        :param request_params: The request parameters to be updated.
        :type request_params: dict
        """
        if self.auth:
            auth_type = self.auth.get("auth_type", None)
            if auth_type == AuthType.BASIC:
                request_params["auth"] = HTTPBasicAuth(
                    self.auth["username"], self.auth["password"]
                )
            elif auth_type == AuthType.DIGEST:
                request_params["auth"] = HTTPDigestAuth(
                    self.auth["username"], self.auth["password"]
                )
            elif auth_type in (AuthType.OAUTH, AuthType.JWT):
                token_type = self.auth.get("token_type", TokenType.BEARER)
                auth_header = f"{token_type} {self.auth['token']}"
                self.headers[HTTPHeader.AUTHORIZATION] = auth_header

    def _process_payload(self, request_params: dict):
        """
        Process the payload and update headers if needed.

        :param request_params: The request parameters to be updated.
        :type request_params: dict
        """
        if not self.payload:
            return

        files = self._extract_files_from_payload()

        # Check if content type needs to be updated
        if HTTPHeader.CONTENT_TYPE not in self.headers:
            if isinstance(self.payload, (dict, list)):
                self.headers[HTTPHeader.CONTENT_TYPE] = ContentType.JSON
                request_params["data"] = json.dumps(self.payload)
            elif files:
                request_params["files"] = files
            else:
                self.headers[HTTPHeader.CONTENT_TYPE] = ContentType.FORM_URLENCODED
                request_params["data"] = self.payload

    def _extract_files_from_payload(self) -> Optional[dict]:
        """
        Extracts files from the payload.

        :return: A dictionary of files extracted from the payload.
        :rtype: Optional[dict]
        """
        if not self.payload:
            return None

        files = {}

        if isinstance(self.payload, dict):
            for key, value in self.payload.items():
                if isinstance(value, dict) and "file" in value:
                    # File-like object found in the payload
                    file_name = value.get("file_name", None)
                    file_type = value.get("file_type", None)
                    if file_name and file_type:
                        files[key] = (file_name, value["file"], file_type)
                    else:
                        files[key] = value["file"]

                    # Remove the file from the payload
                    self.payload[key] = value.get("file_name", "")

        return files

    def _update_request_params_with_cookies_and_headers(self, request_params: dict):
        """
        Updates the request parameters dictionary with cookies and headers.

        :param request_params: The request parameters to be updated.
        :type request_params: dict
        """
        if self.cookies:
            request_params["cookies"] = self.cookies
        if self.headers:
            request_params["headers"] = self.headers

    @staticmethod
    def _close_file_streams(request_params: dict):
        """
        Closes file streams if there are files in the payload.

        :param request_params: The request parameters.
        :type request_params: dict
        """
        # If there are files in the payload, close them after the request is made
        if "files" not in request_params:
            return

        for file_obj in request_params["files"].values():
            if hasattr(file_obj, "close"):
                file_obj.close()

    def _log_request(self, request_params: dict):
        """
        Logs the details of the HTTP request.

        This method generates a cURL command based on the provided request parameters and logs the details of the request
        including the method, URL, and cURL command.

        :param request_params: The request parameters for the HTTP request.
        :type request_params: dict
        """
        curl_command = self._generate_curl_command(request_params)

        logger.info(
            f"[{self.client.__full_name__}] Performing {self.method} call to {self.full_url}\n{curl_command}"
        )

    @staticmethod
    def _generate_curl_command(request_params: dict) -> str:
        """
        Generates a cURL command based on the request parameters.

        :param request_params: The request parameters.
        :type request_params: dict
        :return: The cURL command.
        :rtype: str
        """
        curl_command = f"curl -X {request_params['method']} '{request_params['url']}'"

        if "headers" in request_params:
            for key, value in request_params["headers"].items():
                curl_command += f" -H '{key}: {value}'"

        if "data" in request_params:
            data = request_params["data"]
            if isinstance(data, dict) or isinstance(data, list):
                # For JSON data, format it as a single line and use single quotes
                data = str(data).replace("'", r"'\''")
                curl_command += f" -d '{data}'"
            else:
                # For other data types, use double quotes
                curl_command += f' -d "{data}"'

        if "files" in request_params:
            files = request_params["files"]
            for key, value in files.items():
                if isinstance(value, str):
                    # File path provided, use it directly
                    curl_command += f" -F '{key}=@{value}'"
                elif isinstance(value, tuple):
                    # File content provided as tuple (filename, content)
                    filename, content = value
                    curl_command += f" -F '{key}=@{filename};type={content}'"

        return curl_command
