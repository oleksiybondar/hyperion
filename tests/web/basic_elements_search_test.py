import pytest
from hyperiontf.executors.pytest import automatic_log_setup, fixture  # noqa: F401
from ..page_objects.basic_elements_page import BasicElementsSearch
from .caps_variants import caps_variants
from hyperiontf import expect

import os

dirname = os.path.dirname(__file__)
test_page_path = os.path.join(
    dirname, "../resources/test_pages/basic_elements_search_and_interactions.html"
)
page_url = f"file://{test_page_path}"


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = BasicElementsSearch.start_browser(caps)
    page.open(page_url)
    yield page


@pytest.mark.SingleElement
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_simple_element_and_assert_its_text(page):
    """
    Test finding a simple element and asserting its text.
    """
    page.single_element_1.assert_text("Single Element 1 (ID: single-element-1)")


@pytest.mark.SingleElement
@pytest.mark.attribute
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_simple_element_and_assert_its_attribute(page):
    """
    Test finding a simple element and asserting its attribute.
    """
    page.single_element_2.assert_attribute("class", "single-element unique-element-1")


@pytest.mark.SingleElement
@pytest.mark.style
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_simple_element_and_assert_its_style(page):
    """
    Test finding a simple element and asserting its style.
    """
    color = page.single_element_3.get_style("background-color")
    expect([color]).contains_at_least_one(
        ["rgb(240, 128, 128)", "rgba(240, 128, 128, 1)"]
    )


@pytest.mark.MultipleElement
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_multiple_elements_and_assert_their_texts(page):
    """
    Test finding multiple elements and asserting their texts.
    """
    for element in page.multiple_elements:
        expected_string = (
            f"Multiple Element {page.multiple_elements.index(element) + 1}"
        )
        element.assert_text(expected_string)


@pytest.mark.SingleWidget
@pytest.mark.SingleElement
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_widget_child_and_assert_its_text(page):
    """
    Test finding a widget child element and asserting its text.
    """
    page.single_widget.child_element.assert_text("Widget Child Element 1")


@pytest.mark.NestedWidget
@pytest.mark.SingleWidget
@pytest.mark.SingleElement
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_nested_widget_child_and_assert_its_text(page):
    """
    Test finding a nested widget child element and asserting its text
    """
    page.nested_single_widget.child_widget.child_element.assert_text(
        "Nested Widget Child Element 1"
    )


@pytest.mark.NestedWidget
@pytest.mark.SingleWidget
@pytest.mark.MultipleWidget
@pytest.mark.SingleElement
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_nested_widgets_child_and_assert_its_text(page):
    """
    Test finding a nested widgets child element and asserting its text
    """
    for nested_widget in page.widget.child_widgets:
        expected_string = f"Nested Widget Child Element {page.widget.child_widgets.index(nested_widget) + 2}"
        nested_widget.child_element.assert_text(expected_string)


@pytest.mark.SingleElement
@pytest.mark.click
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_clickable_element_text_change(page):
    """
    Test clicking the clickable element and assert its changing text
    """
    initial_text = page.clickable_element.get_text()
    page.clickable_element.click()
    updated_text = (
        f"Click Me (Click Count: {int(initial_text.split(': ')[-1][:-1]) + 1})"
    )
    page.clickable_element.assert_text(updated_text)


@pytest.mark.SingleElement
@pytest.mark.fill
@pytest.mark.attribute
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_input_field_set_value_and_assert_attribute(page):
    """
    Test typing something into the input field and assert its attribute value
    """
    input_value = "Hello, HyperionTF!"
    page.input_element.send_keys(input_value)
    page.input_element.assert_attribute("value", input_value)
