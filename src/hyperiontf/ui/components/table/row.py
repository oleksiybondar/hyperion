from typing import Type

from hyperiontf.assertions.expectation_result import ExpectationResult
from hyperiontf.ui.components.decorators.page_object_helpers import slots
from hyperiontf.ui.helpers.prepare_expect_object import prepare_expect_object
from hyperiontf.ui.widget import Widget


class Row(Widget):
    """
    A single table row widget.

    ``Row`` represents one logical row within a :class:`~hyperiontf.ui.components.table.table.Table`.
    It is a lightweight façade over the row scope that exposes the row's cells as a
    heterogeneous, slot-policy-driven collection.

    Structural model
    ----------------
    - A Row belongs to a Table and inherits its specification and policies.
    - Cells are declared using the table's structural ``cells`` locator from the component spec.
    - Each cell may be materialized as a different wrapper type (Element/Widget/Component) based on
      the table's slot policy rules.

    Convenience behavior
    --------------------
    - ``row[index]`` delegates to ``row.cells[index]``.
      - ``index`` may be ``int`` (positional) or ``str`` (header name), depending on the underlying
        ``Cells`` implementation and whether headers are configured.
    - Iteration yields cells: ``for cell in row: ...``
    - ``len(row)`` returns the number of currently resolved cells.

    Assertions and verification
    ---------------------------
    Row provides basic count-based expectations for diagnostics and fast-fail checks:

    - ``assert_has_cells(min_cells=...)`` / ``verify_has_cells(min_cells=...)``
      validate that the row contains at least a given number of cells.

    - ``assert_row_cells(expected=...)`` / ``verify_row_cells(expected=...)``
      validate that the row contains exactly the expected number of cells.

    Notes
    -----
    - All counts reflect **currently resolved** cells for the row in the active UI state.
      (No guarantees are made about off-screen or virtualized content.)
    - Cell-level interaction and assertions are performed on the returned cell wrappers
      (Element/Widget/etc.), not by the Row itself.
    """

    @property
    def table(self):
        """
        Return the owning table component.

        The Row is instantiated under a rows collection holder; this property walks the hierarchy:
        ``row.parent`` -> rows collection holder, ``row.parent.parent`` -> Table.
        """
        # parent -> rows collection holder
        # rows.parent -> table
        return self.parent.parent

    @property
    def component_spec(self):
        """Return the table's component specification (TableBySpec)."""
        return self.table.component_spec

    @slots
    def cells(self):
        """
        Return the row's cells as a slot-materialized collection.

        The locator used for cell enumeration is taken from the owning table spec (``TableBySpec.cells``).
        """
        return self.component_spec.cells

    def __getitem__(self, index: int | str):
        """
        Retrieve a cell by index or name.

        Delegates to ``self.cells[index]``. Supported indexing depends on the underlying Cells collection:
        - ``int`` for positional access (including negative indices if supported by Slots).
        - ``str`` for header-name access when headers are configured.
        """
        return self.cells[index]

    def __iter__(self):
        """Iterate over materialized cells in this row."""
        return iter(self.cells)

    def __len__(self):
        """Return the number of currently resolved cells in this row."""
        return len(self.cells)

    def assert_has_cells(self, min_cells: int = 1) -> ExpectationResult:
        """
        Assert that the row contains at least ``min_cells`` cells.

        This is a fast-fail assertion: on mismatch, it raises (via the expectation machinery).
        On success, returns the expectation result for logging/diagnostics consistency.
        """
        actual_value = self.__len__()
        verify = prepare_expect_object(
            self,
            actual_value,
            True,
            "Asserting row cells count",
            self._logger,
        )
        return verify.to_be_greater_than_or_equal_to(min_cells)

    def verify_has_cells(self, min_cells: int = 1) -> ExpectationResult:
        """
        Verify that the row contains at least ``min_cells`` cells.

        This is a non-throwing decision-mode check: it returns an ``ExpectationResult`` that is
        bool-compatible and traceable in logs.
        """
        actual_value = self.__len__()
        verify = prepare_expect_object(
            self,
            actual_value,
            False,
            "Verifying row cells count",
            self._logger,
        )
        return verify.to_be_greater_than_or_equal_to(min_cells)

    def assert_row_cells(self, expected: int) -> Type[ExpectationResult]:
        """
        Assert that the row contains exactly ``expected`` cells.

        Fast-fail assertion: raises on mismatch, returns an expectation result on success.
        """
        actual_value = self.__len__()
        verify = prepare_expect_object(
            self,
            actual_value,
            True,
            "Asserting row cells count",
            self._logger,
        )
        return verify.to_be(expected)

    def verify_row_cells(self, expected: int) -> Type[ExpectationResult]:
        """
        Verify that the row contains exactly ``expected`` cells.

        Decision-mode check: returns an ``ExpectationResult`` (bool-compatible) without raising.
        """
        actual_value = self.__len__()
        verify = prepare_expect_object(
            self,
            actual_value,
            False,
            "Verifying row cells count",
            self._logger,
        )
        return verify.to_be(expected)
