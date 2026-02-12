import os

import pytest
from hyperiontf.executors.pytest import fixture, hyperion_test_case_setup  # noqa: F401

from ..page_objects.buttons_page import ButtonsPage
from .caps_variants import caps_variants

dirname = os.path.dirname(__file__)
test_page_path = os.path.join(dirname, "../resources/test_pages/buttons.html")
page_url = f"file://{test_page_path}"


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = ButtonsPage.start_browser(caps)
    page.open(page_url)
    yield page


@pytest.mark.Button
@pytest.mark.click
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_standard_button_increments_text_on_click(page):
    """
    Standard button: clickable element contains the visible text.
    """
    page.standard_button.assert_text("Button 1; clicks 0")

    page.standard_button.click()
    page.standard_button.assert_text("Button 1; clicks 1")

    page.standard_button.click()
    page.standard_button.assert_text("Button 1; clicks 2")


@pytest.mark.Button
@pytest.mark.click
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_decoupled_label_button_get_text_uses_label(page):
    """
    Decoupled label button:
    - click target is the button element
    - visible text is in a separate label element
    - Button.get_text() must resolve text from label when label locator is provided
    """
    # Initial state (text should be read from label)
    page.decoupled_label_button.assert_text("Button 2; clicks 0")

    page.decoupled_label_button.click()
    page.decoupled_label_button.assert_text("Button 2; clicks 1")

    page.decoupled_label_button.click()
    page.decoupled_label_button.assert_text("Button 2; clicks 2")
