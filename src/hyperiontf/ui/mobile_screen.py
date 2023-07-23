from hyperiontf.logging import getLogger
from hyperiontf.typing import LoggerSource, Platform, ViewportLabel, OS
from hyperiontf.typing import ANDROID_AUTOMATION_FAMILY
from .decorators.autolog_class_method_helper import (
    auto_decorate_class_methods_with_logging,
)
from .page_object_base import BasePageObject
from .context_manager import ContextManager
from .viewport_manager import ViewportManager
from .window_manager import WindowManager
from .automation_adapter_manager import AutomationAdaptersManager


class MobileScreen(BasePageObject):
    def __init__(self, automation_descriptor):
        super().__init__(automation_descriptor, getLogger(LoggerSource.MOBILE_SCREEN))
        self.window_manager = WindowManager(self, self.logger)
        self.context_manager = ContextManager(self, self.logger)
        self.viewport_manager = ViewportManager(self, self.logger)
        auto_decorate_class_methods_with_logging(self, MobileScreen, self.logger)

    @classmethod
    def launch_app(cls, caps=None):
        return cls((AutomationAdaptersManager().create(caps)))

    @property
    def platform(self):
        return Platform.MOBILE

    @property
    def viewport(self) -> ViewportLabel:
        return self.viewport_manager.current_viewport

    @property
    def os(self):
        if self.automation_adapter.automation_name in ANDROID_AUTOMATION_FAMILY:
            return OS.ANDROID

        return OS.IOS

    def __resolve__(self):
        self.context_manager.set_native_context()
