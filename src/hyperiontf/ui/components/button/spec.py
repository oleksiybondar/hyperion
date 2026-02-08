from typing import Optional

from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.spec import ComponentSpec


class ButtonBySpec(ComponentSpec):
    """
    Specification object for a Button-like clickable component.

    ButtonBySpec intentionally separates:
    - the interaction target (root)
    - the identity/label source (label)

    This is required for real-world UIs where the clickable container does not
    expose meaningful text, or where the visible label is rendered by a nested
    element (common in desktop UI trees and some web structures).

    Examples of why this matters:
    - Some automation backends (e.g. desktop drivers) may report an empty text
      property for the button container even when a nested text node exists.
    - In some UI implementations, the element that receives the click event is
      not the same element that provides the accessible/visible label.
    - Accessibility and screen-reader labeling may differ from the visual click
      target, so decoupling trigger and label improves modeling flexibility.

    Parameters:
        root:
            Locator tree describing the primary clickable element (the trigger).

        label:
            Optional locator tree describing where the label/text should be
            resolved from. If omitted, the consuming component should treat the
            root element as the label source by default.
    """

    def __init__(self, root: LocatorTree, label: Optional[LocatorTree] = None):
        super().__init__(root)
        self.label = label
