from hyperiontf.logging import getLogger
from .element import Element
from .decorators.autolog_class_method_helper import (
    auto_decorate_class_methods_with_logging,
)

logger = getLogger("Element")


class Widget(Element):
    def __init__(self, parent, locator, name):
        super().__init__(parent, locator, name)
        auto_decorate_class_methods_with_logging(self, Widget, logger)
