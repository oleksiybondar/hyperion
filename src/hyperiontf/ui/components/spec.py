from typing import Optional

from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.typing import SlotPolicyType


class ComponentSpec:
    """
    Base specification object for complex UI components.

    ComponentSpec defines the minimal, shared structure required to describe
    a reusable UI component in a declarative manner.
    """

    def __init__(
        self, root: LocatorTree, slot_policies: Optional[SlotPolicyType] = None
    ):
        self.root = root
        self.slot_policies = slot_policies if slot_policies else []
