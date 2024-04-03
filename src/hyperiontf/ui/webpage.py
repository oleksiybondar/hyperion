import time
from typing import Optional

from .decorators.autolog_class_method_helper import (
    auto_decorate_class_methods_with_logging,
)
from hyperiontf.logging import getLogger
from hyperiontf.typing import (
    Platform,
    LoggerSource,
    PlatformType,
    OSType,
    ViewportLabelType,
)
import platform
from .page_object_base import BasePageObject
from .content_manager import ContentManager
from .window_manager import WindowManager
from .viewport_manager import ViewportManager
from .automation_adapter_manager import AutomationAdaptersManager
from hyperiontf.configuration import config


class WebPage(BasePageObject):
    def __init__(self, automation_descriptor):
        super().__init__(automation_descriptor, getLogger(LoggerSource.WEB_PAGE))
        self.window_manager = WindowManager(self, self.logger)
        self.content_manager = ContentManager(self, self.logger)
        self.viewport_manager = ViewportManager(self, self.logger)
        auto_decorate_class_methods_with_logging(self, WebPage, self.logger)

    @property
    def viewport(self):
        return self.viewport_manager.current_viewport

    @viewport.setter
    def viewport(self, viewport: ViewportLabelType):
        self.viewport_manager.set_viewport(viewport)

    def change_viewport(self, width: int, height: Optional[int] = None) -> None:
        self.viewport_manager.resize(width, height)

    @property
    def platform(self) -> PlatformType:
        return Platform.WEB

    @property
    def os(self) -> OSType | str:
        return platform.system()

    def __resolve__(self):
        self.window_manager.activate()
        self.content_manager.resolve(self)

    @classmethod
    def start_browser(cls, caps=None, attempts: int = config.page_object.start_retries):
        try:
            return cls((AutomationAdaptersManager().create(caps)))
        except Exception as e:
            logger = getLogger(LoggerSource.WEB_PAGE)
            msg = f"Unable to start browser! {e.__class__.__name__}: {str(e)}"
            if attempts > 0:
                logger.debug(msg)
                time.sleep(config.page_object.retry_delay)
                return cls.start_browser(caps, attempts - 1)

            logger.critical(msg)
            raise e

    def open(self, url: str):
        self.logger.info(f"[{self.__full_name__}] Open '{url}' URL")
        self.automation_adapter.open(url)

    @property
    def title(self):
        title = self.automation_adapter.title
        self.logger.info(f"[{self.__full_name__}] Page title:\n{title}")
        return title
