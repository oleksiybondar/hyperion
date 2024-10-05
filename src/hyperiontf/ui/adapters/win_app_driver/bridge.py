from typing import Optional

from hyperiontf import RESTClient, getLogger
from hyperiontf.typing import LoggerSource
from hyperiontf.ui.adapters.win_app_driver.element import Element
from hyperiontf.typing import (
    NoSuchElementException,
    StaleElementReferenceException,
    ContentSwitchingException,
    UnknownUIException,
)

logger = getLogger(LoggerSource.WIN_APP_DRIVER)


class Bridge:
    def __init__(
        self, url: Optional[str] = "http://127.0.0.1", port: Optional[int] = 4723
    ):
        self.url = url
        self.port = port
        self.session_id = None
        self.client = RESTClient(
            url=f"{url}:{port}",
            accept_errors=True,
            default_event_logging_level="debug",
            logger=logger,
        )

    def execute(self, command, params, payload=None):
        """
        Execute a command by making an HTTP request using the client.

        :param command: The command to execute (e.g., commands.element.click)
        :param params: A dictionary of parameters to substitute in the endpoint URL.
        :param payload: Optional; query parameters (GET) or payload (POST/PUT).
        :return: Processed response data.
        """
        # Perform endpoint substitution using the params
        endpoint = command["endpointTemplate"].format(**params)

        # Handle GET and POST/PUT requests
        if command["method"] in ["GET", "DELETE"]:
            response = self.client.get(
                path=endpoint, query=payload
            )  # Use payload as query params
        elif command["method"] in ["POST", "PUT"]:
            response = self.client.post(
                path=endpoint, payload=payload
            )  # Use payload as request body
        else:
            raise ValueError(f"Unsupported HTTP method: {command['method']}")

        # Process the response
        return self._process_response(response)

    def _process_response(self, response):
        """
        Process the response and convert any element data into element classes.

        :param response: The raw HTTP response from the REST client.
        :return: The processed response data, converting element data as needed.
        """
        response_json = response.body
        if response_json["status"] == 0:
            return self.process_value(response_json["value"])

        self._process_error(response_json)

    def _process_error(self, response_data):
        """
        Process and map WinAppDriver errors to framework exceptions.

        :param response_data: The raw HTTP response with error details.
        :raises: Framework-specific exceptions based on the error content.
        """
        error_message = response_data.get("value", {}).get("message", "").lower()
        error_code = response_data.get("status")

        # Check for specific error types
        if self._is_no_such_element_error(error_code, error_message):
            raise NoSuchElementException(
                f"[WinAppDriver] NoSuchElementException: {error_message}"
            )

        if self._is_stale_element_error(error_message):
            raise StaleElementReferenceException(
                f"[WinAppDriver] StaleElementReferenceException: {error_message}"
            )

        if self._is_content_switching_error(error_message):
            raise ContentSwitchingException(
                f"[WinAppDriver] ContentSwitchingException: {error_message}"
            )

        # If no specific exception is matched, raise a generic UnknownUIException
        raise UnknownUIException(f"[WinAppDriver] UnknownUIException: {error_message}")

    @staticmethod
    def _is_no_such_element_error(error_code, error_message):
        """
        Check if the error is a NoSuchElementException.

        :param error_code: The error code from the response.
        :param error_message: The error message from the response.
        :return: True if the error is related to no such element, False otherwise.
        """
        return error_code == 7 or "no such element" in error_message

    @staticmethod
    def _is_stale_element_error(error_message):
        """
        Check if the error is a StaleElementReferenceException.

        :param error_message: The error message from the response.
        :return: True if the error is related to stale element reference, False otherwise.
        """
        return "stale element reference" in error_message

    @staticmethod
    def _is_content_switching_error(error_message):
        """
        Check if the error is a ContentSwitchingException.

        :param error_message: The error message from the response.
        :return: True if the error is related to content switching, False otherwise.
        """
        return "frame not found" in error_message or "window not found" in error_message

    def process_value(self, value):
        """
        Process a value and return the appropriate object based on its type.

        :param value: The value to process (could be simple type, list, or dict).
        :return: The processed value.
        """
        # Check for simple types
        if isinstance(value, (bool, int, float, str)):
            return value  # Return simple type as-is

        # Check if it's a list, then recursively process each item
        elif isinstance(value, list):
            return [self.process_value(item) for item in value]

        # Check if it's a dictionary, then process as dict
        elif isinstance(value, dict):
            return self.process_dict_value(value)

        # If the value doesn't match any known types, raise an error
        raise TypeError(f"Unsupported value type: {type(value)}")

    def process_dict_value(self, value_dict):
        """
        Process a dictionary value, handling element objects and other mappings.

        :param value_dict: The dictionary to process.
        :return: The processed dictionary or element object.
        """
        # Check if the dictionary represents an element
        element_key = self._get_element_key(value_dict)
        if element_key:
            # If it has an element identifier, return an Element object
            return self._create_element(value_dict[element_key])

        # Otherwise, recursively process each key-value pair in the dictionary
        return {key: self.process_value(val) for key, val in value_dict.items()}

    @staticmethod
    def _get_element_key(value_dict):
        """
        Check if the dictionary contains an element identifier.

        :param value_dict: The dictionary to check.
        :return: The key if it's an element, else None.
        """
        element_keys = [
            "ELEMENT",
            "element-6066-11e4-a52e-4f735466cecf",  # W3C standard and legacy key
        ]
        for key in element_keys:
            if key in value_dict:
                return key
        return None

    def _create_element(self, element_id):
        """
        Create an Element object from an element identifier.

        :param element_id: The identifier of the element.
        :return: An instance of an Element object (implementation-dependent).
        """
        return Element(element_id, self)
