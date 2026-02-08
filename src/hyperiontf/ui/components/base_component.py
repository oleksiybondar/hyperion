from hyperiontf.logging.logger import getLogger
from hyperiontf.ui.widget import Widget


logger = getLogger("Component")


class BaseComponent(Widget):
    """
    Base class for all complex UI components.

    BaseComponent bridges the generic Widget infrastructure with
    component-specific declarative specifications.

    It ensures that:
    - the component is anchored to a valid component specification
    - the component root locator is correctly derived from that specification
    - the full specification remains available for further, component-specific
      processing (e.g. resolving slots, rows, options, panels)

    Parameters:
        parent:
            Parent widget or page object that defines the resolution context.

        locator:
            Component specification object describing the structure of the
            component (e.g. TableBySpec, DropdownBySpec, RadioGroupBySpec).

            The specification must define a `root` locator tree, which is used
            as the effective root locator for this component.

        name:
            Logical name of the component, used for diagnostics and logging.

    Notes:
        - BaseComponent does not interpret or resolve any component internals.
        - It validates the presence of a component specification and exposes it
          via `component_spec` for use by concrete component implementations.
        - The `_locator` attribute is explicitly set to the specification's
          `root` to ensure correct scoping during resolution.
    """

    def __init__(self, parent, locator, name: str):
        super().__init__(parent, locator, name)
        self.component_spec = locator
        self._locator = self.component_spec.root
        self._logger = logger
