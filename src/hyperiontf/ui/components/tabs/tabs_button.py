from hyperiontf.ui.decorators.page_object_helpers import element
from hyperiontf.ui.components.button.button import Button


class TabButton(Button):
    @element
    def close_button(self):
        return self.component_spec.close_button
