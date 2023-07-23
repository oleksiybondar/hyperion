from hyperiontf.logging import getLogger
from hyperiontf.typing import LoggerSource, Platform, ViewportLabel
from .decorators.autolog_class_method_helper import (
    auto_decorate_class_methods_with_logging,
)
from .page_object_base import BasePageObject
from .viewport_manager import ViewportManager
from .window_manager import WindowManager
from .automation_adapter_manager import AutomationAdaptersManager
import platform


logger = getLogger("DesktopWindow")


class DesktopWindow(BasePageObject):
    def __init__(self, automation_descriptor):
        super().__init__(automation_descriptor, getLogger(LoggerSource.DESKTOP_SCREEN))
        self.window_manager = WindowManager(self, self.logger)
        # self.context_manager = ContextManager(self, self.logger)
        self.viewport_manager = ViewportManager(self, self.logger)
        auto_decorate_class_methods_with_logging(self, DesktopWindow, self.logger)

    @property
    def platform(self):
        return Platform.DESKTOP

    @property
    def viewport(self) -> ViewportLabel:
        return self.viewport_manager.current_viewport

    @property
    def os(self):
        return platform.system()

    def open(self, app: str):
        self.logger.info(f"[{self.__full_name__}] Open '{app}' app")
        self.automation_adapter.open(app)

    @classmethod
    def launch_app(cls, caps=None):
        return cls((AutomationAdaptersManager().create(caps)))
