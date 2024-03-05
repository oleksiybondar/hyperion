from selenium.webdriver import Remote
from selenium.webdriver.remote.command import Command


class WinAppDriver(Remote):
    """
    A customized Selenium Remote WebDriver class designed specifically
    for interfacing with Microsoft's WinAppDriver. This class addresses
    the compatibility issue between WinAppDriver v1.2.1 and Selenium 4
    concerning the desired capabilities format.

    As WinAppDriver v1.2.1 expects capabilities in the deprecated
    'desiredCapabilities' format, this class provides a workaround by
    allowing these capabilities to be passed directly, bypassing the
    newer capabilities structure expected by Selenium 4's standard Remote
    class.

    Note: This class is specifically tailored for the scenario where direct
    usage of Selenium 4's Remote class is not feasible with WinAppDriver
    v1.2.1 due to the capabilities format discrepancy. Future versions of
    WinAppDriver may address this issue, potentially rendering this class
    unnecessary. It's advised to check WinAppDriver's release notes for
    compatibility updates with Selenium 4.

    Usage:
        This class should be used in place of Selenium's Remote class when
        initiating a session with WinAppDriver. The custom start_session
        method ensures that the capabilities are processed in a manner
        compatible with WinAppDriver's expectations.

        By directly setting the '_caps' attribute in the ArgOptions instance,
        we bypass the normal capabilities processing of Selenium 4. This ensures
        that the options.to_capabilities() method returns the exact dictionary
        necessary for WinAppDriver, which is particularly crucial given its
        current handling of capabilities.

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
            Initiates a new session with WinAppDriver using the specified
            capabilities. Overrides the start_session method in Selenium's
            Remote class to accommodate WinAppDriver's capabilities format.
    """

    def start_session(self, capabilities: dict) -> None:
        """Creates a new session with the desired capabilities.

        :Args:
         - capabilities - a capabilities dict to start the session with.
        """
        response = self.execute(Command.NEW_SESSION, capabilities)
        self.session_id = response.get("sessionId")
        self.caps = response
