from hyperiontf.typing import (
    StaleElementReferenceException,
    UnknownUIException,
    HyperionUIException,
)

STALE_ELEMENT_ERROR_MESSAGES = [
    "Element is not attached to the DOM",
    "Frame was detached",  # older < 1.46.0 playwright versions
    "ElementHandle.evaluate: Frame was detached",  # newer >= 1.46.0  playwright versions
    "ElementHandle.evaluate: Execution context was destroyed, most likely because of a navigation",  # newer >= 1.46.0  playwright versions
    "Execution context was destroyed, most likely because of a navigation",  # older < 1.46.0 playwright versions
]


def map_exception(method):
    def decorator(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except Exception as pwe:
            # re-raise if already a HyperonException
            if isinstance(pwe, HyperionUIException):
                raise pwe

            error_message = str(pwe)
            msg = f"[Playwright] {pwe.__class__.__name__}: {error_message}"
            # TODO: process exception
            if error_message in STALE_ELEMENT_ERROR_MESSAGES:
                raise StaleElementReferenceException(msg)

            raise UnknownUIException(msg)

    return decorator


# isConnected
