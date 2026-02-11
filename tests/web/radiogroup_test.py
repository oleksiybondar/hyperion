import os
import re

import pytest
from hyperiontf.executors.pytest import fixture, hyperion_test_case_setup  # noqa: F401

from ..page_objects.radiogroups_page import RadioGroupsPage
from .caps_variants import caps_variants

dirname = os.path.dirname(__file__)
test_page_path = os.path.join(dirname, "../resources/test_pages/radiogroups.html")
page_url = f"file://{test_page_path}"


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = RadioGroupsPage.start_browser(caps)
    page.open(page_url)
    yield page


# ---------------------------------------------------------------------
# A) Selection (one strategy per definition)
# Each test explicitly selects and asserts selection outcome.
# One assert_* call per test (selection assertion only).
# ---------------------------------------------------------------------


@pytest.mark.RadioGroup
@pytest.mark.click
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wrapper_radiogroup_select_by_text(page):
    """
    RG1 (Scenario 1): wrapper items with separate input + label
    Strategy: select by exact text
    Validates: click/text/checked resolution for wrapper+input+label structure.
    """
    page.wrapper_group.select("Wrapper B")
    page.wrapper_group.assert_selected_value("Wrapper B")


@pytest.mark.RadioGroup
@pytest.mark.click
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_nested_label_radiogroup_select_by_pattern(page):
    """
    RG2 (Scenario 2): label wraps input (label is the item root)
    Strategy: select by regex pattern
    Assertion: selected index (ensures index introspection works for this shape).
    """
    page.nested_label_group.select(re.compile(r"Nested C"))
    page.nested_label_group.assert_selected_index(2)


@pytest.mark.RadioGroup
@pytest.mark.click
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_sibling_radiogroup_select_by_index(page):
    """
    RG3 (Scenario 3): sibling input + label (no dedicated item wrapper)
    Strategy: select by index
    Assertion: selected value (ensures sibling label resolution works).
    """
    page.sibling_group.select(1)
    page.sibling_group.assert_selected_value("Sibling B")


@pytest.mark.RadioGroup
@pytest.mark.click
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_js_only_radiogroup_select_by_text(page):
    """
    RG4 (Scenario 4): JS-only radios (div items, no native inputs)
    Strategy: select by exact text
    Validates: self-click path + checked_expression evaluation + text from root.
    """
    page.js_only_group.select("JS B")
    page.js_only_group.assert_selected_value("JS B")


# ---------------------------------------------------------------------
# B) Assertion helpers (API coverage)
# One assert_* method -> one test (interaction optional / irrelevant).
# verify_* APIs intentionally omitted.
# ---------------------------------------------------------------------


@pytest.mark.RadioGroup
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_radiogroup_assert_has_item(page):
    page.wrapper_group.assert_has_item("Wrapper A")


@pytest.mark.RadioGroup
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_radiogroup_assert_item_missing(page):
    page.wrapper_group.assert_item_missing(re.compile(r"Definitely Missing"))


@pytest.mark.RadioGroup
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_radiogroup_assert_at_most_one_selected(page):
    page.sibling_group.assert_at_most_one_selected()


@pytest.mark.RadioGroup
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_radiogroup_assert_only_one_selected(page):
    page.wrapper_group.assert_only_one_selected()


@pytest.mark.RadioGroup
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_radiogroup_assert_radio_state_by_index_dispatch(page):
    """
    Exercises assert_radio_state dispatch path for int -> assert_selected_index.
    """
    page.nested_label_group.select(0)
    page.nested_label_group.assert_radio_state(0)


@pytest.mark.RadioGroup
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_radiogroup_assert_none_selected_js_only(page):
    """
    This assertion is meaningful only for the JS-based radiogroup, because native radios
    cannot be 'unselected' by user interaction.

    Fixture requirement:
    - the JS-only group must support a 'none selected' state (initially or via interaction)
      for this test to pass deterministically.
    """
    page.js_only_group.assert_none_selected()
