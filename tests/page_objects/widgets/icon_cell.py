from hyperiontf import (
    By,
    Widget,
    element,
)


class IconCell(Widget):
    """
    Cell widget representing an icon cell.

    The cell contains a visual icon span + text (e.g. "Icon A (unique)").
    """

    @element
    def icon(self):
        return By.css(".icon")
