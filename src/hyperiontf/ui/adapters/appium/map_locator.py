from appium.webdriver.common.appiumby import AppiumBy
from hyperiontf.typing import LocatorStrategies

LOCATOR_STRATEGIES_MAPPING = {
    LocatorStrategies.ID: AppiumBy.ID,
    LocatorStrategies.NAME: AppiumBy.NAME,
    LocatorStrategies.CLASS_NAME: AppiumBy.CLASS_NAME,
    LocatorStrategies.CSS_SELECTOR: AppiumBy.CSS_SELECTOR,
    LocatorStrategies.XPATH: AppiumBy.XPATH,
    LocatorStrategies.TAG_NAME: AppiumBy.TAG_NAME,
    LocatorStrategies.LINK_TEXT: AppiumBy.LINK_TEXT,
    LocatorStrategies.PARTIAL_LINK_TEXT: AppiumBy.PARTIAL_LINK_TEXT,
    LocatorStrategies.IOS_CLASS_CHAINE: AppiumBy.IOS_CLASS_CHAIN,
    LocatorStrategies.IOS_PREDICATE: AppiumBy.IOS_PREDICATE,
    LocatorStrategies.ANDROID_DATA_MATCHER: AppiumBy.ANDROID_DATA_MATCHER,
    LocatorStrategies.ANDROID_UIAUTOMATOR: AppiumBy.ANDROID_UIAUTOMATOR,
    LocatorStrategies.ANDROID_VIEWTAG: AppiumBy.ANDROID_VIEWTAG,
    LocatorStrategies.ANDROID_VIEW_MATCHER: AppiumBy.ANDROID_VIEW_MATCHER,
    LocatorStrategies.WINDOWS_ACCESSIBILITY_ID: LocatorStrategies.WINDOWS_ACCESSIBILITY_ID,
}


def map_locator(hyperion_by):
    """
    Maps a Hyperion locator strategy to its corresponding Appium locator strategy.

    If a Hyperion locator strategy does not have a direct equivalent in Appium,
    it returns `LocatorStrategies.UNSUPPORTED`.

    Parameters:
        hyperion_by: The Hyperion locator strategy to be mapped.

    Returns:
        The corresponding Appium locator strategy or `LocatorStrategies.UNSUPPORTED`
        if there is no direct equivalent.
    """
    return LOCATOR_STRATEGIES_MAPPING.get(hyperion_by, LocatorStrategies.UNSUPPORTED)
