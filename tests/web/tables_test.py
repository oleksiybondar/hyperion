import os

import pytest
from hyperiontf.executors.pytest import fixture, hyperion_test_case_setup  # noqa: F401
from hyperiontf.typing import FailedExpectationException
from page_objects.widgets.actions_cell import ActionsCell
from page_objects.widgets.icon_cell import IconCell

from ..page_objects.tabels_page import TablesPage
from .caps_variants import caps_variants

dirname = os.path.dirname(__file__)
test_page_path = os.path.join(dirname, "../resources/test_pages/tables.html")
page_url = f"file://{test_page_path}"


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = TablesPage.start_browser(caps)
    page.open(page_url)
    yield page


@pytest.mark.Table
@pytest.mark.collection
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_table_len_matches_rows_len(page):
    table = page.standard_no_header
    assert len(table) == len(table.rows)


@pytest.mark.Table
@pytest.mark.collection
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_table_getitem_returns_row(page):
    row = page.standard_no_header[0]
    # explicit outcome: row should have at least one cell
    row.assert_has_cells(1)


@pytest.mark.Table
@pytest.mark.collection
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_table_iter_yields_rows(page):
    table = page.standard_no_header
    count = 0
    for row in table:
        row.assert_has_cells(1)
        count += 1

    # explicit outcome
    assert count == len(table)


@pytest.mark.Table
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_table_assert_has_rows_pass(page):
    page.standard_no_header.assert_has_rows(1)


@pytest.mark.Table
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_table_assert_row_count_fails(page):
    # Negative: make sure assertion mode raises
    with pytest.raises(FailedExpectationException):
        page.standard_no_header.assert_row_count(9999)


@pytest.mark.Table
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_table_assert_columns_names_pass(page):
    # This assumes tables.html defines these headers in this exact order.
    page.standard_with_header.assert_columns_names(["Name", "Role", "Status"])


@pytest.mark.Table
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_table_assert_columns_names_fails_without_headers(page):
    with pytest.raises(AssertionError):
        page.standard_no_header.assert_columns_names(["Name"])


@pytest.mark.Table
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_table_assert_table_normalized_pass(page):
    page.standard_no_header.assert_table_normalized()


@pytest.mark.Table
@pytest.mark.collection
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_table_2d_index_access_returns_correct_cell(page):
    table = page.standard_no_header

    table[0][0].assert_text("StdNH R1C1")


@pytest.mark.Table
@pytest.mark.collection
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_table_2d_column_name_access_returns_correct_cell(page):
    table = page.standard_with_header

    table[0]["Role"].assert_text("Admin")


@pytest.mark.Table
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_slots_materialize_correct_cell_type(page):
    row = page.standard_with_header[0]

    # plain cell
    row["Name"].assert_text("Alice")
    row["Status"].assert_text("Active")


@pytest.mark.Table
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_column_key_matches_index(page):
    row = page.standard_with_header[0]

    row["Role"].assert_text(row[1].get_text())


@pytest.mark.Table
@pytest.mark.slot
@pytest.mark.predicate
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_last_column_resolves_to_actions_cell_via_predicate(page):
    cell = page.custom_editable[0][-1]
    assert isinstance(cell, ActionsCell)
    cell.buttons[0].assert_text("Edit")


@pytest.mark.Table
@pytest.mark.slot
@pytest.mark.index
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_last_column_resolves_to_actions_cell_via_index(page):
    cell = page.custom_mixed[0][-1]
    assert isinstance(cell, ActionsCell)
    cell.buttons[1].assert_text("Remove")


@pytest.mark.Table
@pytest.mark.slot
@pytest.mark.key
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_column_key_resolves_to_icon_cell_via_key(page):
    cell = page.custom_mixed[-1]["Icon"]
    assert isinstance(cell, IconCell)
    cell.icon.assert_visible()
