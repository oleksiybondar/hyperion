from hyperiontf import By, Widget, elements


class ActionsCell(Widget):
    """
    Cell widget representing an actions panel (buttons).
    """

    @elements
    def buttons(self):
        # buttons are inside .ht-actions container, but targeting buttons directly is simplest.
        return By.css("button")

    def click_first(self) -> None:
        self.buttons[0].click()
