from typing import List, Any

from selenium import webdriver
from selenium.webdriver.common.by import By as SeleniumBy

from hyperiontf.configuration import config
from hyperiontf.logging import getLogger
from hyperiontf.ui import By
from hyperiontf.typing import Browser, AutomationTool, UnsupportedLocatorException
from .map_locator import map_locator
from .map_exception import map_exception
from .element import Element

from hyperiontf.typing import LocatorStrategies

import base64

logger = getLogger()

if config.logger.intercept_selenium_logs:
    logger.merge_logger_stream(AutomationTool.SELENIUM)


class Page:
    chrome_driver = None
    firefox_driver = None
    edge_driver = None

    @staticmethod
    def get_chrome_driver_bin():
        if Page.chrome_driver is not None:
            return Page.chrome_driver

        from webdriver_manager.chrome import ChromeDriverManager

        Page.chrome_driver = ChromeDriverManager().install()

        return Page.chrome_driver

    @staticmethod
    def get_firefox_driver_bin():
        if Page.firefox_driver is not None:
            return Page.firefox_driver

        from webdriver_manager.firefox import GeckoDriverManager

        Page.firefox_driver = GeckoDriverManager().install()

        return Page.firefox_driver

    @staticmethod
    def get_edge_driver_bin():
        if Page.edge_driver is not None:
            return Page.edge_driver

        from webdriver_manager.microsoft import EdgeChromiumDriverManager

        Page.edge_driver = EdgeChromiumDriverManager().install()

        return Page.edge_driver

    def __init__(self, driver: Any):
        self.automation_type = AutomationTool.SELENIUM
        self.driver = driver

    @staticmethod
    def start_browser(browser: str, caps: dict):
        lowered_browser = browser.lower()
        if lowered_browser == Browser.CHROME:
            from selenium.webdriver.chrome.service import Service as ChromiumService

            options = Page.process_chrome_caps(caps)
            driver = webdriver.Chrome(
                service=ChromiumService(Page.get_chrome_driver_bin()),
                options=options,
            )
        elif lowered_browser == Browser.FIREFOX:
            from selenium.webdriver.firefox.service import Service as FirefoxService

            options = Page.process_firefox_caps(caps)
            driver = webdriver.Firefox(
                service=FirefoxService(Page.get_firefox_driver_bin()), options=options
            )  # type: ignore
        elif lowered_browser == Browser.EDGE:
            from selenium.webdriver.edge.service import Service as EdgeService

            options = Page.process_edge_caps(caps)
            driver = webdriver.Edge(
                service=EdgeService(Page.get_edge_driver_bin()),
                options=options,
            )  # type: ignore
        elif lowered_browser == Browser.SAFARI:
            driver = webdriver.Safari()  # type: ignore
        elif lowered_browser == Browser.REMOTE:
            remote_caps = Page.process_remote_caps(caps)
            driver = webdriver.Remote(
                command_executor=caps["remote_url"], desired_capabilities=remote_caps
            )  # type: ignore
        else:
            raise Exception(f"Unsupported browser {browser}")

        return Page(driver)

    @staticmethod
    def process_chrome_caps(caps: dict):
        from selenium.webdriver import ChromeOptions

        chrome_options = ChromeOptions()

        return Page.process_chrome_family_caps(caps, chrome_options)

    @staticmethod
    def process_firefox_caps(caps: dict):
        from selenium.webdriver import FirefoxOptions

        firefox_options = FirefoxOptions()

        # Set headless mode if specified
        if "headless" in caps:
            firefox_options.headless = True

        return firefox_options

    @staticmethod
    def process_edge_caps(caps: dict):
        from selenium.webdriver import EdgeOptions

        edge_options = EdgeOptions()

        return Page.process_chrome_family_caps(caps, edge_options)

    @staticmethod
    def process_chrome_family_caps(caps, options):
        # Set headless mode if specified
        if "headless" in caps:
            options.add_argument("--headless")

        # Set mobile emulation if specified
        if "mobileEmulation" in caps:
            mobile_emulation = caps["mobileEmulation"]
            processed_args = {
                "deviceMetrics": {
                    "width": mobile_emulation["width"],
                    "height": mobile_emulation["height"],
                    "pixelRatio": mobile_emulation.get("pixelRatio", 1.0),
                }
            }

            options.add_experimental_option("mobileEmulation", processed_args)

        return options

    @staticmethod
    def process_remote_caps(caps):
        remote_browser = caps.get("browserName", Browser.CHROME)
        if remote_browser == Browser.CHROME:
            return Page.process_chrome_caps(caps).to_capabilities()
        elif remote_browser == Browser.FIREFOX:
            return Page.process_firefox_caps(caps).to_capabilities()
        elif remote_browser == Browser.EDGE:
            return Page.process_edge_caps(caps).to_capabilities()
        elif remote_browser == Browser.SAFARI:
            return {}

    @map_exception
    def open(self, url: str):
        self.driver.get(url)

    @property
    @map_exception
    def title(self):
        return self.driver.title

    @property
    @map_exception
    def window_handle(self):
        return self.driver.current_window_handle

    @property
    @map_exception
    def window_handles(self):
        return self.driver.window_handles

    @property
    @map_exception
    def url(self):
        return self.driver.current_url

    @map_exception
    def find_element(self, locator: By) -> Element:
        selenium_locator = map_locator(locator.by)
        if selenium_locator == LocatorStrategies.UNSUPPORTED:
            return Element(self.find_using_undefined_locator(locator), self)
        return Element(self.driver.find_element(selenium_locator, locator.value), self)

    def find_using_undefined_locator(self, locator, is_single: bool = True):
        if locator.by == LocatorStrategies.TEST_ID:
            css_locator = f"[data-testid='{locator.value}']"
            if is_single:
                return self.driver.find_element(SeleniumBy.CSS_SELECTOR, css_locator)
            else:
                return self.driver.find_elements(SeleniumBy.CSS_SELECTOR, css_locator)
        if locator.by == LocatorStrategies.SCRIPT:
            return self.driver.execute_script(locator.value)

        raise UnsupportedLocatorException(
            f"Unsupported {locator.by} locator for Appium"
        )

    @map_exception
    def find_elements(self, locator) -> List[Element]:
        selenium_locator = map_locator(locator.by)
        if selenium_locator == LocatorStrategies.UNSUPPORTED:
            elements = self.find_using_undefined_locator(locator, is_single=False)
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
    def switch_to_window(self, handle: str):
        self.driver.switch_to.window(handle)

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
        for index, window in enumerate(self.window_handles):
            self.switch_to_window(window)

            base_64_img_URL = f"data:image/png;base64,{self.screenshot_as_base64}"
            attachments.append(
                {
                    "title": f"Window {index + 1} screenshot",
                    "type": "image",
                    "url": base_64_img_URL,
                }
            )

            base_64_src_url = (
                f"data:text/html;base64,"
                f"{base64.b64encode(self.page_source.encode('utf-8')).decode('utf-8')}"
            )
            attachments.append(
                {
                    "title": f"Window {index + 1} page source",
                    "type": "html",
                    "url": base_64_src_url,
                }
            )

        return attachments
