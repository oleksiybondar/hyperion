from typing import Optional

from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.typing import (
    MenuActivator,
    MenuActivatorType,
    AUTO_SELECT,
)


class MenuLevelBySpec:

    def __init__(
        self,
        options: LocatorTree,
        label: Optional[LocatorTree] = None,
        value_attribute: Optional[str] = AUTO_SELECT,
        option_label: Optional[LocatorTree] = None,
        activator: MenuActivatorType = MenuActivator.CLICK,
    ):
        self.label = label
        self.options = options
        self.value_attribute = value_attribute
        self.option_label = option_label
        self.activator = activator
