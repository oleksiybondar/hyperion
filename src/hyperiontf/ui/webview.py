from hyperiontf.logging import getLogger
from hyperiontf.typing import (
    Platform,
    LoggerSource,
    ViewportLabelType,
    PlatformType,
)
from .decorators.autolog_class_method_helper import (
    auto_decorate_class_methods_with_logging,
)
from .locatable import LocatableElement
from .viewport_manager import ViewportManager
from .content_manager import ContentManager

logger = getLogger(LoggerSource.WEB_VIEW)


class WebView(LocatableElement):
    def __init__(self, parent, locator, name):
        super().__init__(parent, locator, name)
        # does not have own, uses parent, at least with Appium, which is currently the only supported
        self._element_adapter = self.root.automation_adapter
        self.viewport_manager = ViewportManager(self, logger)
        self.content_manager = ContentManager(self, logger)
        auto_decorate_class_methods_with_logging(self, WebView, logger)

    @property
    def platform(self) -> PlatformType:
        return Platform.WEB

    @property
    def viewport(self) -> ViewportLabelType:
        return self.viewport_manager.current_viewport

    @property
    def context_manager(self):
        return self.root.context_manager

    def find_itself(self, retries: int = 0):
        """
        WebView does not need to be searched, it will be resolved by context manager
        :param retries:
        :return:
        """
        pass

    def __resolve__(self):
        self.context_manager.set_webview_context()
        self.content_manager.resolve_content(self)

    def __resolve_eql_chain__(self, chain):
        child_element = getattr(self, chain[0]["name"], None)

        if child_element is None:
            return None

        return child_element.__resolve_eql_chain__(chain[1:])
