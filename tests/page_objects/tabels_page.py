from hyperiontf import (
    By,
    WebPage,
    table,
    TableBySpec,
    SlotPolicyRule,
)

from page_objects.widgets.actions_cell import ActionsCell
from page_objects.widgets.icon_cell import IconCell


class TablesPage(WebPage):
    """
    Page Object for `tables.html`.

    Covers:
    - 2 standard HTML tables (with/without header)
    - 2 custom div/grid tables (slot-policy driven)
    """

    # ---------------------------------------------------------------------
    # Standard HTML tables (no slot policy)
    # ---------------------------------------------------------------------

    @table
    def standard_no_header(self) -> TableBySpec:
        return TableBySpec(
            root=By.id("tbl-standard-no-header"),
            rows=By.css("tbody tr"),
            cells=By.css("td"),
        )

    @table
    def standard_with_header(self) -> TableBySpec:
        return TableBySpec(
            root=By.id("tbl-standard-with-header"),
            header_cells=By.css("thead th"),
            rows=By.css("tbody tr"),
            cells=By.css("td"),
        )

    # ---------------------------------------------------------------------
    # Custom tables (div/grid)
    # ---------------------------------------------------------------------

    @table
    def custom_editable(self) -> TableBySpec:
        """
        Table 3: first column is text; middle columns are inputs; last column is actions.

        Slot policy:
        - predicate rule for LAST -> ActionsCell
        """
        return TableBySpec(
            root=By.id("tbl-custom-editable"),
            header_cells=By.css(".ht-header .ht-cell"),
            rows=By.css(".ht-row[data-row]"),
            cells=By.css(".ht-cell"),
            slot_policy=[
                SlotPolicyRule("LAST", ActionsCell),
            ],
        )

    @table
    def custom_mixed(self) -> TableBySpec:
        """
        Table 4: mixed content.

        Slot policy:
        - key-based: "Icon" -> IconCell
        - index-based: -1 -> ActionsCell
        """
        return TableBySpec(
            root=By.id("tbl-custom-mixed"),
            header_cells=By.css(".ht-header .ht-cell"),
            rows=By.css(".ht-row[data-row]"),
            cells=By.css(".ht-cell"),
            slot_policy=[
                SlotPolicyRule("Icon", IconCell),  # key-based substitution
                SlotPolicyRule(-1, ActionsCell),  # last column actions
            ],
        )
