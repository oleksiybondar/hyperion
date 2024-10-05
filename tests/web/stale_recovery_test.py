import pytest
from hyperiontf.executors.pytest import automatic_log_setup, fixture  # noqa: F401
from ..page_objects.basic_elements_page_with_controls import (
    BasicElementsSearchWithControls,
)
from .caps_variants import caps_variants

import os

dirname = os.path.dirname(__file__)
test_page_path = os.path.join(
    dirname, "../resources/test_pages/stale_errors_autohandle.html"
)
page_url = f"file://{test_page_path}"


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = BasicElementsSearchWithControls.start_browser(caps)
    page.open(page_url)
    yield page


@pytest.mark.SingleElement
@pytest.mark.text
@pytest.mark.StaleErrorAutoRecovery
@pytest.mark.click
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_re_render_single_element_and_assert_updated_text(page):
    """
    Test re-rendering a single element using the control panel and asserting its updated text.
    """
    # we need to fire elements search, so get text is a good option for that
    page.single_element_1.get_text()
    page.re_render_panel.re_render_single_element()
    updated_text = "Re-rendered Single Element"
    page.single_element_1.assert_text(updated_text)


@pytest.mark.MultipleElement
@pytest.mark.StaleErrorAutoRecovery
@pytest.mark.text
@pytest.mark.click
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_recover_from_stale_reference_error_multiple_elements(page):
    """
    Test recovering from StaleElementReferenceError when dealing with multiple elements
    """
    page.multiple_elements[0].get_text()

    # Trigger re-render of multiple elements
    page.re_render_panel.re_render_multiple_elements()

    # Verify that the first element's text has been updated
    updated_text = f"Re-rendered Multiple Element {page.multiple_elements.index(page.multiple_elements[0]) + 1}"
    page.multiple_elements[0].assert_text(updated_text)


@pytest.mark.SingleWidget
@pytest.mark.SingleElement
@pytest.mark.StaleErrorAutoRecovery
@pytest.mark.text
@pytest.mark.click
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_auto_recovery_with_direct_chain(page):
    """
    Test auto-recovery of widget child element with direct chain.
    """
    # Step 1: Get text of the child element
    page.single_widget.child_element.get_text()

    # Step 2: Click on the re-render button to trigger the widget re-render
    page.re_render_panel.re_render_single_widget()

    # Step 3: Check the child text after re-render
    updated_text = "Re-rendered Widget Child Element"
    page.single_widget.child_element.assert_text(updated_text)


@pytest.mark.SingleWidget
@pytest.mark.SingleElement
@pytest.mark.StaleErrorAutoRecovery
@pytest.mark.MemorizedElement
@pytest.mark.text
@pytest.mark.click
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_auto_recovery_with_memorized_element(page):
    """
    Test auto-recovery of memorized widget child element in variable.
    """
    # Step 1: Get text of the child element
    page.single_widget.child_element.get_text()

    # Step 2: Store child element reference into a variable
    child_element_ref = page.single_widget.child_element

    # Step 3: Click on the re-render button to trigger the widget re-render
    page.re_render_panel.re_render_single_widget()

    # Step 4: Assert child text using the variable (auto-recovered reference)
    updated_text = "Re-rendered Widget Child Element"
    child_element_ref.assert_text(updated_text)


@pytest.mark.NestedWidgets
@pytest.mark.MultipleWidget
@pytest.mark.SingleWidget
@pytest.mark.SingleElement
@pytest.mark.StaleErrorAutoRecovery
@pytest.mark.MemorizedElement
@pytest.mark.text
@pytest.mark.click
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_nested_widgets_auto_recovery_with_memorized_chain(page):
    """
    Test auto-recovery of memorized nested widgets child element in variable.
    """
    # Step 1: Get text of the child element
    page.widget.child_widgets[1].child_element.get_text()

    # Step 2: Store child element reference into a variable
    child_element_ref = page.widget.child_widgets[1].child_element

    # Step 3: Click on the re-render button to trigger the widget re-render
    page.re_render_panel.re_render_nested_widgets()

    # Step 4: Assert child text using the variable (auto-recovered reference)
    updated_text = "Re-rendered Nested Widget Child Element 3"
    child_element_ref.assert_text(updated_text)
