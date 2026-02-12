from typing import Callable, Any

from hyperiontf.typing import LocatorStrategies
from hyperiontf.ui.by import By
from hyperiontf.ui.element import Element
from hyperiontf.ui.elements import Elements


class Slots(Elements):
    """
    Heterogeneous collection of UI items resolved through slot policies.

    ``Slots`` behaves like a normal :class:`Elements` collection but allows each
    position in the collection to be materialized as a different wrapper class
    (e.g. Element, Widget, Component). The final class for each index is
    determined at runtime using the parent component's ``slot_resolver``.

    Resolution process
    ------------------
    1. A base :class:`Element` wrapper is created for each index.
    2. The slot resolver evaluates rules against the index and element.
    3. If a rule matches, the element is re-instantiated using the resolved class.
    4. The resulting instance is cached in the collection.

    This enables structured UI containers (tables, tabs, forms, etc.) to expose
    semantically meaningful objects instead of uniform elements.
    """

    @property
    def slot_resolver(self):
        """
        Retrieve the slot resolver from the parent component if available.

        The resolver is responsible for determining which wrapper class should be
        used for each slot index. If the parent does not provide a resolver,
        items remain plain :class:`Element` instances.

        Returns
        -------
        SlotRuleResolver | None
            Resolver instance provided by the parent component, or None if not defined.
        """
        if hasattr(self.parent, "slot_resolver"):
            return self.parent.slot_resolver
        return None

    def _cache_elements(self):
        """
        Populate the internal cache with materialized slot items.

        For each index in the underlying element adapter:
        - A base Element wrapper is instantiated
        - The slot resolver determines if a specialized class should be used
        - The final instance is cached

        This overrides the default homogeneous caching behavior of ``Elements``
        to support heterogeneous collections.
        """
        i = 0
        self._elements_cache = []
        total_count = len(self.element_adapter)
        while i < total_count:
            item = self._instantiate_item(i)
            final_item = self._materialize_item(i, item, total_count)
            self._elements_cache.append(final_item)
            i += 1

    def _instantiate_item(self, index: int, klass: Callable = Element):
        """
        Instantiate a wrapper object for a slot at a given index.

        Parameters
        ----------
        index:
            Position of the element in the collection.
        klass:
            Wrapper class to instantiate. Defaults to :class:`Element`.

        Returns
        -------
        Element
            Instance of ``klass`` bound to the indexed element.
        """
        return klass(self, By(LocatorStrategies.ELEMENTS_ITEM, str(index)), str(index))

    def _materialize_item(
        self, index: int, item: Element, total_count: int
    ) -> Element | Any:
        """
        Resolve and instantiate the final wrapper type for a slot.

        The slot resolver is consulted to determine whether the base element
        should be replaced with a more specific wrapper class. If a matching
        rule exists, the element is re-instantiated using the resolved class.

        Parameters
        ----------
        index:
            Position in the collection.
        item:
            Initially created Element wrapper.
        total_count:
            Total number of elements in the collection.

        Returns
        -------
        Element | Any
            The final wrapper instance. Either the original Element or a
            specialized subclass such as a Widget or Component.
        """
        klass = self.slot_resolver.resolve(index, item, total_count)
        if klass is not None:
            return self._instantiate_item(index, klass)

        return item
