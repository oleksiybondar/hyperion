from hyperiontf.typing import MouseButtonType, MouseButton, TouchFingerType, TouchFinger
from typing import List, Callable, Tuple, Dict
from playwright.sync_api import Page
import time

# Mouse Value Map for Playwright Compatibility
MOUSE_BUTTON_MAP = {
    MouseButton.LEFT: "left",
    MouseButton.MIDDLE: "middle",
    MouseButton.RIGHT: "right",
}

FINGER_MAP = {
    TouchFinger.ONE: "left",
    TouchFinger.TWO: "right",
    TouchFinger.THREE: "middle",
}


class PlaywrightActionBuilder:
    """
    PlaywrightActionBuilder adapts mouse, keyboard, and touch actions for Playwright.
    It stores actions in a stack and executes them when perform() is called.
    """

    def __init__(self, page: Page):
        """
        Initialize the PlaywrightActionBuilder with a Playwright Page instance.

        Parameters:
            page: A Playwright Page instance to execute actions.
        """
        self.page = page
        self.actions_stack: List[Tuple[Callable, Tuple, Dict]] = (
            []
        )  # Stack to store commands and their arguments

    def _add_action(self, method, *args, **kwargs):
        """
        Add an action to the command stack.

        Parameters:
            method: The method to be executed.
            *args: Positional arguments for the method.
            **kwargs: Keyword arguments for the method.
        """
        self.actions_stack.append((method, args, kwargs))

    # Mouse actions
    def mouse_down(self, button: MouseButtonType):
        """
        Simulate a mouse down action on the specified button.

        Parameters:
            button (MouseButtonType): The mouse button to press (default: 'left').
        """
        self._add_action(self.page.mouse.down, button=MOUSE_BUTTON_MAP[button])

    def mouse_up(self, button: MouseButtonType):
        """
        Simulate a mouse up action on the specified button.

        Parameters:
            button (MouseButtonType): The mouse button to release (default: 'left').
        """
        self._add_action(self.page.mouse.up, button=MOUSE_BUTTON_MAP[button])

    def move_to(self, x: float, y: float):
        """
        Move the mouse to the specified x, y coordinates.

        Parameters:
            x (float): The x-coordinate to move the mouse to.
            y (float): The y-coordinate to move the mouse to.
        """
        self._add_action(self.page.mouse.move, x, y)

    # Touch actions mapped to mouse actions
    def touch_down(self, finger: TouchFingerType):
        """
        Simulate a touch down action by mapping it to a mouse down action.

        Parameters:
            finger (TouchFingerType): The finger identifier for the touch action.
        """
        self._add_action(
            self.page.mouse.down, button=FINGER_MAP[finger]
        )  # Map touch down to mouse down for now

    def touch_up(self, finger: TouchFingerType):
        """
        Simulate a touch up action by mapping it to a mouse up action.

        Parameters:
            finger (TouchFingerType): The finger identifier for the touch action.
        """
        self._add_action(self.page.mouse.up, button=FINGER_MAP[finger])

    def touch_move(self, x: float, y: float):
        """
        Simulate a touch move action by mapping it to a mouse move action.

        Parameters:
            x (float): The x-coordinate to move the pointer to.
            y (float): The y-coordinate to move the pointer to.
        """
        self.move_to(x, y)  # Map touch move to mouse move for now

    # Keyboard actions
    def key_down(self, key: str):
        """
        Simulate a key down action.

        Parameters:
            key (str): The key to press down.
        """
        self._add_action(self.page.keyboard.down, key)

    def key_up(self, key: str):
        """
        Simulate a key up action.

        Parameters:
            key (str): The key to release.
        """
        self._add_action(self.page.keyboard.up, key)

    def wait(self, milliseconds: float):
        self._add_action(time.sleep, milliseconds / 1000)

    # Perform all actions
    def perform(self):
        """
        Perform all actions stored in the command stack.
        This method iterates over the actions stack and executes each action.
        """
        for method, args, kwargs in self.actions_stack:
            method(*args, **kwargs)
        self.actions_stack = []  # Clear the stack after execution
