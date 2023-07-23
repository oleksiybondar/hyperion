from hyperiontf.ui.by import By
from hyperiontf.typing import LocatorStrategies


def convert_locator(hyperion_by: By):
    if hyperion_by.by == LocatorStrategies.ID:
        return f"#{hyperion_by.value}"
    if hyperion_by.by == LocatorStrategies.NAME:
        return f"[name='{hyperion_by.value}]'"
    if hyperion_by.by == LocatorStrategies.CLASS_NAME:
        return f".{'.'.join(hyperion_by.value.split(' '))}"
    if hyperion_by.by == LocatorStrategies.CSS_SELECTOR:
        return hyperion_by.value
    if hyperion_by.by == LocatorStrategies.XPATH:
        return f"xpath={hyperion_by.value}"
    if hyperion_by.by == LocatorStrategies.TAG_NAME:
        return hyperion_by.value
    if hyperion_by.by == LocatorStrategies.TEST_ID:
        return f"[data-testid='{hyperion_by.value}']"
    if hyperion_by.by == LocatorStrategies.LINK_TEXT:
        return f"text={hyperion_by.value}"

    # No equivalent found, returning unsupported
    return LocatorStrategies.UNSUPPORTED
