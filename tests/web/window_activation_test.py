import pytest
from hyperiontf.executors.pytest import automatic_log_setup, fixture  # noqa: F401
from ..page_objects.multiple_windows_page import MultipleWindowsTestPage

from .caps_variants import caps_variants
import os

# The paths to the test pages
multi_tabs_test_page = os.path.join(
    os.path.dirname(__file__), "../resources/test_pages/multi_tabs.html"
)

# The URLs of the test pages
page_url = f"file://{multi_tabs_test_page}"


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = MultipleWindowsTestPage.start_browser(caps)
    page.open(page_url)
    yield page


@pytest.mark.tags("WindowManagement", "AutoResolve", "RootPage", "Switching")
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_auto_resolve_context_switching_to_new_window(page):
    """
    Test automatic context resolution when opening a new window from the root page.

    Scenario:
    - Open a new tab from the root page.
    - Assert the title of the new tab (the title should belong to the new page as auto content switching
      happens only when we interact with elements).
    - Assert some element text from the main page.
    - If the test passes, it means we have successfully switched back to the root page.
    """
    pass


@pytest.mark.tags("WindowManagement", "AutoResolve", "MultiplePages", "Switching")
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_auto_resolve_context_switching_between_multiple_windows(page):
    """
    Test automatic context resolution when switching between multiple windows.

    Scenario:
    - Open several new tabs from the root page.
    - Create new Page objects for each tab.
    - Assert elements from different tabs.
    - If all assertions pass, it means the tabs are correctly switching when we have multiple Page
      objects from the same browser instance.
    """
    pass
