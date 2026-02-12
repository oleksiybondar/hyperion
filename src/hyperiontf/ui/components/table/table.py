from typing import List, Optional, Union

from hyperiontf.assertions.expectation_result import ExpectationResult
from hyperiontf.ui.components.slot_rule_resolver import SlotRuleResolver
from hyperiontf.ui.components.table.row import Row
from hyperiontf.ui.decorators.page_object_helpers import elements, widgets
from hyperiontf.ui.components.base_component import BaseComponent
from hyperiontf.ui.helpers.prepare_expect_object import prepare_expect_object


class Table(BaseComponent):
    """
    Reusable Table component with slot-policy cell materialization.

    ``Table`` models a logical table structure as:
    - a collection of :class:`~hyperiontf.ui.components.table.row.Row` objects (rows)
    - where each row contains a heterogeneous collection of cells (see ``Row.cells`` / ``Cells``)

    The table is configured declaratively via a table specification (TableBySpec) that provides:
    - ``root``: component scope
    - ``rows``: locator for enumerating row roots
    - ``cells``: locator for enumerating cells within a row
    - optional ``header_cells``: locator for header cell elements (column identity)
    - optional ``slot_policies``: ordered rules controlling how cells are materialized

    Slot policies
    -------------
    ``Table`` owns a :class:`~hyperiontf.ui.components.slot_rule_resolver.SlotRuleResolver`
    instance (``slot_resolver``) used by row cell collections to decide which wrapper class
    should be instantiated for each cell position. Rules are applied in order and the
    **last matching rule wins**.

    Column names (optional)
    -----------------------
    When ``header_cells`` is configured, ``Table`` can derive column names from header cell text
    and use those names for:
    - key-based slot policy rules (via ``column_name_to_index_resolver``)
    - name-based cell access (e.g. ``table[0]["Status"]`` through Row/Cells indexing)

    Navigation and collection behavior
    ----------------------------------
    ``Table`` behaves like a collection of rows:
    - ``table[i]`` returns the Row at index ``i``
    - iteration yields rows: ``for row in table: ...``
    - ``len(table)`` returns the current row count

    Assertions and verification
    ---------------------------
    ``Table`` provides table-level expectation helpers:
    - ``assert_has_rows`` / ``verify_has_rows``: minimum row count
    - ``assert_row_count`` / ``verify_row_count``: exact row count
    - ``assert_columns_names`` / ``verity_columns_names``: validate derived header names
    - ``assert_table_normalized`` / ``verity_table_normalized``: validate consistent cell counts per row

    Notes
    -----
    - All row/cell enumerations reflect **currently rendered** DOM/UI state.
      Virtualized tables are implicitly supported (only present rows are modeled).
    - Cell-level interaction and assertions are performed on the materialized cell wrappers
      (Element/Widget/etc.) returned by row/cell indexing.
    """

    def __init__(self, parent, locator, name: str):
        """
        Create a Table component instance.

        Parameters
        ----------
        parent:
            Owning container (Page/Widget/Component).
        locator:
            Component root locator (framework-internal wrapper).
        name:
            Logical name of the component in the Page Object.
        """
        super().__init__(parent, locator, name)
        self._column_names: List[str] = []
        self.slot_resolver = SlotRuleResolver(
            self.component_spec.slot_policies,
            self.column_name_to_index_resolver,
        )

    @property
    def column_names(self) -> List[str]:
        """
        Return derived column names from header cells (when configured).

        When the table specification defines ``header_cells``, this property resolves header
        cell text and caches the resulting list for name-based column access and key policies.

        Returns
        -------
        List[str]
            Column names in header order. Returns an empty list when header cells are not configured.
        """
        if self.component_spec.header_cells is None:
            return []
        if len(self._column_names) == 0:
            self._column_names = [header.get_text() for header in self.headers]
        return self._column_names

    def column_name_to_index_resolver(self, name) -> Optional[int]:
        """
        Resolve a column name to an integer index.

        Parameters
        ----------
        name:
            Column name to resolve (typically derived from header cell visible text).

        Returns
        -------
        Optional[int]
            Integer index if the name is present, otherwise ``None``.
        """
        try:
            return self.column_names.index(name)
        except ValueError:
            return None

    @widgets(klass=Row)
    def rows(self):
        """
        Return the table's rows collection.

        Rows are modeled as :class:`~hyperiontf.ui.components.table.row.Row` widgets.
        """
        return self.component_spec.rows

    @elements
    def headers(self):
        """
        Return the table's header cells collection.

        This is only meaningful when ``header_cells`` is configured in the table spec.
        """
        return self.component_spec.header_cells

    def force_refresh(self):
        """
        Force refresh of cached row/header resolution.

        Clears the rows cache and (when header cells are configured) clears the derived
        column name cache and refreshes header resolution.
        """
        self.rows.force_refresh()
        if self.component_spec.header_cells is not None:
            self._column_names = []
            self.headers.force_refresh()

    def __getitem__(self, index: int | str):
        """
        Retrieve a row by index.

        Delegates to ``self.rows[index]``.
        """
        return self.rows[index]

    def __iter__(self):
        """Iterate over rows in the table."""
        return iter(self.rows)

    def __len__(self):
        """Return the number of currently resolved rows."""
        return len(self.rows)

    def assert_has_rows(self, min_rows: int = 1) -> ExpectationResult:
        """
        Assert that the table contains at least ``min_rows`` rows.

        Fast-fail assertion: raises on mismatch, returns an ``ExpectationResult`` on success.
        """
        actual_value = self.__len__()
        verify = prepare_expect_object(
            self,
            actual_value,
            True,
            "Asserting table row count",
            self._logger,
        )
        return verify.to_be_greater_than_or_equal_to(min_rows)

    def verify_has_rows(self, min_rows: int = 1) -> ExpectationResult:
        """
        Verify that the table contains at least ``min_rows`` rows.

        Decision-mode check: returns an ``ExpectationResult`` (bool-compatible) without raising.
        """
        actual_value = self.__len__()
        verify = prepare_expect_object(
            self,
            actual_value,
            False,
            "Verifying table row count",
            self._logger,
        )
        return verify.to_be_greater_than_or_equal_to(min_rows)

    def assert_row_count(self, expected: int) -> ExpectationResult:
        """
        Assert that the table contains exactly ``expected`` rows.

        Fast-fail assertion: raises on mismatch, returns an ``ExpectationResult`` on success.
        """
        actual_value = self.__len__()
        verify = prepare_expect_object(
            self,
            actual_value,
            True,
            "Asserting table row count",
            self._logger,
        )
        return verify.to_be(expected)

    def verify_row_count(self, expected: int) -> ExpectationResult:
        """
        Verify that the table contains exactly ``expected`` rows.

        Decision-mode check: returns an ``ExpectationResult`` (bool-compatible) without raising.
        """
        actual_value = self.__len__()
        verify = prepare_expect_object(
            self,
            actual_value,
            False,
            "Verifying table row count",
            self._logger,
        )
        return verify.to_be(expected)

    def assert_columns_names(self, expected_names: List[str]) -> ExpectationResult:
        """
        Assert that derived column names equal ``expected_names``.

        This requires ``header_cells`` to be configured. Comparison is order-sensitive.

        Parameters
        ----------
        expected_names:
            Expected column names in header order.

        Returns
        -------
        ExpectationResult
            Expectation result on success. Raises on mismatch.
        """
        if self.component_spec.header_cells is None:
            raise AssertionError(
                "Asserting table column names failed: header_cells not defined in TableBySpec."
            )

        actual_value = self.column_names

        verify = prepare_expect_object(
            self,
            actual_value,
            True,
            "Asserting table column names",
            self._logger,
        )
        return verify.to_be(expected_names)

    def verity_columns_names(
        self, expected_names: List[str]
    ) -> Union[bool, ExpectationResult]:
        """
        Verify that derived column names equal ``expected_names``.

        This requires ``header_cells`` to be configured. When headers are not configured,
        this method returns ``False``.

        Parameters
        ----------
        expected_names:
            Expected column names in header order.

        Returns
        -------
        Union[bool, ExpectationResult]
            - ``False`` when headers are not configured.
            - Otherwise, an ``ExpectationResult`` describing the comparison.
        """
        if self.component_spec.header_cells is None:
            return False

        actual_value = self.column_names

        verify = prepare_expect_object(
            self,
            actual_value,
            False,
            "Verifying table column names",
            self._logger,
        )
        return verify.to_be(expected_names)

    def assert_table_normalized(self) -> bool:
        """
        Assert that the table is normalized (consistent cell counts per row).

        A normalized table satisfies:
        - each rendered row contains the same number of cells
        - when headers are configured, header cell count matches row cell count

        Returns
        -------
        bool
            ``True`` if normalized. In assertion mode, failures may raise depending on the
            underlying row-level assertion behavior.
        """
        expected_value = self._get_expected_cells_count()

        for row in self.rows:
            if not row.assert_row_cells(expected_value):
                return False

        return True

    def _get_expected_cells_count(self):
        """
        Determine the expected number of cells for normalization checks.

        When headers are configured, the header count is used as the expected cell count.
        Otherwise, the first row cell count is used.
        """
        if self.component_spec.header_cells is not None:
            return len(self.headers)
        else:
            return len(self.rows[0])

    def verity_table_normalized(self) -> bool:
        """
        Verify that the table is normalized (consistent cell counts per row).

        Returns
        -------
        bool
            ``True`` if all rendered rows match the expected cell count, otherwise ``False``.
        """
        expected_value = self._get_expected_cells_count()

        for row in self.rows:
            if not row.verify_row_cells(expected_value):
                return False

        return True
