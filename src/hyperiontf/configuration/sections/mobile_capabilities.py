from ..capabilities import Capabilities


class MobileCapabilities(Capabilities):
    """
    Represents the [mobile_capabilities] section in the config.
    """

    def __init__(self):
        self.automation = "appium"
        self.automation_name = "XCUITest"
        self.platform_name = "iOS"
        self.device_name = "iPhone 14"
        self.platform_version = "16.2"
        self.auto_accept_alerts = False
        self.new_command_timeout = 300
