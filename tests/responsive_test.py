import pytest
import time
from hyperiontf.executors.pytest import automatic_log_setup  # noqa: F401
from page_objects.responsive_page import ResponsivePage
from page_objects.iframe_with_responsive_elements import IframeWithResponsive

import os

dirname = os.path.dirname(__file__)
responsive_page = os.path.join(dirname, "resources/test_pages/responsive_locators.html")
responsive_page_url = f"file://{responsive_page}"
responsive_iframe = os.path.join(dirname, "resources/test_pages/responsive_iframe.html")
responsive_iframe_url = f"file://{responsive_iframe}"
selenium_caps = {"automation": "selenium"}
playwright_caps = {"automation": "playwright"}


@pytest.mark.tags("SingleElement", "text", "ResponsiveLocator")
@pytest.mark.parametrize("caps", [selenium_caps, playwright_caps])
def test_find_simple_element_using_viewport_locator_and_assert_its_text(caps):
    """
    Test finding a simple element having responsive locator and asserting its text.
    """
    page = ResponsivePage.start_browser(caps)
    page.open(responsive_page_url)
    page.responsive_element1.get_text()
    page.responsive_element2.get_text()
    page.responsive_element3.get_text()


@pytest.mark.tags("SingleElement", "text", "ResponsiveLocator", "SingleIframe")
@pytest.mark.parametrize("caps", [selenium_caps, playwright_caps])
def test_find_simple_element_in_iframe_using_viewport_locator_and_assert_its_text(caps):
    """
    Test finding a simple element having responsive locator inside iframe and asserting its text.
    """
    page = IframeWithResponsive.start_browser(caps)
    page.open(responsive_iframe_url)
    page.xxl_button.click()
    time.sleep(1)
    page.iframe.responsive_element1.get_text()
    page.iframe.responsive_element2.get_text()
    page.iframe.responsive_element3.get_text()
