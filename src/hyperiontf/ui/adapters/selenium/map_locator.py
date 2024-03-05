from selenium.webdriver.common.by import By as SeleniumBy
from hyperiontf.typing import LocatorStrategies

LOCATOR_MAPPINGS = {
    LocatorStrategies.ID: SeleniumBy.ID,
    LocatorStrategies.NAME: SeleniumBy.NAME,
    LocatorStrategies.CLASS_NAME: SeleniumBy.CLASS_NAME,
    LocatorStrategies.CSS_SELECTOR: SeleniumBy.CSS_SELECTOR,
    LocatorStrategies.XPATH: SeleniumBy.XPATH,
    LocatorStrategies.TAG_NAME: SeleniumBy.TAG_NAME,
    LocatorStrategies.LINK_TEXT: SeleniumBy.LINK_TEXT,
    LocatorStrategies.PARTIAL_LINK_TEXT: SeleniumBy.PARTIAL_LINK_TEXT,
    LocatorStrategies.WINDOWS_ACCESSIBILITY_ID: LocatorStrategies.WINDOWS_ACCESSIBILITY_ID,
}


def map_locator(hyperion_by):
    """
    Maps a Hyperion locator strategy to its equivalent Selenium locator strategy.

    If there is no direct Selenium equivalent for a given Hyperion locator strategy,
    it returns `LocatorStrategies.UNSUPPORTED`.

    Parameters:
        hyperion_by: A locator strategy from Hyperion.

    Returns:
        The equivalent Selenium locator strategy or `LocatorStrategies.UNSUPPORTED`
        if there is no direct equivalent.
    """
    return LOCATOR_MAPPINGS.get(hyperion_by, LocatorStrategies.UNSUPPORTED)
