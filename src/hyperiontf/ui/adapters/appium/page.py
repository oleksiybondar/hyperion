from typing import List

from appium import webdriver

import copy

from hyperiontf.configuration import config
from hyperiontf.logging import getLogger
from hyperiontf.ui import By
from hyperiontf.typing import (
    AutomationTool,
    UnsupportedLocatorException,
    AppiumAutomationName,
    APPIUM_DEFAULT_URL,
)
from hyperiontf.typing import Context

import base64
from .map_locator import map_locator
from .map_exception import map_exception
from .element import Element
from hyperiontf.typing import LocatorStrategies
from hyperiontf.ui.adapters.selenium.action_builder import SeleniumActionBuilder

logger = getLogger()

if config.logger.intercept_selenium_logs:
    # Appium Client is plugin for  Selenium
    logger.merge_logger_stream(AutomationTool.SELENIUM)


class Page:
    def __init__(self, driver: webdriver.Remote, automation_name: AppiumAutomationName):
        self.automation_type = AutomationTool.APPIUM
        self.automation_name = automation_name
        self.driver = driver

    @staticmethod
    def launch_app(caps: dict):
        desired_cap = copy.deepcopy(caps)
        if "remote_url" in desired_cap.keys():
            hub_url = desired_cap.pop("remote_url")
        else:
            hub_url = APPIUM_DEFAULT_URL
        # just delete it as it's a framework specific
        desired_cap.pop("automation")
        automation_name = desired_cap["automationName"]

        return Page(
            webdriver.Remote(hub_url, options=Page.dict_to_options(desired_cap)),
            automation_name,
        )

    @staticmethod
    def dict_to_options(desired_caps):
        automation_name = desired_caps["automationName"]

        if automation_name == "ios":
            from appium.options.ios import XCUITestOptions

            options = XCUITestOptions()
        if automation_name == "uiautomator2":
            from appium.options.android import UiAutomator2Options

            options = UiAutomator2Options()
        if automation_name == "Mac2":
            from appium.options.mac import Mac2Options

            options = Mac2Options()
        if automation_name == "windows":
            from appium.options.windows import WindowsOptions

            options = WindowsOptions()

        options.load_capabilities(desired_caps)
        return options

    @property
    @map_exception
    def action_builder(self) -> SeleniumActionBuilder:
        return SeleniumActionBuilder(self.driver)

    @property
    @map_exception
    def window_handle(self):
        return "NATIVE_APP"

    @property
    @map_exception
    def window_handles(self):
        return [self.window_handle]

    @property
    @map_exception
    def context(self):
        return self.driver.context

    @property
    @map_exception
    def contexts(self):
        return self.driver.contexts

    @map_exception
    def open(self, app: str):
        self.driver.get(app)

    @map_exception
    def find_element(self, locator: By) -> Element:
        selenium_locator = map_locator(locator.by)
        if selenium_locator == LocatorStrategies.UNSUPPORTED:
            raise UnsupportedLocatorException(
                f"Unsupported {locator.by} locator for Appium"
            )
        return Element(self.driver.find_element(selenium_locator, locator.value), self)

    @map_exception
    def find_elements(self, locator) -> List[Element]:
        selenium_locator = map_locator(locator.by)
        if selenium_locator == LocatorStrategies.UNSUPPORTED:
            raise UnsupportedLocatorException(
                f"Unsupported {locator.by} locator for Appium"
            )
        else:
            elements = self.driver.find_elements(selenium_locator, locator.value)
        return list(map(lambda x: Element(x, self), elements))

    @map_exception
    def switch_to_default_content(self):
        self.driver.switch_to.default_content()

    @map_exception
    def switch_to_iframe(self, iframe: Element):
        self.driver.switch_to.frame(iframe.element)

    @map_exception
    def switch_to_context(self, context):
        self.driver.switch_to.context(context)

    @map_exception
    def quit(self):
        self.driver.quit()

    @map_exception
    def close(self):
        self.driver.close()

    @map_exception
    def execute_script(self, script, *args, **kwargs):
        return self.driver.execute_script(script, *args, **kwargs)

    @property
    @map_exception
    def screenshot_as_base64(self):
        return self.driver.get_screenshot_as_base64()

    @map_exception
    def screenshot(self, path):
        screenshot_as_bytes = self.driver.get_screenshot_as_png()

        # Write the bytes to a file
        with open(path, "wb") as file:
            file.write(screenshot_as_bytes)

    @property
    @map_exception
    def page_source(self):
        return self.driver.page_source

    def dump(self):
        attachments = []
        try:
            self.switch_to_context(Context.NATIVE)
        except Exception:
            pass

        base_64_img_URL = f"data:image/png;base64,{self.screenshot_as_base64}"
        attachments.append(
            {
                "title": "Native app context screenshot",
                "type": "image",
                "url": base_64_img_URL,
            }
        )

        base_64_src_url = f"data:text/xml;base64,{base64.b64encode(self.page_source.encode('utf-8')).decode('utf-8')}"
        attachments.append(
            {
                "title": "Native app context page source",
                "type": "html",
                "url": base_64_src_url,
            }
        )

        return attachments

    @property
    @map_exception
    def size(self):
        return self.driver.get_window_size()

    @property
    @map_exception
    def location(self):
        return self.driver.get_window_position()

    @property
    @map_exception
    def rect(self):
        return self.driver.get_window_rect()

    @map_exception
    def set_window_size(self, width, height):
        self.driver.set_window_size(width, height)

    @map_exception
    def set_window_location(self, x, y):
        self.driver.set_window_position(x, y)

    @map_exception
    def set_window_rect(self, x, y, width, height):
        self.driver.set_window_rect(x, y, width, height)
