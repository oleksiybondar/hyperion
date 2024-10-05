import requests

from hyperiontf.assertions.expectation_result import ExpectationResult
from hyperiontf.logging import getLogger
from hyperiontf.configuration import config
from hyperiontf.typing import LoggerSource, HTTPHeader
from hyperiontf.typing import AnyResponse
from hyperiontf.typing import (
    FailedHTTPRequestException,
    ExceededRedirectionLimitException,
    NotARedirectionException,
)
import json
import xml.dom.minidom
from typing import Union, Any
from hyperiontf.assertions.expect import Expect

logger = getLogger(LoggerSource.REST_CLIENT)

CONTENT_TYPE_PARSERS = {
    "application/json": json.loads,
    "xml": xml.dom.minidom.parseString,
    "html": xml.dom.minidom.parseString,
}


class Response:
    @staticmethod
    def create_response(request: Any, response: requests.Response) -> AnyResponse:
        """
        Create a response object based on the HTTP status code.

        :param request: The request object.
        :type request: AnyRequest
        :param response: The raw response object from requests library.
        :type response: requests.Response
        :return: An instance of SuccessResponse, RedirectResponse, or ErrorResponse based on the status code.
        :rtype: AnyResponse
        """
        if 200 <= response.status_code < 300:
            return SuccessResponse(request, response)
        elif 300 <= response.status_code < 400:
            return RedirectResponse(request, response)
        else:
            return ErrorResponse(request, response)

    def __init__(self, request: Any, response: requests.Response):
        """
        Initialize the Response object.

        :param request: The request object.
        :type request: AnyRequest
        :param response: The raw response object from requests library.
        :type response: requests.Response
        """
        self.request = request
        self.response = response
        self._log_or_raise()

    @property
    def client(self):
        return self.request.client

    @property
    def status(self) -> int:
        """
        Get the HTTP status code of the response.

        :return: The HTTP status code.
        :rtype: int
        """
        return self.response.status_code

    @property
    def message(self) -> str:
        """
        Get the HTTP status message of the response.

        :return: The HTTP status message.
        :rtype: str
        """
        return self.response.reason

    @property
    def raw_body(self) -> str:
        """
        Get the raw body of the response.

        :return: The raw body of the response as a string.
        :rtype: str
        """
        return self.response.text

    @property
    def logger(self):
        return self.client.logger

    @property
    def body(self) -> Union[str, dict, object]:
        """
        Get the parsed body of the response.

        If the content type is JSON or similar, it will try to parse the JSON data and return it as a dictionary.
        Otherwise, it will return the raw body as a string.

        :return: The parsed body of the response (as a dictionary for JSON content type).
        :rtype: Union[str, dict]
        """
        content_type = (
            self.response.headers.get("content-type", "").lower().split(";")[0]
        )

        parser = CONTENT_TYPE_PARSERS.get(content_type, None)

        if parser is None:
            return self.raw_body

        try:
            return parser(self.raw_body)  # type: ignore
        except (ValueError, xml.parsers.expat.ExpatError):
            return self.raw_body

    @property
    def headers(self) -> dict:
        """
        Get the headers of the response.

        :return: The headers of the response as a dictionary.
        :rtype: dict
        """
        return dict(self.response.headers)

    @property
    def cookies(self) -> dict:
        """
        Get the cookies of the response.

        :return: The cookies of the response as a dictionary.
        :rtype: dict
        """
        return dict(self.response.cookies)

    def follow_redirect(self):
        """
        Follows a single HTTP redirection.

        :raises NotARedirectionException: If the current response is not a redirection.
        :raises NotARedirectionException: If the 'Location' header is missing in the response, which is required
                                          for following a redirection.

        :return: The response from the new endpoint after following the redirection.
        :rtype: Response
        """

        if not isinstance(self, RedirectResponse):
            raise NotARedirectionException(
                f"[{self.client.__full_name__}] The 'follow_redirect' method can only be called on "
                f"responses resulting from a redirection, but the current response is not a redirection. "
                f"Current URL: {self.request.full_url}"
            )

        next_url = self.headers.get(HTTPHeader.LOCATION, None)

        if next_url is None:
            raise NotARedirectionException(
                f"[{self.client.__full_name__}] The 'Location' header is missing in the response, "
                f"which is required for following a redirection. Current URL: {self.request.full_url}"
            )

        self.logger.debug(
            f"[{self.client.__full_name__}] Following redirection to new endpoint: {next_url}"
        )

        next_request = self.client.request(
            method=self.request.method,
            url=next_url,
            parent_request=self.request,
            headers=self.request.headers,
            auth=self.request.auth,
            follow_redirects=False,
            post_redirect_get=self.request.post_redirect_get,
            accept_errors=self.request.accept_errors,
            redirections_limit=self.request.redirections_limit,
            connection_timeout=self.request.connection_timeout,
            request_timeout=self.request.request_timeout,
        )

        return next_request.execute()

    def follow_redirects(self, max_redirects: int = config.rest.redirections_limit):
        """
        Follows HTTP redirections until the final response or the maximum number of redirects is reached.

        :param max_redirects: The maximum number of redirects to follow. Defaults to the value specified in the
                              configuration.
        :type max_redirects: Optional[int]

        :raises ExceededRedirectionLimitException: If the maximum number of redirects is reached and the final
                                                   response is still a redirection.

        :return: The final response after following all the redirections.
        :rtype: Response
        """
        response = self
        redirects_left = max_redirects
        while isinstance(response, RedirectResponse) and redirects_left > 0:
            response = response.follow_redirect()
            redirects_left -= 1

        if isinstance(response, RedirectResponse):
            raise ExceededRedirectionLimitException(
                f"[{self.client.__full_name__}] The maximum number of redirects "
                f"({max_redirects}) was exceeded while following the redirect from "
                f"'{self.request.full_url}' to '{response.request.full_url}'."
            )

    def validate_json_schema(
        self, schema: Any, is_assertion: bool = True
    ) -> ExpectationResult:
        """
        Validates the response content against the provided JSON Schema.

        :param schema: The JSON Schema to validate against.
                       It can be either a JSON Schema file path or a dictionary representing the JSON Schema.
        :type schema: Union[str, dict]
        :param is_assertion: If True (default), raise an exception on failure. If False, log a message at info level.
        :type is_assertion: bool
        :return: True if the response content is valid against the JSON Schema, False otherwise (when is_assertion is False).
        :rtype: bool
        """
        return Expect(
            self.body,
            is_assertion=is_assertion,
            sender=self.client.__full_name__,
            logger=self.logger,
        ).to_match_schema(schema)

    def _generate_log_message(self) -> str:
        """
        Generate the log message for the response.

        :return: The log message for the response.
        :rtype: str
        """
        status_code = self.response.status_code
        reason = self.response.reason
        headers = self._format_headers()
        body = self._format_body()

        return (
            f"[{self.client.__full_name__}] Received response: Status: {status_code} {reason}\nHeaders:\n"
            f"{headers}\nBody:\n{body}"
        )

    def _format_body(self):
        """
        Format the body of the response.

        :return: The formatted body.
        :rtype: str
        """
        body_as_object = self.body

        if isinstance(body_as_object, dict) or isinstance(body_as_object, list):
            return json.dumps(body_as_object, indent=4)
        elif isinstance(body_as_object, xml.dom.minidom.Document):
            return body_as_object.toprettyxml()
        else:
            # For other content types, return the raw body
            return body_as_object

    def _format_headers(self):
        """
        Format the headers of the response.

        :return: The formatted headers.
        :rtype: str
        """
        headers = []
        for header, value in self.response.headers.items():
            headers.append(f"     {header}: {value}")
        return "\n".join(headers)

    def _log_or_raise(self):
        """
        Log the response or raise an exception if it's an error response.

        :raises: FailedHTTPRequestException: If the response status code is an error status and accept_errors is False.
        """
        log_message = self._generate_log_message()

        # If it's an error response, raise an exception
        if not 200 <= self.response.status_code < 300:
            if not self.request.accept_errors:
                logger.critical(log_message)
                raise FailedHTTPRequestException(log_message)

        self._log_event(log_message)

    def _log_event(self, message: str):
        """
        Logs the given event message using the logger's default event logging level

        Parameters:
        message (str): The event message to be logged
        """
        method = getattr(logger, self.client.default_event_logging_level)
        method(message)


class SuccessResponse(Response):
    pass


class RedirectResponse(Response):
    pass


class ErrorResponse(Response):
    pass
