from hyperiontf.logging import getLogger
from hyperiontf.typing import NoSuchElementException
from .element import Element
from .locatable import LocatableElement
from .by import By
from hyperiontf.typing import LocatorStrategies

logger = getLogger("Element")


class Elements(LocatableElement):
    def __init__(self, parent, locator, name, item_class=Element):
        super().__init__(parent, locator, name)
        self._item_class = item_class
        self._elements_cache = []

    def is_interactive(self):
        if self.element_adapter is NoSuchElementException:
            raise self.element_adapter

    @property
    def _elements(self):
        if len(self.element_adapter) != len(self._elements_cache):
            self._cache_elements()

        return self._elements_cache

    def _cache_elements(self):
        i = 0
        self._elements_cache = []
        while i < len(self.element_adapter):
            item = self._item_class(
                self, By(LocatorStrategies.ELEMENTS_ITEM, str(i)), str(i)
            )
            self._elements_cache.append(item)
            i += 1

    def __len__(self):
        return len(self.element_adapter)

    def __getitem__(self, index):
        return self._elements[index]

    def __iter__(self):
        return iter(self._elements)

    def __contains__(self, item):
        return item in self._elements

    def index(self, item):
        return self._elements.index(item)

    def count(self, item):
        return self._elements.count(item)

    def sort(self, key=None, reverse=False):
        self._elements.sort(key=key, reverse=reverse)
