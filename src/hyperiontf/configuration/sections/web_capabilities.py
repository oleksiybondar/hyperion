from ..capabilities import Capabilities
import platform


class WebCapabilities(Capabilities):
    """
    Represents the [web_capabilities] section in the config.
    """

    def __init__(self):
        self.automation = "selenium"
        self.browser = self.get_default_browser()
        self.headless = True

    @staticmethod
    def get_default_browser():
        """
        Get the default browser based on the operating system.

        Returns:
            str: The default browser name.
        """
        os_name = platform.system()
        if os_name == "Windows":
            return "edge"
        elif os_name == "Linux":
            return "firefox"
        elif os_name == "Darwin":
            return "safari"
        else:
            return "chrome"
