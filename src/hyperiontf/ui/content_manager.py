from typing import Optional, Any
from hyperiontf.logging import getLogger, Logger

from hyperiontf.typing import (
    ContentSwitchingException,
    StaleElementReferenceException,
    DEFAULT_CONTENT,
    NoSuchElementException,
)
from hyperiontf.typing import AnyContentContainer
from .iframe import IFrame


class ContentManager:
    """
    The ContentManager class manages context switching for WebPage and Iframe instances.

    It allows switching the context to different iframes within the page.
    """

    def __init__(
        self,
        owner: AnyContentContainer,
        logger: Logger = getLogger("PageObject"),
        current_content: Optional[str] = DEFAULT_CONTENT,
    ):
        """
        Initialize the ContentManager with the provided owner, logger, and current_content.

        :param owner: The WebPage or WebView instance that owns the context.
        :param logger: The logger to use for logging context switching information.
        :param current_content: The initial current context of the manager, defaults to 'default'.
        """
        self.owner = owner
        self.current_context = current_content
        self._logger = logger

    @property
    def automation_adapter(self):
        """
        Get the automation_adapter from the owner, if available.

        :return: The automation_adapter if available, otherwise None.
        """
        if hasattr(self.owner, "automation_adapter"):
            return self.owner.automation_adapter
        return None

    def set_context(self, iframe: Any):
        """
        Set the context to the provided iframe.

        :param iframe: The IFrame instance to switch the context to.
        :raises ContextSwitchingException: If context switching fails.
        """
        # The 'element_adapter' is used to resolve element references and can trigger API calls to find elements or
        # recover from errors. To ensure the correct logging order, we first retrieve the 'element_adapter' before
        # posting a content switch message. This way, the log chronology remains accurate.
        adapter = iframe.element_adapter
        self._logger.debug(
            f"[{self.owner.__full_name__}] Switching content to '{iframe.__full_name__}' iframe."
        )
        self.automation_adapter.switch_to_iframe(adapter)
        self.current_context = iframe.__full_name__

    def set_default_context(self):
        """
        Set the context to the default page context.

        This method switches back to the default context of the page or WebView.
        """
        self._logger.debug(
            f"[{self.owner.__full_name__}] Switching content to default - page content."
        )
        self.automation_adapter.switch_to_default_content()
        self.current_context = DEFAULT_CONTENT

    def resolve_content(self, target: Any, force: bool = False):
        """
        Resolve the context to the target IFrame or default context.

        :param target: The target IFrame to resolve the context to.
        :param force: If True, forces the context to switch even if the current context is already the target.
        """
        if self.current_context == target.__full_name__ and not force:
            return

        if not isinstance(target, IFrame):
            if self.current_context == DEFAULT_CONTENT:
                return
            # If the target is not an IFrame, then traverse back to the page or WebView where the context is default.
            return self.set_default_context()

        self._try_to_resolve_context(target)

    def _try_to_resolve_context(self, target):
        try:
            self.set_context(target)
        except ContentSwitchingException as e:
            self._resolve_content_switching_error(target, e)
        except StaleElementReferenceException as e:
            self._resolve_stale_error(target, e)
        except NoSuchElementException as e:
            # An edge case occurs when a NoSuchElementException is raised for elements in a different context, or
            # they are not correctly mapped on the adapter end due to changes in message patterns in newer versions.
            # In such cases, attempt to resolve it as if it were a stale element, provided that the target element
            # was previously found. This ensures that we are not dealing with a genuine NoSuchElementException.
            if target.__is_present__():
                self._resolve_stale_error(target, e)
            else:
                raise e

    def _resolve_content_switching_error(self, target, exception):
        self._logger.debug(
            f"[{self.owner.__full_name__}] Exception Intercepted!\n{exception.__class__.__name__}: {str(exception)}"
        )
        # If an exception occurred during context switching, attempt to resolve the parent context first,
        # and then retry setting the target context.
        parent_holder = target.document_holder
        if parent_holder != target:
            parent_holder.__resolve__()
        self.set_context(target)

    def _resolve_stale_error(self, target, exception):
        self._logger.debug(
            f"[{self.owner.__full_name__}] Exception Intercepted!\n{exception.__class__.__name__}: {str(exception)}"
        )
        target.find_itself()
        target.__resolve__()

    # Define an alias for resolve_context
    resolve = resolve_content
