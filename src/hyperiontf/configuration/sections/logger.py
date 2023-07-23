from ..section import Section


class Logger(Section):
    """
    Represents the [log] section in the config.
    """

    def __init__(self):
        self.log_folder = "logs"
        self.intercept_selenium_logs = True
        self.intercept_playwright_logs = True
        self.intercept_appium_logs = True
