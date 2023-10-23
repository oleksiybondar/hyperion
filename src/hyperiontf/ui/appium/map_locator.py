from appium.webdriver.common.appiumby import AppiumBy
from hyperiontf.typing import LocatorStrategies


def map_locator(hyperion_by):
    if hyperion_by == LocatorStrategies.ID:
        return AppiumBy.ID
    if hyperion_by == LocatorStrategies.NAME:
        return AppiumBy.NAME
    if hyperion_by == LocatorStrategies.CLASS_NAME:
        return AppiumBy.CLASS_NAME
    if hyperion_by == LocatorStrategies.CSS_SELECTOR:
        return AppiumBy.CSS_SELECTOR
    if hyperion_by == LocatorStrategies.XPATH:
        return AppiumBy.XPATH
    if hyperion_by == LocatorStrategies.TAG_NAME:
        return AppiumBy.TAG_NAME
    if hyperion_by == LocatorStrategies.LINK_TEXT:
        return AppiumBy.LINK_TEXT
    if hyperion_by == LocatorStrategies.PARTIAL_LINK_TEXT:
        return AppiumBy.PARTIAL_LINK_TEXT
    if hyperion_by == LocatorStrategies.IOS_CLASS_CHAINE:
        return AppiumBy.IOS_CLASS_CHAIN
    if hyperion_by == LocatorStrategies.IOS_PREDICATE:
        return AppiumBy.IOS_PREDICATE
    if hyperion_by == LocatorStrategies.ANDROID_DATA_MATCHER:
        return AppiumBy.ANDROID_DATA_MATCHER
    if hyperion_by == LocatorStrategies.ANDROID_UIAUTOMATOR:
        return AppiumBy.ANDROID_UIAUTOMATOR
    if hyperion_by == LocatorStrategies.ANDROID_VIEWTAG:
        return AppiumBy.ANDROID_VIEWTAG
    if hyperion_by == LocatorStrategies.ANDROID_VIEW_MATCHER:
        return AppiumBy.ANDROID_VIEW_MATCHER
    if hyperion_by == LocatorStrategies.WINDOWS_ACCESSIBILITY_ID:
        return LocatorStrategies.WINDOWS_ACCESSIBILITY_ID
    # no Selenium equivalents, return as is probably artificial(in Selenium's terminology) locator, returning
    # unsupported
    return LocatorStrategies.UNSUPPORTED
