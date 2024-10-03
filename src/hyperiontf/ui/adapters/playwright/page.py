from typing import List

from playwright.sync_api import sync_playwright


from hyperiontf.configuration import config
from hyperiontf.logging import getLogger
from hyperiontf.ui import By
from hyperiontf.typing import AutomationTool, UnsupportedLocatorException
from .map_locator import convert_locator
from .map_exception import map_exception
from .selenium_to_playwright_script import convert_to_function
from .element import Element
from .action_builder import PlaywrightActionBuilder
from hyperiontf.typing import LocatorStrategies

import base64

logger = getLogger()
adapter_logger = getLogger("PlaywrightAdapter")

if config.logger.intercept_selenium_logs:
    logger.merge_logger_stream(AutomationTool.SELENIUM)


class Page:
    playwright = None

    @staticmethod
    def start_playwright():
        if Page.playwright is None:
            Page.playwright = sync_playwright().start()

        return Page.playwright

    def __init__(self, browser, context, page):
        self.automation_type = AutomationTool.PLAYWRIGHT
        self.browser = browser
        self.context = context
        self._page = page
        self._current_context = "default"
        self._iframe = None

    @property
    def page(self):
        if self._current_context == "default":
            return self._page

        return self._iframe

    @property
    def action_builder(self) -> PlaywrightActionBuilder:
        return PlaywrightActionBuilder(self.page)

    @staticmethod
    def start_browser(browser: str, caps: dict):
        service = Page.start_playwright()

        browser_map = {
            "chromium": service.chromium.launch,
            "chrome": service.chromium.launch,
            "electron": service.chromium.launch,
            "edge": service.chromium,
            "firefox": service.firefox.launch,
            "webkit": service.webkit.launch,
            "safari": service.webkit.launch,
        }

        headless = "headless" in caps and caps["headless"]

        # Configure mobile emulation if specified
        viewport = None
        if "mobileEmulation" in caps:
            mobile_emulation = caps["mobileEmulation"]
            viewport = {
                "width": mobile_emulation["width"],
                "height": mobile_emulation["height"],
                "deviceScaleFactor": mobile_emulation.get("pixelRatio", 1.0),
            }

        browser_instance = browser_map[browser.lower()](headless=headless)
        context = browser_instance.new_context(viewport=viewport)

        # Open a new page
        page = context.new_page()

        return Page(browser_instance, context, page)

    @map_exception
    def open(self, url: str):
        self.page.goto(url)

    @property
    @map_exception
    def window_handle(self):
        return "default"

    @property
    @map_exception
    def window_handles(self):
        return [self.window_handle]

    @map_exception
    def find_element(self, locator: By) -> Element:
        playwright_locator = convert_locator(locator)
        if playwright_locator == LocatorStrategies.UNSUPPORTED:
            raise UnsupportedLocatorException(
                f"Unsupported {locator.by} locator for Playwright"
            )
        return Element(self.page.query_selector(playwright_locator), self)

    @map_exception
    def find_elements(self, locator) -> List[Element]:
        playwright_locator = convert_locator(locator)
        if playwright_locator == LocatorStrategies.UNSUPPORTED:
            raise UnsupportedLocatorException(
                f"Unsupported {locator.by} locator for Playwright"
            )

        elements = self.page.query_selector_all(playwright_locator)
        return list(map(lambda x: Element(x, self), elements))

    @map_exception
    def switch_to_iframe(self, iframe):
        # Switch to the iframe's content
        self._iframe = iframe.get_iframe_content()
        self._current_context = "iframe"

    @map_exception
    def switch_to_default_content(self):
        # Switching back to the main content is as simple as using the 'page' object again
        # Now you can use 'self.page' for actions in the main content
        self._current_context = "default"

    @map_exception
    def switch_to_window(self, handle: str):
        # Switching between windows is not needed as every page has own instance and it's managed by playwright
        pass

    @property
    @map_exception
    def title(self):
        return self.page.title()

    @property
    @map_exception
    def url(self):
        return self.page.url

    @map_exception
    def quit(self):
        self.browser.close()

    @map_exception
    def close(self):
        self.page.close()

    @map_exception
    def execute_script(self, script, *args, **kwargs):
        return self.page.evaluate(convert_to_function(script), *args, **kwargs)

    @property
    @map_exception
    def screenshot_as_base64(self):
        screenshot_as_bytes = self.page.screenshot()
        return base64.b64encode(screenshot_as_bytes).decode("utf-8")

    @map_exception
    def screenshot(self, path):
        self.page.screenshot(path=path)

    @property
    @map_exception
    def page_source(self):
        return self.page.content()

    @property
    @map_exception
    def size(self):
        adapter_logger.debug(
            "Window size getter:\nPlaywright does not actually manage window "
            "size!\nReturning viewport size instead!"
        )
        return self.page.viewport_size

    @property
    @map_exception
    def location(self):
        adapter_logger.debug(
            "Window location getter:\nPlaywright does not actually manage window "
            "location!\nReturning zero coordinate instead!"
        )
        return {"x": 0, "y": 0}

    @map_exception
    def set_window_size(self, width, height):
        adapter_logger.debug(
            "Window size setter:\nPlaywright does not actually manage window "
            "size!\nSetting viewport size instead!"
        )
        self.page.set_viewport_size({"width": width, "height": height})

    @map_exception
    def set_window_location(self, x_, y_):
        adapter_logger.warning(
            "Window location setter:\nPlaywright does not actually manage window "
            "location!\nNothing to do here!"
        )

    @map_exception
    def set_window_rect(self, x, y, width, height):
        self.set_window_location(x, y)
        self.set_window_size(width, height)

    @property
    @map_exception
    def rect(self):
        return {**self.size, **self.location}

    def dump(self):
        attachments = []

        self.switch_to_default_content()

        base_64_img_URL = f"data:image/png;base64,{self.screenshot_as_base64}"
        attachments.append(
            {"title": "Page screenshot", "type": "image", "url": base_64_img_URL}
        )

        base_64_src_url = f"data:text/html;base64,{base64.b64encode(self.page_source.encode('utf-8')).decode('utf-8')}"
        attachments.append(
            {"title": "Page source", "type": "html", "url": base_64_src_url}
        )

        return attachments
