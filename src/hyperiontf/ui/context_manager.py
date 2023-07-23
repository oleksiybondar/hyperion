import time
from hyperiontf.logging import getLogger, Logger

from hyperiontf.typing import AnyContextContainer, Context
from .automation_adapter_manager import AutomationAdaptersManager


class ContextManager:
    """
    The ContextManager class manages context switching for Native APP and WebView instances.
    """

    def __init__(
        self,
        owner: AnyContextContainer,
        logger: Logger = getLogger("PageObject"),
    ):
        """
        Initialize the ContextManager with the provided owner, logger, and current_context.

        :param owner: The WebPage or WebView instance that owns the context.
        :param logger: The logger to use for logging context switching information.
        """
        self.owner = owner
        self.adapters_manager = AutomationAdaptersManager()
        self._logger = logger
        if self._current_context is None:
            self._current_context = Context.NATIVE

    @property
    def _current_context(self):
        return self.adapters_manager.get_meta(
            self.owner.automation_adapter, "current_context"
        )

    @_current_context.setter
    def _current_context(self, context: Context):
        self.adapters_manager.set_meta(
            self.owner.automation_adapter, "current_context", context
        )

    @property
    def automation_adapter(self):
        """
        Get the automation_adapter from the owner, if available.

        :return: The automation_adapter if available, otherwise None.
        """
        if hasattr(self.owner, "automation_adapter"):
            return self.owner.automation_adapter
        return None

    def set_webview_context(self, force: bool = False):
        if self._current_context == Context.WEB and not force:
            return

        available_contexts = self._wait_for_web_context()

        if len(available_contexts) > 1:
            context = available_contexts[len(available_contexts) - 1]
            self._logger.debug(
                f"[{self.owner.__full_name__}] Switching context to '{context}' context."
            )
            self.automation_adapter.switch_to_context(context)
            self._current_context = Context.WEB
        else:
            raise Exception("No available WebView contexts")

    def set_native_context(self, force: bool = False):
        """
        Set the context to the default page context.

        This method switches back to the default context of the page or WebView.
        """
        if self._current_context == Context.NATIVE and not force:
            return

        self._logger.debug(
            f"[{self.owner.__full_name__}] Switching context to native app context."
        )
        self.automation_adapter.switch_to_context(Context.NATIVE)
        self._current_context = Context.NATIVE

    def _wait_for_web_context(self):
        start_time = time.time()
        available_contexts = []
        while time.time() - start_time < 30:
            available_contexts = self.automation_adapter.contexts
            self._logger.debug(
                f"[{self.owner.__full_name__}] Acquired available contexts: {available_contexts}"
            )

            if len(available_contexts) > 1:
                break
            time.sleep(1)

        return available_contexts
