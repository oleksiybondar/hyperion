from selenium.webdriver import Remote
from selenium.webdriver.remote.command import Command


class WinAppDriver(Remote):
    """
    A customized Selenium Remote WebDriver class designed specifically for interfacing with
    Microsoft's WinAppDriver. This class addresses compatibility issues between WinAppDriver v1.2.1
    and Selenium 4, focusing on both the desired capabilities format and element identifier differences.

    The main enhancements include:
    1. Adjusting the capabilities format to adhere to WinAppDriver v1.2.1 expectations, which relies
       on the deprecated 'desiredCapabilities' structure.
    2. Extending the response processing logic to handle WinAppDriver-specific element identifiers,
       ensuring that element references ("ELEMENT" keys) are properly recognized and processed.

    These modifications ensure that the WebDriver client can communicate effectively with WinAppDriver,
    maintaining compatibility without requiring alterations to existing Selenium-based test scripts.

    Note: This class is specifically tailored for scenarios where the direct usage of Selenium 4's
    Remote class is not feasible with WinAppDriver v1.2.1 due to discrepancies in capabilities format
    and element identification. It is recommended to monitor WinAppDriver's updates for any changes
    that might affect this custom implementation.

    Usage:
        Similar to the standard Remote class, with the addition that this class should be utilized
        when interacting with WinAppDriver. The customized start_session method and enhanced
        _unwrap_value processing cater to WinAppDriver's unique requirements.

    Example:
        caps = {'desiredCapabilities': {'app': 'Root'}}
        options = ArgOptions()
        setattr(options, '_caps', caps)

        drv = WinAppDriver(command_executor='http://127.0.0.1:4723',
                           options=options)

    Attributes:
        Inherits all attributes from the selenium.webdriver.Remote class.

    Methods:
        start_session(capabilities: dict) -> None:
            Initiates a new session with WinAppDriver using the specified capabilities.

        _unwrap_value(value: dict or list) -> dict or list:
            Enhances value unwrapping to accommodate WinAppDriver-specific element identifiers.
    """

    def start_session(self, capabilities: dict) -> None:
        """Creates a new session with the desired capabilities.

        :Args:
         - capabilities - a capabilities dict to start the session with.
        """
        response = self.execute(Command.NEW_SESSION, capabilities)
        self.session_id = response.get("sessionId")
        self.caps = response

    def _unwrap_value(self, value):
        """
        Extends the base _unwrap_value method to handle potential WinAppDriver-specific element identifiers.

        This method retains the original logic of unwrapping values but adds a check for the "ELEMENT" key
        within the result, addressing a WinAppDriver-specific response scenario. If the superclass method
        has already processed the value successfully without identifying an "ELEMENT" key, this method will
        simply return that result. However, if the "ELEMENT" key is detected within the resultant dictionary,
        it suggests that the response is specific to WinAppDriver, and a WebElement instance is created and
        returned using this key.

        The enhancement ensures compatibility with responses where WinAppDriver uniquely identifies elements,
        seamlessly integrating this with the standard WebDriver protocol.

        :param value: The original value to be unwrapped, potentially containing nested element identifiers.
        :type value: dict or list

        :return: The unwrapped value, with any WinAppDriver-specific element identifiers processed accordingly.
        :rtype: The same type as the input 'value' (dict, list, or the base type if neither).

        Note: This method should not be invoked directly; it is internally utilized by the WinAppDriver class
        to process and normalize responses.
        """
        result = super()._unwrap_value(value)

        if isinstance(result, dict) and "ELEMENT" in result:
            return self.create_web_element(result["ELEMENT"])

        return result
