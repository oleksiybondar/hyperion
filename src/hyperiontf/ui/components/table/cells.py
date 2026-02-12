from typing import Optional

from hyperiontf.ui.components.slots import Slots


class Cells(Slots):
    """
    Table row cell collection with slot-policy materialization and header-based lookup.

    ``Cells`` is a table-specific specialization of :class:`~hyperiontf.ui.components.slots.Slots`
    used to represent the cells within a single table row.

    Key behaviors
    -------------
    - **Heterogeneous materialization**:
      Each cell position can be materialized as a different wrapper type (Element/Widget/Component)
      based on the owning table's slot policy rules. The resolver is provided by the parent
      :class:`~hyperiontf.ui.components.table.table.Table` via ``table.slot_resolver``.

    - **Column name indexing (optional)**:
      If the table specification defines ``header_cells``, cells may be accessed by header name:

      - ``row.cells["Status"]`` resolves the header name to an integer column index
        and returns the cell at that index.

      When ``header_cells`` is not configured, name-based lookup is disabled and string indexing
      falls back to the base collection behavior.

    Indexing contract
    -----------------
    - ``cells[int]``: returns the cell at the given column index (supports negative indices via Slots).
    - ``cells[str]``: attempts to resolve the string as a column name using the table's header mapping.
      If the name cannot be resolved, falls back to the base ``Slots`` implementation.

    Notes
    -----
    - Name-to-index resolution depends on the owning table's header mapping strategy.
    - ``Cells`` does not define cell-level interaction or assertion APIs; those are provided by the
      materialized cell objects themselves (Element/Widget/etc.).
    """

    @property
    def row(self):
        """Return the owning row widget (the immediate parent in the hierarchy)."""
        return self.parent

    @property
    def table(self):
        """Return the owning table component."""
        return self.row.table

    @property
    def slot_resolver(self):
        """
        Return the slot resolver used to materialize cells.

        This is delegated to the owning table so that slot policies are defined at the table level.
        """
        return self.table.slot_resolver

    @property
    def component_spec(self):
        """Return the table's component specification (TableBySpec)."""
        return self.table.component_spec

    def __getitem__(self, index: int | str):
        """
        Retrieve a cell by column index or header name.

        Parameters
        ----------
        index:
            - ``int``: zero-based cell index (negative indices supported).
            - ``str``: header name to resolve to a column index (only when ``header_cells`` is configured).

        Returns
        -------
        Element | Widget | Any
            The materialized cell wrapper at the resolved index.

        Notes
        -----
        If string indexing is used and the name cannot be resolved, this method falls back to the
        base ``Slots`` behavior for string indexing (if any).
        """
        if isinstance(index, str):
            named_index = self._resolve_column_name_index(index)
            if named_index is not None:
                return super().__getitem__(named_index)

        return super().__getitem__(index)

    def _resolve_column_name_index(self, name: str) -> Optional[int]:
        """
        Resolve a header name to a column index.

        Resolution is only available when the table specification defines ``header_cells``.
        When headers are absent, returns ``None``.

        Parameters
        ----------
        name:
            Header name to resolve.

        Returns
        -------
        Optional[int]
            Integer column index for the given header name, or ``None`` if:
            - headers are not configured, or
            - the name is not present in the resolved header list.
        """
        if self.component_spec.header_cells is None:
            return None

        return self.table.column_name_to_index_resolver(name)
