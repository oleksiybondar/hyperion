from __future__ import annotations

from hyperiontf import By, WebPage, button, ButtonBySpec


class ButtonsPage(WebPage):
    """
    Page Object for `buttons.html`.

    This page is used as an etalon for the Button component:
    - a standard button where clickable node contains visible text
    - a button with a decoupled label element (text source is separate)
    """

    @button
    def standard_button(self) -> ButtonBySpec:
        """
        Standard button:
        - click target: the button itself
        - label/text source: the button itself
        """
        return ButtonBySpec(
            root=By.id("btn-standard"),
        )

    @button
    def decoupled_label_button(self) -> ButtonBySpec:
        """
        Button with decoupled label:
        - click target: #btn-decoupled
        - label/text source: #btn-decoupled-label
        """
        return ButtonBySpec(
            root=By.id("btn-decoupled"),
            label=By.id("btn-decoupled-label").from_document(),
        )
