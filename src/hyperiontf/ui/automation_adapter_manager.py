import logging
from typing import Optional

from hyperiontf.helpers.decorators.singleton import Singleton
from hyperiontf.configuration import config
from hyperiontf.logging import Logger, getLogger
from hyperiontf.typing import (
    WEB_FAMILY,
    MOBILE_FAMILY,
    DESKTOP_FAMILY,
    AutomationTool,
    LoggerSource,
)
from hyperiontf.typing import ANDROID_AUTOMATION_FAMILY, IOS_AUTOMATION_FAMILY
from hyperiontf.typing import UnsupportedAutomationTypeException


@Singleton
class AutomationAdaptersManager:
    """
    A singleton class managing automation adapters for web, mobile, and desktop apps.
    """

    def __init__(self):
        """
        Initialize an empty list of adapters.
        """
        self.adapters = []

    def quit_all(self):
        """
        Quit all applications related to adapters and clear the adapter list.
        """
        for index, adapter in enumerate(self.adapters):
            adapter["logger"].info(f"Quiting application {index + 1}")
            adapter["adapter"].quit()
        self.adapters.clear()

    def make_state_dump(self):
        for index, adapter in enumerate(self.adapters):
            attachments = adapter["adapter"].dump()
            adapter["logger"].info(
                f"Application {index + 1} post morten dumps.",
                extra={"attachments": attachments},
            )

    def create(self, caps: Optional[dict] = None):
        """
        Create an adapter based on the given capabilities. Defaults to Selenium for web automation.

        :param caps: A dictionary of capabilities.
        :return: An adapter instance.
        """
        if caps is None:
            caps = {}

        automation_type = caps.get("automation", AutomationTool.SELENIUM)
        if automation_type in WEB_FAMILY:
            return self._start_browser(caps)
        elif automation_type in MOBILE_FAMILY:
            return self._start_mobile_app(caps)
        elif automation_type in DESKTOP_FAMILY:
            return self._start_desktop_app(caps)
        else:
            raise UnsupportedAutomationTypeException(
                f"Unknown automation type: {automation_type}"
            )

    def delete(self, adapter):
        """
        Delete a specific adapter from the adapters list.

        :param adapter: The adapter to be deleted.
        """
        # Filter out instances with adapter not matching the one provided.
        self.adapters = [item for item in self.adapters if item["adapter"] != adapter]

    def _get_record(self, adapter) -> dict:
        """
        Get a specific adapter record from the adapters list.

        :param adapter: The adapter whose record is to be fetched.
        :return: A dictionary of adapter records or an empty dict if not found.
        """
        for rec in self.adapters:
            if "adapter" in rec and rec["adapter"] == adapter:
                return rec

        # Return None if no adapter found
        return {}

    def get_meta(self, adapter, key: str):
        """
        Get the meta information of a specific adapter using a key.

        :param adapter: The adapter whose meta information is to be fetched.
        :param key: The key for the meta information.
        :return: The meta information or None if not found.
        """
        return self._get_record(adapter).get(key, None)

    def set_meta(self, adapter, key: str, value):
        """
        Set the meta information of a specific adapter.

        :param adapter: The adapter whose meta information is to be set.
        :param key: The key for the meta information.
        :param value: The value to be set for the meta information.
        """
        self._get_record(adapter)[key] = value

    def _add_adapter(self, adapter, logger: Logger | logging.Logger):
        """
        Add an adapter to the adapters list.

        :param adapter: The adapter to be added.
        :param logger: The logger instance.
        """
        self.adapters.append({"adapter": adapter, "logger": logger})

    def _start_browser(self, caps: dict):
        """
        Start a browser with given capabilities.

        :param caps: A dictionary of capabilities.
        :return: The adapter instance.
        """
        final_caps = config.web_capabilities.build_caps(caps)
        browser = final_caps["browser"]
        automation_type = final_caps["automation"]
        logger = getLogger(LoggerSource.WEB_PAGE)
        logger.info(f"Start '{browser.capitalize()}' browser")
        if automation_type == AutomationTool.SELENIUM:
            from hyperiontf.ui.adapters.selenium.page import Page as seleniumAPI

            adapter = seleniumAPI.start_browser(browser, final_caps)
        elif automation_type == AutomationTool.PLAYWRIGHT:
            from hyperiontf.ui.adapters.playwright.page import Page as playwrightAPI

            adapter = playwrightAPI.start_browser(browser, final_caps)
        else:
            raise UnsupportedAutomationTypeException(
                f"Unknown automation type: {automation_type}"
            )

        self._add_adapter(adapter, logger)
        return adapter

    def _start_mobile_app(self, caps: dict):
        """
        Start a mobile app with given capabilities.

        :param caps: A dictionary of capabilities.
        :return: The adapter instance.
        """
        final_caps = config.mobile_capabilities.build_caps(caps)
        automation_type = final_caps.get("automation", AutomationTool.APPIUM)
        automation_name = final_caps["automationName"]
        if automation_type == AutomationTool.APPIUM:
            if (
                automation_name not in ANDROID_AUTOMATION_FAMILY
                and automation_name not in IOS_AUTOMATION_FAMILY
            ):
                return self._start_desktop_app(caps)
        logger = self._log_mobile_app_execution(automation_name, final_caps)
        from hyperiontf.ui.adapters.appium.page import Page as AppiumAPI

        adapter = AppiumAPI.launch_app(caps)
        self._add_adapter(adapter, logger)
        return adapter

    @staticmethod
    def _log_mobile_app_execution(automation_name, final_caps):
        app = final_caps.get("app", None)
        if app is None and automation_name in IOS_AUTOMATION_FAMILY:
            app = final_caps["bundleId"]
        else:
            app_package = final_caps["appPackage"]
            app_activity = final_caps["appActivity"]
            app = f"{app_package}.{app_activity}"
        logger = getLogger(LoggerSource.MOBILE_SCREEN)
        logger.info(f"Start '{app}' mobile application")
        return logger

    def _start_desktop_app(self, caps: dict):
        """
        Start a desktop app with given capabilities.

        :param caps: A dictionary of capabilities.
        :return: The adapter instance.
        """
        final_caps = config.desktop_capabilities.build_caps(caps)
        app = final_caps.get("app", None)
        automation_type = final_caps.get("automation", AutomationTool.APPIUM)
        logger = getLogger(LoggerSource.DESKTOP_SCREEN)
        logger.info(f"Start '{app}' desktop application")
        if automation_type == AutomationTool.WIN_APP_DRIVER:
            from hyperiontf.ui.adapters.win_app_driver.page import (
                Page as winAppDriverAPI,
            )

            adapter = winAppDriverAPI.launch_app(final_caps)
        else:
            from hyperiontf.ui.adapters.appium.page import Page as AppiumAPI

            adapter = AppiumAPI.launch_app(caps)

        self._add_adapter(adapter, logger)
        return adapter
