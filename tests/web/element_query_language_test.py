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


@pytest.mark.ElementChainResolution
@pytest.mark.InternalTesting
@pytest.mark.EQL
@pytest.mark.AttributeResolution
@pytest.mark.SingleElement
@pytest.mark.SingleWidget
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_eql_resolves_element_chain_correctly(page):
    """
    Test the system's capability to accurately resolve a nested element chain using EQL.

    This test focuses on the internal mechanics of EQL's ability to traverse and resolve chains of nested elements
    ending in an attribute. The test runs against a real system build and uses a predefined query to ensure correct
    chain resolution.
    """
    parsed_query = [
        {"name": "child_widget", "type": "element"},
        {"name": "child_element", "type": "element"},
        {"name": "text", "type": "attribute"},
    ]
    result = page.nested_single_widget.__resolve_eql_chain__(parsed_query)
    expect(result).to_be("Nested Widget Child Element 1")


@pytest.mark.ElementChainResolution
@pytest.mark.InternalTesting
@pytest.mark.EQL
@pytest.mark.UnreachableElement
@pytest.mark.SingleElement
@pytest.mark.SingleWidget
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_eql_handles_unreachable_element_without_failure(page):
    """
    Test that EQL can handle and resolve an element chain containing an unreachable element without failing.

    An unreachable element is present in the chain. The expected behavior is that EQL doesn't fail but resolves to a
    result of None.
    """
    parsed_query = [
        {"name": "child_widget", "type": "element"},
        {"name": "not_reachable", "type": "element"},
        {"name": "text", "type": "attribute"},
    ]
    result = page.nested_single_widget.__resolve_eql_chain__(parsed_query)
    expect(result).to_be(None)


@pytest.mark.ElementChainResolution
@pytest.mark.InternalTesting
@pytest.mark.EQL
@pytest.mark.NonExistentAttribute
@pytest.mark.SingleElement
@pytest.mark.SingleWidget
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_eql_handles_non_existent_attribute_without_failure(page):
    """
    Test that EQL can handle and resolve an element chain containing a non-existent attribute without failing.

    An incorrect attribute is present in the chain. The expected behavior is that EQL doesn't fail but resolves to a
    result of None.
    """
    parsed_query = [
        {"name": "child_widget", "type": "element"},
        {"name": "incorrect", "type": "element"},
        {"name": "text", "type": "attribute"},
    ]
    result = page.nested_single_widget.__resolve_eql_chain__(parsed_query)
    expect(result).to_be(None)


@pytest.mark.ElementChainResolution
@pytest.mark.InternalTesting
@pytest.mark.EQL
@pytest.mark.NestedArrays
@pytest.mark.StyleAttribute
@pytest.mark.MultipleWidgets
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_eql_navigates_nested_arrays_to_retrieve_style_attribute(page):
    """
    Test EQL's capability to navigate through nested arrays using specified indices and retrieve a specific style
    attribute.

    The test aims to verify the correct traversal through nested elements using indices and subsequently fetch a
    specific style attribute. The returned style attribute value is then checked against a list of expected values.
    """
    parsed_query = [
        {"name": "child_widgets", "type": "element", "index": 1},
        {"type": "element", "index": 1},
        {"name": "child_element", "type": "element"},
        {"name": "background-color", "type": "attribute", "attr_type": "style"},
    ]
    result = page.widget.__resolve_eql_chain__(parsed_query)
    expect([result]).contains_at_least_one(
        ["rgb(255, 255, 224)", "rgba(255, 255, 224, 1)"]
    )
