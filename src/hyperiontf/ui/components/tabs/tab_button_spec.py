from typing import Optional

from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.button.spec import ButtonBySpec


class TabButtonBySpec(ButtonBySpec):

    def __init__(
        self,
        root: LocatorTree,
        label: Optional[LocatorTree] = None,
        close_button: Optional[LocatorTree] = None,
    ):
        super().__init__(root)
        self.label = label
        self.close_button = close_button
