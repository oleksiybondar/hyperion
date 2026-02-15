from .slot_policy_rule import SlotPolicyRule
from .button.spec import ButtonBySpec
from .dropdown.spec import DropdownBySpec
from .radiogroup.spec import RadioGroupBySpec
from .table.spec import TableBySpec
from .tabs.spec import TabsBySpec

from .button.button import Button
from .dropdown.dropdown import Dropdown
from .radiogroup.radigroup import Radiogroup
from .table.table import Table
from .tabs.tabs import Tabs

from .decorators.page_object_helpers import button, dropdown, radiogroup, table

__all__ = [
    "SlotPolicyRule",
    "ButtonBySpec",
    "DropdownBySpec",
    "RadioGroupBySpec",
    "TableBySpec",
    "TabsBySpec",
    "Button",
    "Dropdown",
    "Radiogroup",
    "button",
    "dropdown",
    "radiogroup",
    "table",
    "Table",
    "tabs",
    "Tabs",
]
