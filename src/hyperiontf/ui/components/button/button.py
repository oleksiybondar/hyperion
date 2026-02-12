from hyperiontf.ui.components.base_component import BaseComponent
from hyperiontf.ui.decorators.page_object_helpers import element


class Button(BaseComponent):
    """
    Base component for clickable, button-like UI elements.

    Button provides a common abstraction for components whose interaction
    target and visible label may not be the same element.

    It supports scenarios where:
    - the clickable container exposes no meaningful text
    - the visible label is rendered by a nested element
    - automation backends report text inconsistently across platforms

    When a label locator is defined in the component specification, Button
    uses it as the authoritative text source. Otherwise, it falls back to
    the default Widget text resolution behavior.
    """

    @element
    def button_label(self):
        """
        Resolve the label element for the button.

        This element is used as the text and identity source when a label
        locator is provided in the component specification.
        """
        return self.component_spec.label

    def get_text(self, log: bool = True) -> str:
        """
        Return the visible text associated with the button.

        Resolution strategy:
        - If a label locator is defined in the component specification,
          text is resolved from the label element.
        - Otherwise, text resolution falls back to the default behavior
          implemented by the parent Widget class.

        Parameters:
            log:
                Whether to emit diagnostic logging during text resolution.

        Returns:
            The resolved button text.
        """
        if self.component_spec.label:
            return self.button_label.get_text(log=log)

        return super().get_text(log=log)
