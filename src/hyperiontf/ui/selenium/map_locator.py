from selenium.webdriver.common.by import By as SeleniumBy
from hyperiontf.typing import LocatorStrategies


def map_locator(hyperion_by):
    if hyperion_by == LocatorStrategies.ID:
        return SeleniumBy.ID
    if hyperion_by == LocatorStrategies.NAME:
        return SeleniumBy.NAME
    if hyperion_by == LocatorStrategies.CLASS_NAME:
        return SeleniumBy.CLASS_NAME
    if hyperion_by == LocatorStrategies.CSS_SELECTOR:
        return SeleniumBy.CSS_SELECTOR
    if hyperion_by == LocatorStrategies.XPATH:
        return SeleniumBy.XPATH
    if hyperion_by == LocatorStrategies.TAG_NAME:
        return SeleniumBy.TAG_NAME
    if hyperion_by == LocatorStrategies.LINK_TEXT:
        return SeleniumBy.LINK_TEXT
    if hyperion_by == LocatorStrategies.PARTIAL_LINK_TEXT:
        return SeleniumBy.PARTIAL_LINK_TEXT
    # no Selenium equivalents, return as is probably artificial(in Selenium's terminology) locator, returning
    # unsupported
    return LocatorStrategies.UNSUPPORTED
