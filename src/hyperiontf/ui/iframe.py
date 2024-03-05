from hyperiontf.logging import getLogger
from hyperiontf.typing import ViewportLabelType, NoSuchElementException
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

    def __is_present__(self):
        if self.element_adapter is NoSuchElementException:
            return False

        # edge case for Playwright, when by some reason exception is not risen ,the adapter instance is created with an
        # empty element
        if self.element_adapter.element is None:
            return False

        return True

    def __resolve_eql_chain__(self, chain):
        if not self.__is_present__():
            return None

        child_element = getattr(self, chain[0]["name"], None)

        if child_element is None:
            return None

        return child_element.__resolve_eql_chain__(chain[1:])
