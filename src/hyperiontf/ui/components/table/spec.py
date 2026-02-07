from typing import Optional

from hyperiontf.typing import LocatorTree
from hyperiontf.ui.components.component_specification import ComponentSpec
from hyperiontf.ui.components.typing import SlotPolicyType


class TableBySpec(ComponentSpec):
    """
    Specification object for a Table component.

    TableBySpec describes the structural locators and slot resolution rules
    required to model a table as a reusable, declarative UI component.

    A Table consists of:
    - a logical root that scopes the table
    - a collection of rows
    - a collection of cells within each row
    - an optional collection of header cells
    - an optional slot policy that controls cell materialization

    Parameters:
        root:
            Locator tree describing the logical root of the table.
            This defines the primary resolution scope for rows and headers.

        rows:
            Locator tree describing the collection of table rows.
            Rows represent only the currently rendered rows in the DOM;
            virtualized tables are supported implicitly.

        cells:
            Locator tree describing the collection of cells within a row.
            This locator is purely structural and is used to locate the
            root element of each cell.

        header_cells:
            Optional locator tree describing the table header cells.

            This locator is expected to point directly to header cell elements
            (e.g. `thead > td` or equivalent), rather than to a header row wrapper.

            Header cells may be used by the consuming implementation to derive
            column identity or index mappings but are not required for index-based
            table access.

        slot_policy:
            Optional ordered list of slot policy rules controlling how table
            cells are materialized.

            Slot policies follow a policy-by-ordering model:
            rules are evaluated in order, and the last matching rule wins.

    Notes:
        - TableBySpec is a declarative description only; it performs no DOM
          resolution, interaction, or scrolling by itself.
        - Cell location (`cells`) and cell materialization (`slot_policy`) are
          intentionally separated to support heterogeneous cell types.
        - Absence of `header_cells` implies index-based column addressing only.
    """

    def __init__(
        self,
        root: LocatorTree,
        rows: LocatorTree,
        cells: LocatorTree,
        header_cells: Optional[LocatorTree] = None,
        slot_policy: Optional[SlotPolicyType] = None,
    ):
        super().__init__(root, slot_policy)
        self.rows = rows
        self.cells = cells
        self.header_cells = header_cells
