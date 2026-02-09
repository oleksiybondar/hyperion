import os
import re

import pytest
from hyperiontf.executors.pytest import fixture, hyperion_test_case_setup  # noqa: F401
from hyperiontf.typing import FailedExpectationException

from ..page_objects.dropdowns_page import DropdownsPage
from .caps_variants import caps_variants

dirname = os.path.dirname(__file__)
test_page_path = os.path.join(dirname, "../resources/test_pages/dropdowns.html")
page_url = f"file://{test_page_path}"


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = DropdownsPage.start_browser(caps)
    page.open(page_url)
    yield page


# ---------------------------------------------------------------------
# A) Selection (one strategy per definition)
# ---------------------------------------------------------------------


@pytest.mark.Dropdown
@pytest.mark.click
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_native_dropdown_select_by_index(page):
    """
    D1: native <select> dropdown
    Strategy: select by index

    Assumption: index 0 is a placeholder ("please select...") which yields selected_option_index=None,
    and the first real option starts at index 1.
    """
    page.native_dropdown.select(1)
    page.native_dropdown.assert_selected_value("Native B")
    assert page.native_dropdown.selected_option_index == 1


@pytest.mark.Dropdown
@pytest.mark.click
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_sibling_dropdown_select_by_text(page):
    """
    D2: sibling menu dropdown
    Strategy: select by exact text
    """
    page.sibling_dropdown.select("Sibling B")
    page.sibling_dropdown.assert_selected_value("Sibling B")
    assert page.sibling_dropdown.selected_option_index == 1


@pytest.mark.Dropdown
@pytest.mark.click
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_portal_dropdown_select_by_pattern(page):
    """
    D3: portal/detached menu dropdown
    Strategy: select by pattern string (EQL regex integration smoke)
    """
    page.portal_dropdown.select(re.compile(r"Por.*?C"))
    page.portal_dropdown.assert_selected_value("Portal C")
    assert page.portal_dropdown.selected_option_index == 2


# ---------------------------------------------------------------------
# B) Assertion helpers (single representative definition: portal)
# One API call -> one test
# ---------------------------------------------------------------------


@pytest.mark.Dropdown
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_portal_dropdown_assert_has_option(page):
    page.portal_dropdown.assert_has_option("Portal B")


@pytest.mark.Dropdown
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_portal_dropdown_assert_option_missing(page):
    page.portal_dropdown.assert_option_missing("Definitely Missing Option")


@pytest.mark.Dropdown
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_portal_dropdown_assert_selected_value_pass(page):
    page.portal_dropdown.select(1)  # B
    page.portal_dropdown.assert_selected_value("Portal B")


@pytest.mark.Dropdown
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_portal_dropdown_assert_selected_value_fails(page):
    """
    Negative case: ensure assertion failure path works.

    NOTE: tighten the exception type once confirmed (Hyperion assertion exception vs AssertionError).
    """
    page.portal_dropdown.select(1)  # B
    with pytest.raises(FailedExpectationException):
        page.portal_dropdown.assert_selected_value("Portal A")


# ---------------------------------------------------------------------
# C) selected_option_index property (2 dedicated tests)
# ---------------------------------------------------------------------


@pytest.mark.Dropdown
@pytest.mark.selected_index
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_native_dropdown_selected_option_index_is_none_when_nothing_selected(page):
    """
    Native dropdown has a placeholder ("please select...") with no real option selected.
    Contract: selected_option_index is None on initial load.
    """
    assert page.native_dropdown.selected_option_index is None


@pytest.mark.Dropdown
@pytest.mark.selected_index
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_portal_dropdown_selected_option_index_updates_after_selection(page):
    """
    Portal dropdown index introspection should work after selections.
    This also exercises any 'open to render options' behavior required by portal menus.
    """
    page.portal_dropdown.select(2)  # C
    assert page.portal_dropdown.selected_option_index == 2

    page.portal_dropdown.select(1)  # B
    assert page.portal_dropdown.selected_option_index == 1
