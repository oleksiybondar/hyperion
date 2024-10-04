from selenium.webdriver.common.action_chains import (
    ActionBuilder,
    PointerInput,
    KeyInput,
)
from selenium.webdriver.common.actions.pointer_actions import PointerActions
from hyperiontf.typing import MouseButtonType, MouseButton, TouchFinger, TouchFingerType

# Mouse Value Map for Selenium Compatibility
MOUSE_BUTTON_MAP = {
    MouseButton.LEFT: 0,  # Selenium's left button
    MouseButton.MIDDLE: 1,  # Selenium's middle button
    MouseButton.RIGHT: 2,  # Selenium's right button
}

FINGERS_MAP = {
    TouchFinger.ONE: 0,
    TouchFinger.TWO: 1,
    TouchFinger.THREE: 2,
}


class SeleniumActionBuilder:
    """
    SeleniumActionBuilder adapts mouse, keyboard, and touch actions for Selenium's ActionChains.
    It uses a Selenium ActionBuilder instance and maps framework-specific arguments to the
    proper Selenium-compatible format.

    The class supports basic mouse, touch, and keyboard actions by simulating these actions
    through corresponding Pointer and Key Inputs.
    """

    def __init__(self, driver):
        """
        Initialize the SeleniumActionBuilder with a Selenium WebDriver instance.

        Parameters:
            driver: A Selenium WebDriver instance.
        """
        self.action_builder = ActionBuilder(driver)
        self._create_devices()
        self._create_pointer_actions()

    def _create_devices(self):
        """
        Internal method to initialize mouse, touch, and keyboard input devices for the action builder.
        This method creates three input devices: one for mouse actions, one for touch actions, and
        one for keyboard actions.
        """
        self._mouse_device = PointerInput("mouse", "mouse")
        self._touch_device = PointerInput("touch", "touch")
        self._keyboad_device = KeyInput("keyboard")

        self.action_builder.devices = [
            self._mouse_device,
            self._touch_device,
            self._keyboad_device,
        ]

    def _create_pointer_actions(self):
        """
        Internal method to create PointerActions for both mouse and touch devices.
        """
        self._mouse_actions = PointerActions(self._mouse_device)
        self._touch_actions = PointerActions(self._touch_device)

    # Mouse actions
    def mouse_down(self, button: MouseButtonType):
        """
        Simulate a mouse down action on the specified button.

        Parameters:
            button (MouseButtonType): The mouse button to press (default: 'left').
        """
        self._mouse_actions.pointer_down(MOUSE_BUTTON_MAP[button])

    def mouse_up(self, button: MouseButtonType):
        """
        Simulate a mouse up action on the specified button.

        Parameters:
            button (MouseButtonType): The mouse button to release (default: 'left').
        """
        self._mouse_actions.pointer_up(MOUSE_BUTTON_MAP[button])

    # Touch actions mapped to mouse actions
    def touch_down(self, finger: TouchFingerType):
        """
        Simulate a touch down action by mapping it to a mouse down action using the specified finger.

        Parameters:
            finger (TouchFingerType): The finger identifier for the touch action.
        """
        self._mouse_actions.pointer_down(FINGERS_MAP[finger])

    def touch_up(self, finger: TouchFingerType):
        """
        Simulate a touch up action by mapping it to a mouse up action using the specified finger.

        Parameters:
            finger (TouchFingerType): The finger identifier for the touch action.
        """
        self._mouse_actions.pointer_down(FINGERS_MAP[finger])

    def touch_move(self, x: float, y: float):
        """
        Simulate a touch move action by mapping it to a mouse move action.

        Parameters:
            x (float): The x-coordinate to move the pointer to.
            y (float): The y-coordinate to move the pointer to.
        """
        self._touch_actions.move_to_location(x, y)

    def move_to(self, x: float, y: float):
        """
        Move the pointer to the specified x, y coordinates.
        This action is typically handled at the upper abstraction layer.
        """
        self._mouse_actions.move_to_location(x, y)

    # Keyboard actions
    def key_down(self, key: str):
        """
        Simulate a key down action.

        Parameters:
            key (str): The key to press down.
        """
        self.action_builder.key_action.key_down(key)

    def key_up(self, key: str):
        """
        Simulate a key up action.

        Parameters:
            key (str): The key to release.
        """
        self.action_builder.key_action.key_up(key)

    def wait(self, milliseconds: float):
        self._mouse_actions.pause(milliseconds)
        self._touch_actions.pause(milliseconds)

    # Perform all actions
    def perform(self):
        """
        Perform all actions that have been built using the Selenium ActionBuilder instance.
        """
        self.action_builder.perform()
