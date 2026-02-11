from hyperiontf.ui.widget import Widget
from hyperiontf.ui.decorators.page_object_helpers import element
from hyperiontf.ui.components.radiogroup.spec import RadioGroupBySpec


class RadioItem(Widget):
    """
    A single radio option inside a ``RadioGroup``.

    This widget represents one logical radio item in the group and is designed to be
    **instantiated only by the RadioGroup implementation** as part of its internal
    item collection.

    ⚠️ Important
        ``RadioItem`` must **not** be used as a standalone widget in Page Objects.
        It relies on its parent hierarchy to access the owning ``RadioGroup`` and its
        specification (``RadioGroupBySpec``). Used outside that hierarchy it may fail
        at runtime.

    Hierarchy contract
        ``RadioItem`` expects to live under a structure like:

        - RadioGroup (owns ``component_spec``)
          - RadioItemCollection (internal collection wrapper)
            - RadioItem (this class)

        Therefore, ``RadioItem`` resolves the specification via ``self.parent.parent``.

    Spec-driven structure
        ``RadioItem`` exposes optional sub-elements defined by ``RadioGroupBySpec``:

        - ``input``: resolved from ``component_spec.input`` (may be ``None``)
        - ``label``: resolved from ``component_spec.label`` (may be ``None``)

        The consuming RadioGroup can support UIs where:
        - the input exists but is hidden or not directly clickable
        - the label is the primary click/identity target
        - the item root itself is the interaction/identity source (no input/label)

    Delegation rules (deterministic)
        - ``get_text()``:
            If a label locator is defined, text is read from the label element.
            Otherwise, text is read from the item root (``Widget.get_text``).

        - ``get_attribute()`` / ``get_style()``:
            If an input locator is defined, attribute/style is read from the input element.
            Otherwise, it is read from the item root (``Widget.get_attribute/get_style``).

        - ``click()``:
            Clicks the most appropriate target using this priority:
            1) input (if defined)
            2) label (if defined)
            3) item root (fallback)

        These rules intentionally keep Page Objects simple and allow per-project structure
        differences to be expressed only in the spec.
    """

    @property
    def component_spec(self) -> RadioGroupBySpec:
        """
        Return the owning ``RadioGroup`` specification.

        The immediate parent resolves to the internal RadioItem collection object,
        and the second parent resolves to the RadioGroup widget where the
        ``RadioGroupBySpec`` instance is stored.
        """
        return self.parent.parent.component_spec

    @element
    def input(self):
        """
        Radio input element for this item.

        The locator is provided by ``component_spec.input`` and may be ``None``.
        When the spec does not define an input locator, the consuming logic should
        treat the item root as the state/interaction source.
        """
        return self.component_spec.input

    @element
    def label(self):
        """
        Radio label element for this item.

        The locator is provided by ``component_spec.label`` and may be ``None``.
        When the spec does not define a label locator, the item root may be treated
        as the identity/text source.
        """
        return self.component_spec.label

    def get_text(self, log: bool = True) -> str:
        """
        Return the visible text for this radio item.

        If the RadioGroup spec defines a label locator, text is read from the label.
        Otherwise, falls back to reading text from the item root.
        """
        if self.component_spec.label:
            return self.label.get_text(log=log)

        return super().get_text(log=log)

    def get_attribute(self, attr_name: str, log: bool = True) -> str:
        """
        Return an attribute value for this radio item.

        If the RadioGroup spec defines an input locator, the attribute is read from
        the input element (common for native radio state/value attributes).
        Otherwise, falls back to reading from the item root.
        """
        if self.component_spec.input:
            return self.input.get_attribute(attr_name, log=log)

        return super().get_attribute(attr_name, log=log)

    def get_style(self, attr_name: str, log: bool = True) -> str:
        """
        Return a style value for this radio item.

        If the RadioGroup spec defines an input locator, the style is read from
        the input element. Otherwise, falls back to reading from the item root.
        """
        if self.component_spec.input:
            return self.input.get_style(attr_name, log=log)

        return super().get_style(attr_name, log=log)

    def click(self):
        """
        Click this radio item using the spec-defined interaction priority.

        Click target selection is deterministic:

        1) If ``component_spec.input`` is defined and visible, click the resolved input element.
        2) Else if ``component_spec.label`` is defined, click the resolved label element.
        3) Otherwise, click the item root (fallback).

        This supports:
        - native radios (input is the authoritative interaction node)
        - hidden-input patterns where the label is clickable
        - custom radios where the item root is the clickable target
        """
        if self.component_spec.input:
            if self.input.is_visible:
                return self.input.click()

        if self.component_spec.label:
            return self.label.click()

        return super().click()
