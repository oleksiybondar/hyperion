from __future__ import annotations

import os
import re

import pytest
from hyperiontf.executors.pytest import fixture, hyperion_test_case_setup  # noqa: F401
from hyperiontf.typing import FailedExpectationException, NoSuchElementException

from ..page_objects.tabs_page import TabsPage
from ..page_objects.widgets.activity_panel import ActivityPanel
from ..page_objects.widgets.help_panel import HelpPanel
from ..page_objects.widgets.home_panel import HomePanel
from ..page_objects.widgets.overview_panel import OverviewPanel
from ..page_objects.widgets.profile_panel import ProfilePanel
from ..page_objects.widgets.settings_panel import SettingsPanel
from ..page_objects.widgets.users_panel import UsersPanel
from .caps_variants import caps_variants

dirname = os.path.dirname(__file__)
test_page_path = os.path.join(dirname, "../resources/test_pages/tabs.html")
page_url = f"file://{test_page_path}"


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = TabsPage.start_browser(caps)
    page.open(page_url)
    yield page


@pytest.mark.Tabs
@pytest.mark.click
@pytest.mark.index
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_tabs_1to1_select_by_index_resolves_settings_panel(page):
    page.tabs_1to1.activate(2)

    panel = page.tabs_1to1.panel
    assert isinstance(panel, SettingsPanel)
    panel.title.assert_text("Settings")
    panel.language_select.assert_visible()


@pytest.mark.Tabs
@pytest.mark.click
@pytest.mark.text
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_tabs_1to1_select_by_name_resolves_users_panel(page):
    page.tabs_1to1.activate("Users")

    panel = page.tabs_1to1.panel
    assert isinstance(panel, UsersPanel)
    panel.title.assert_text("Users")
    panel.users_table.assert_visible()


@pytest.mark.Tabs
@pytest.mark.click
@pytest.mark.pattern
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_tabs_1to1_select_by_regexp_resolves_overview_panel(page):
    page.tabs_1to1.activate(re.compile(r"Over.*"))

    panel = page.tabs_1to1.panel
    assert isinstance(panel, OverviewPanel)
    panel.title.assert_text("Overview")
    panel.unique_summary.assert_visible()


@pytest.mark.Tabs
@pytest.mark.slot
@pytest.mark.memoization
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_tabs_1to1_panel_memoization_stays_bound_to_static_slot(page):
    page.tabs_1to1.activate(1)
    users_panel = page.tabs_1to1.panel
    assert isinstance(users_panel, UsersPanel)
    users_panel.users_table.assert_visible()

    page.tabs_1to1.activate(2)
    settings_panel = page.tabs_1to1.panel
    assert isinstance(settings_panel, SettingsPanel)
    settings_panel.language_select.assert_visible()

    page.tabs_1to1.activate(1)
    # Static tabs: previously memoized slot object remains bound to its own slot.
    users_panel.users_table.assert_visible()


@pytest.mark.Tabs
@pytest.mark.slot
@pytest.mark.shared_panel
@pytest.mark.index
@pytest.mark.memoization
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_tabs_rerender_resolves_index_based_slots_and_does_not_rebind_memoized_panel(
    page,
):
    page.tabs_rerender.activate(0)
    home_panel = page.tabs_rerender.panel
    assert isinstance(home_panel, HomePanel)
    home_panel.title.assert_text("Home")
    home_panel.unique_welcome.assert_visible()

    page.tabs_rerender.activate(1)
    profile_panel = page.tabs_rerender.panel
    assert isinstance(profile_panel, ProfilePanel)
    profile_panel.title.assert_text("Profile")
    profile_panel.profile_name.assert_visible()

    with pytest.raises((FailedExpectationException, NoSuchElementException)):
        home_panel.unique_welcome.assert_visible()


@pytest.mark.Tabs
@pytest.mark.slot
@pytest.mark.shared_panel
@pytest.mark.text
@pytest.mark.memoization
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_tabs_rerender_resolves_key_based_slots_and_does_not_rebind_memoized_panel(
    page,
):
    page.tabs_rerender.activate("Activity")
    activity_panel = page.tabs_rerender.panel
    assert isinstance(activity_panel, ActivityPanel)
    activity_panel.title.assert_text("Activity")
    activity_panel.activity_items[0].assert_text("Logged in")

    page.tabs_rerender.activate("Help")
    help_panel = page.tabs_rerender.panel
    assert isinstance(help_panel, HelpPanel)
    help_panel.title.assert_text("Help")
    help_panel.help_link.assert_visible()

    with pytest.raises((AttributeError, NoSuchElementException)):
        page.activity_panel.activity_items[0]("Logged in")


@pytest.mark.Tabs
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_tabs_assert_api_positive_paths(page):
    page.tabs_1to1.assert_has_tab("Users")
    page.tabs_1to1.assert_tab_missing("Definitely Missing Tab")


@pytest.mark.Tabs
@pytest.mark.assertions
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_tabs_assert_api_negative_paths(page):
    with pytest.raises(FailedExpectationException):
        page.tabs_1to1.assert_has_tab("Definitely Missing Tab")

    with pytest.raises(FailedExpectationException):
        page.tabs_1to1.assert_tab_missing("Users")
