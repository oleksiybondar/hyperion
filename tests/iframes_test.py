import pytest
from hyperiontf.executors.pytest import automatic_log_setup, fixture  # noqa: F401
from page_objects.iframe_page import IframesPage

import os

# The paths to the test pages
root_page_path = os.path.join(
    os.path.dirname(__file__), "resources/test_pages/iframes_root.html"
)

# The URLs of the test pages
root_page_url = f"file://{root_page_path}"
selenium_caps = {"automation": "selenium"}
playwright_caps = {"automation": "playwright"}


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = IframesPage.start_browser(caps)
    page.open(root_page_url)
    yield page


@pytest.mark.tags("Iframe", "AutoResolve", "SingleElement", "text")
@pytest.mark.parametrize("page", [selenium_caps, playwright_caps], indirect=True)
def test_auto_resolve_context_switching_to_iframe(page):
    """
    Test automatic context resolution from default (page context) to iframe.
    """
    page.static_iframe.single_element_1.assert_text(
        "Single Element 1 (ID: single-element-1)"
    )


@pytest.mark.tags("Iframe", "AutoResolve", "SingleElement", "text")
@pytest.mark.parametrize("page", [selenium_caps, playwright_caps], indirect=True)
def test_auto_resolve_context_switching_from_iframe(page):
    """
    Test automatic context resolution from iframe back to default (page context).
    """
    # Step 1: Invoke any iframe child element to switch the content to the iframe
    page.dynamic_iframe.page_header.get_text()

    # Step 2: Assert a text on the root page's title element
    page.page_header.assert_text("Main Page Content")


@pytest.mark.tags("Iframe", "AutoResolve", "SingleElement", "text")
@pytest.mark.parametrize("page", [selenium_caps, playwright_caps], indirect=True)
def test_auto_resolve_context_switching_to_nested_iframe(page):
    """
    Test automatic context resolution when switching to a nested iframe.
    """
    nested_frame_child = page.dynamic_iframe.dynamic_iframe.single_element_1
    nested_frame_child.assert_text("Single Element 1 (ID: single-element-1)")


@pytest.mark.tags("Iframe", "AutoResolve", "ContextSwitching", "text")
@pytest.mark.parametrize("page", [selenium_caps, playwright_caps], indirect=True)
def test_switch_back_to_root_from_inner_iframe(page):
    """
    Test switching back to the root page from the innermost iframe using direct child element.
    """
    # Start inside the innermost iframe
    page.dynamic_iframe.dynamic_iframe.single_element_1.get_text()

    # Switch back to the root page
    page.page_header.assert_text("Main Page Content")


@pytest.mark.tags("Iframe", "AutoResolve", "ContextSwitching", "text")
@pytest.mark.parametrize("page", [selenium_caps, playwright_caps], indirect=True)
def test_switch_back_to_mid_level_iframe_from_inner_iframe(page):
    """
    Test switching back to a mid-level iframe from the innermost iframe using direct child element.
    """
    # Start inside the innermost iframe
    page.dynamic_iframe.dynamic_iframe.single_element_1.get_text()

    # Switch back to the mid-level iframe
    page.dynamic_iframe.page_header.assert_text("Iframe Content")


@pytest.mark.tags("Iframe", "AutoResolve", "ContextSwitching", "text")
@pytest.mark.parametrize("page", [selenium_caps, playwright_caps], indirect=True)
def test_switch_back_to_mid_level_iframe_using_memorized_child(page):
    """
    Test switching back to a mid-level iframe using a memorized child element from the mid-level iframe.
    """
    # Start inside the mid-level iframe
    memorized_mid_child_element = page.dynamic_iframe.page_header

    # Start inside the innermost iframe
    innermost = page.dynamic_iframe.dynamic_iframe
    innermost.single_element_1.get_text()
    memorised_innermost_child_element = innermost.single_element_2

    # Switch back to the root page
    page.page_header.assert_text("Main Page Content")

    # Switch back to the innermost using the memorized child element
    memorised_innermost_child_element.assert_text("Single Element 2 (Unique Style 1)")

    # Switch back to mid-level iframe using memorised child element
    memorized_mid_child_element.assert_text("Iframe Content")


@pytest.mark.tags("Iframe", "AutoResolve", "ContextSwitching", "text")
@pytest.mark.parametrize("page", [selenium_caps, playwright_caps], indirect=True)
def test_auto_resolve_context_switching_between_iframes(page):
    """
    Test automatic context resolution when switching between iframes.
    """
    # Start inside the first iframe
    page.static_iframe.single_element_1.get_text()

    # Switch to the second iframe
    page.dynamic_iframe.page_header.assert_text("Iframe Content")


@pytest.mark.tags("Iframe", "AutoResolve", "ContextSwitching", "text")
@pytest.mark.parametrize("page", [selenium_caps, playwright_caps], indirect=True)
def test_dynamic_iframes_re_rendering(page):
    """
    Test automatic context resolution and stale error resolution during dynamic iframe re-rendering.
    """
    # Start inside the mid-level iframe
    memorized_mid_child_element = page.dynamic_iframe.re_render_iframe_button

    # Start inside the innermost iframe
    innermost = page.dynamic_iframe.dynamic_iframe
    innermost.single_element_1.get_text()
    memorized_innermost_child_element = innermost.single_element_2

    # Trigger re-rendering of iframes (perform the action that causes re-rendering)
    page.re_render_iframe_button.click()

    # Switch back to the innermost using the memorized child element
    memorized_innermost_child_element.assert_text("Single Element 2 (Unique Style 1)")

    # Switch back to mid-level iframe using the memorized child element
    memorized_mid_child_element.click()

    # Switch back to the innermost using the memorized child element
    memorized_innermost_child_element.assert_text("Single Element 2 (Unique Style 1)")
