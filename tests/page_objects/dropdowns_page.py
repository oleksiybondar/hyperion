from __future__ import annotations

from hyperiontf import By, WebPage, dropdown, DropdownBySpec


class DropdownsPage(WebPage):
    """
    Page Object for `dropdowns.html`.

    Covers:
    - native <select> dropdown (Scenario 1)
    - custom dropdown with sibling menu (Scenario 2)
    - custom dropdown with detached/portal menu (Scenario 3)
    """

    # ---------------------------------------------------------------------
    # Scenario 1: native <select>
    # ---------------------------------------------------------------------

    @dropdown
    def native_dropdown(self) -> DropdownBySpec:
        """
        Native HTML <select> control exposed as a Dropdown.

        Although the DOM structure differs from custom dropdowns, the control
        still represents a single-value selection widget and is therefore
        intentionally modeled via the same Dropdown API.
        """
        return DropdownBySpec(
            root=By.id("dd-native-select"),
            # Native <option> elements are children of <select>
            options=By.css("option"),
        )

    # ---------------------------------------------------------------------
    # Scenario 2: sibling options (custom dropdown)
    # ---------------------------------------------------------------------

    @dropdown
    def sibling_dropdown(self) -> DropdownBySpec:
        """
        Custom dropdown where the options menu is a sibling of the trigger.

        - root: trigger button
        - label: selected value text inside trigger
        - options: resolved via trigger-anchored sibling XPath
        """
        return DropdownBySpec(
            root=By.id("dd-sibling-trigger"),
            label=By.id("dd-sibling-label"),
            options=By.xpath(
                "./following-sibling::ul[@id='dd-sibling-menu']"
                "//li[contains(concat(' ', normalize-space(@class), ' '), ' option ')]"
            ),
        )

    # ---------------------------------------------------------------------
    # Scenario 3: detached options (portal)
    # ---------------------------------------------------------------------

    @dropdown
    def portal_dropdown(self) -> DropdownBySpec:
        """
        Custom dropdown where the options menu is rendered in a detached container.

        - root: trigger button
        - label: selected value text inside trigger
        - options: document-scoped XPath to the portal menu
        """
        return DropdownBySpec(
            root=By.id("dd-portal-trigger"),
            label=By.id("dd-portal-label"),
            options=By.css("#dd-portal-menu .option").from_document(),
        )
