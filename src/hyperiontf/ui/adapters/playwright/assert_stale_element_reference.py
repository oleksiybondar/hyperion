from hyperiontf.typing import StaleElementReferenceException


def assert_stale_reference(method):
    """
    A decorator for handling stale element references in Playwright.

    This decorator checks if a given element is still connected to the document
    before proceeding with a method. If the element is not connected,
    it raises a StaleElementReferenceException.

    It is intended to be used for decorating methods that involve interaction
    with elements on a page, to ensure the element is still present in the DOM.

    This is particularly useful for playwright as playwright's page.query_selector
    caches element, and it does not raise stale element reference errors. Thus,
    it allows getting attributes and firing actions even though the element is
    no longer a part of the DOM. Therefore, we need to manually check and handle
    such cases.

    Note that using `page.locator` instead of `page.query_selector` would omit this
    check, but it complicates the implementation of find_element vs find_elements
    strategies in the framework.

    Args:
        method (function): The original method that this decorator wraps.

    Returns:
        function: The wrapped function which includes the stale reference check.
    """

    def wrapper(self, *args, **kwargs):
        # Before invoking the original method, evaluate if the element is connected to the document.
        if not self.element.evaluate("element => element.isConnected"):
            # If the element is not connected, raise a StaleElementReferenceException
            raise StaleElementReferenceException(
                "Element is no longer connected to a document!"
            )

        # If the element is connected, proceed with calling the original method.
        return method(self, *args, **kwargs)

    # Return the wrapped function
    return wrapper
