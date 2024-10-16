import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup, fixture  # noqa: F401

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


@pytest.mark.MultipleElement
@pytest.mark.SingleElementy
@pytest.mark.ElementsQueryLanguage
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_item_using_eql(page):
    """
    Test to verify that EQL can accurately find a web page element based on its text content.
    The test uses EQL to locate an element with specific text ('Multiple Element 2') and
    asserts that the element is found and is at the expected index in the collection.

    Args:
        page (BasicElementsSearch): An instance of the page object for testing.
    """
    result = page.multiple_elements['text == "Multiple Element 2"']
    expect(result).is_not_none()
    expect(page.multiple_elements.index(result)).to_be(1)


@pytest.mark.MultipleElement
@pytest.mark.SingleElementy
@pytest.mark.ElementsQueryLanguage
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_item_using_complex_eql(page):
    result = page.multiple_elements['text == "42" or text == "Multiple Element 3"']
    expect(result).is_not_none()
    expect(page.multiple_elements.index(result)).to_be(2)


@pytest.mark.MultipleElement
@pytest.mark.SingleElementy
@pytest.mark.ElementsQueryLanguage
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_item_using_eql_with_regexp(page):
    """
    Test to verify that EQL can accurately find a web page element using regular expression matching.
    This test uses EQL to locate an element whose text matches the regex pattern '/Element 3/' and
    asserts that the element is found and is at the expected index in the collection.

    Args:
        page (BasicElementsSearch): An instance of the page object for testing.
    """
    result = page.multiple_elements["text ~= /Element 3/"]
    expect(result).is_not_none()
    expect(page.multiple_elements.index(result)).to_be(2)


@pytest.mark.MultipleWidget
@pytest.mark.SingleWidget
@pytest.mark.ElementsQueryLanguage
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_item_using_eql_targeting_child_element_text(page):
    result = page.multiple_simple_widgets[
        'child_element.text == "Widget Child Element 2"'
    ]
    expect(result).is_not_none()
    expect(page.multiple_simple_widgets.index(result)).to_be(0)


@pytest.mark.MultipleWidget
@pytest.mark.SingleWidget
@pytest.mark.ElementsQueryLanguage
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_item_using_eql_targeting_child_element_text_without_Results(page):
    """
    Test to ensure that EQL correctly identifies when no widget matches the specified child element text.
    This test searches for a widget where the child element's text is 'Widget Child Element 42' and expects
    no match. It asserts that the result should be None, indicating no widget was found.

    Args:
        page (BasicElementsSearch): An instance of the page object for testing.
    """
    result = page.multiple_simple_widgets[
        'child_element.text == "Widget Child Element 42"'
    ]
    expect(result).is_none()


@pytest.mark.MultipleElement
@pytest.mark.SingleWidget
@pytest.mark.SingleElementy
@pytest.mark.ElementsQueryLanguage
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_find_item_using_eql_without_results(page):
    """
    Test to ensure that EQL correctly handles queries that should yield no results.
    This test searches for an element with a non-existent text ('Multiple Element 42')
    and asserts that no such element is found.

    Args:
        page (BasicElementsSearch): An instance of the page object for testing.
    """
    result = page.multiple_elements['text == "Multiple Element 42"']
    expect(result).is_none()
