from hyperiontf.logging import getLogger
from hyperiontf.typing import ViewportLabelType
from .decorators.autolog_class_method_helper import (
    auto_decorate_class_methods_with_logging,
)
from .locatable import LocatableElement
from .viewport_manager import ViewportManager

logger = getLogger("IFrame")


class IFrame(LocatableElement):
    def __init__(self, parent, locator, name):
        super().__init__(parent, locator, name)
        self.viewport_manager = ViewportManager(self, logger)
        auto_decorate_class_methods_with_logging(self, IFrame, logger)

    @property
    def viewport(self) -> ViewportLabelType:
        return self.viewport_manager.current_viewport

    @property
    def content_manager(self):
        return self.document_holder.content_manager

    def __resolve__(self):
        self.content_manager.resolve_content(self)
