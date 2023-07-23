from ..capabilities import Capabilities


class DesktopCapabilities(Capabilities):
    """
    Represents the [desktop_capabilities] section in the config.
    """

    def __init__(self):
        self.automation = "appium"
        self.automation_name = "Mac"
        self.platform_name = "Mac"
        self.device_name = "Mac"
        self.platform_version = ""
        self.new_command_timeout = 300
