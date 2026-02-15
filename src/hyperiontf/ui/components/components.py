import copy

from hyperiontf import By
from hyperiontf.logging.logger import getLogger
from hyperiontf.typing import LocatorStrategies
from hyperiontf.ui.components.base_component import BaseComponent
from hyperiontf.ui.elements import Elements

logger = getLogger("Component")


class Components(Elements):
    """
    Homogeneous collection wrapper for `BaseComponent`-like items.

    ``Components`` extends :class:`Elements` for cases where each item in the
    collection must be materialized as a component object built from a *spec*
    rather than from a plain locator.

    Typical use case:
    - a Page Object method returns a component spec that describes a reusable
      component shape for each collection item
    - each indexed item is re-instantiated with a deep-copied spec
    - the copied spec root is rebound to the concrete item index

    This allows component collections to preserve spec-level behavior while
    still supporting `Elements`-style indexing/iteration semantics.
    """

    def __init__(self, parent, locator, name: str, item_class=BaseComponent):
        """
        Create a component collection bound to a component specification.

        Parameters:
            parent:
                Owning container (Page/Widget/Component).
            locator:
                Component specification object. Expected to expose `root`.
            name:
                Logical property name in the owning Page Object.
            item_class:
                Component class used to materialize each indexed item.
                Defaults to `BaseComponent`.
        """
        super().__init__(parent, locator, name, item_class)
        self.component_spec = locator
        self._locator = self.component_spec.root
        self._logger = logger

    def _cache_elements(self):
        """
        Populate cache with component instances backed by indexed specs.

        For each index in the underlying adapter:
        - clone the base component spec (`deepcopy`)
        - replace cloned spec root with `ELEMENTS_ITEM` locator for that index
        - instantiate `_item_class` with the indexed spec
        - append the component instance to `_elements_cache`

        Notes:
            Deep-copy is required to avoid shared mutable spec state across
            items in the same collection.
        """
        i = 0
        self._elements_cache = []
        while i < len(self.element_adapter):
            spec = copy.deepcopy(self.component_spec)
            spec.root = By(LocatorStrategies.ELEMENTS_ITEM, str(i))
            item = self._item_class(self, spec, str(i))
            self._elements_cache.append(item)
            i += 1
