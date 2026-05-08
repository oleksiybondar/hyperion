from typing import List, Optional

from hyperiontf import ButtonBySpec
from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.menu.level_spec import MenuLevelBySpec
from hyperiontf.ui.components.typing import (
    AUTO_SELECT,
    MenuActivatorType,
    MenuActivator,
)


class MenuBySpec(ButtonBySpec):

    def __init__(
        self,
        root: LocatorTree,
        options: LocatorTree,
        label: Optional[LocatorTree] = None,
        value_attribute: Optional[str] = AUTO_SELECT,
        option_label: Optional[LocatorTree] = None,
        activator: MenuActivatorType = MenuActivator.CLICK,
        levels: Optional[List[MenuLevelBySpec]] = None,
    ):
        super().__init__(root, label)

        self.options = options
        self.value_attribute = value_attribute
        self.option_label = option_label
        self.activator = activator
        self.levels = levels
