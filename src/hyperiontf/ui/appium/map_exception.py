from selenium.common.exceptions import WebDriverException
from hyperiontf.typing import (
    NoSuchElementException,
    StaleElementReferenceException,
    UnknownUIException,
)
from hyperiontf.typing import ContentSwitchingException
import re


def map_exception(method):
    def decorator(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except WebDriverException as wde:
            msg = f"[Selenium] {wde.__class__.__name__}: {wde.msg}"
            # TODO: process exception
            match wde.__class__.__name__:
                case "NoSuchElementException":
                    switch_pattern = "(not known in the current browsing context)|(element reference not seen before)"
                    if re.search(switch_pattern, wde.msg):
                        raise ContentSwitchingException(msg)
                    raise NoSuchElementException(msg)
                case "StaleElementReferenceException":
                    raise StaleElementReferenceException(msg)
                case "NoSuchFrameException":
                    raise ContentSwitchingException(msg)
                case _:
                    raise UnknownUIException(msg)

    return decorator
