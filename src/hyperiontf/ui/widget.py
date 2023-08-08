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

    def __resolve_eql_chain__(self, chain):
        if not self.__is_present__():
            return None

        if chain[0].get("type", None) == "attribute" or len(chain) == 1:
            return super().__resolve_eql_chain__(chain)

        child_element = getattr(self, chain[0]["name"], None)

        if child_element is None:
            return None

        return child_element.__resolve_eql_chain__(chain[1:])
