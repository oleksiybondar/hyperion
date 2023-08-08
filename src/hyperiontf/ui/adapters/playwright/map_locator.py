from hyperiontf.ui.by import By
from hyperiontf.typing import LocatorStrategies

LOCATOR_TO_PLAYWRIGHT_TEMPLATE = {
    LocatorStrategies.ID: "#{}",
    LocatorStrategies.NAME: "[name='{}']",
    LocatorStrategies.CLASS_NAME: "extra-processing",
    LocatorStrategies.CSS_SELECTOR: "{}",
    LocatorStrategies.XPATH: "xpath={}",
    LocatorStrategies.TAG_NAME: "{}",
    LocatorStrategies.TEST_ID: "[data-testid='{}']",
    LocatorStrategies.LINK_TEXT: "text={}",
}


def _process_class_name(value):
    """
    Processes a CLASS_NAME value for conversion to a Playwright-compatible locator.

    It converts a class name with spaces into a Playwright-compatible class selector.

    Parameters:
        value (str): The class name value to be processed.

    Returns:
        str: A Playwright-compatible class selector.
    """
    return "." + ".".join(value.split(" "))


def convert_locator(hyperion_by: By):
    """
    Converts a Selenium locator object into a Playwright-compatible locator string.

    Utilizes a mapping of Selenium locator strategies to Playwright locator templates.
    Special processing is applied for CLASS_NAME locators.

    Parameters:
        hyperion_by (By): The Selenium locator object.

    Returns:
        str: The converted Playwright-compatible locator string or
             LocatorStrategies.UNSUPPORTED if no equivalent is found.
    """
    template = LOCATOR_TO_PLAYWRIGHT_TEMPLATE.get(
        hyperion_by.by, LocatorStrategies.UNSUPPORTED
    )

    if template == "extra-processing":
        return _process_class_name(hyperion_by.value)

    if template == LocatorStrategies.UNSUPPORTED:
        return LocatorStrategies.UNSUPPORTED

    return template.format(hyperion_by.value)
