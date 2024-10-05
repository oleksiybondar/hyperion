import hyperiontf.ui.adapters.win_app_driver.command as command
from hyperiontf.typing import MouseButtonType, MouseButton, TouchFingerType, TouchFinger
import time

# Mouse and Touch Value Maps for Selenium Compatibility
MOUSE_BUTTON_MAP = {
    MouseButton.LEFT: 0,
    MouseButton.MIDDLE: 1,
    MouseButton.RIGHT: 2,
    MouseButton.BACK: 3,
    MouseButton.FORWARD: 4,
}

TOUCH_FINGER_MAP = {
    TouchFinger.ONE: 1,
    TouchFinger.TWO: 2,
    TouchFinger.THREE: 3,
    TouchFinger.FOUR: 4,
    TouchFinger.FIVE: 5,
}


class WinActionBuilder:
    """
    WinActionBuilder handles mouse, touch, keyboard, and custom actions for WindowsApplicationDriver.
    It uses a bridge to communicate with the client and pushes actions to a stack, which is executed when perform() is called.
    """

    def __init__(self, bridge):
        """
        Initialize the WinActionBuilder with a bridge instance.

        Parameters:
            bridge: A bridge instance to execute commands and handle communication with the client.
        """
        self.bridge = bridge  # Bridge instance for communication
        self.actions_stack = []  # Stack to store actions and their payloads

    def _add_action(self, cmd, payload=None):
        """
        Add an action to the actions stack.

        Parameters:
            cmd: The command (either a dictionary or a string) to be executed.
            payload: The payload containing parameters for the command (default: None).
        """
        if payload is None:
            payload = {}
        self.actions_stack.append((cmd, payload))

    def _get_default_params(self):
        """
        Get the default parameters including the session ID from the bridge.

        Returns:
            dict: A dictionary with default params including the session ID.
        """
        return {"sessionId": self.bridge.session_id}

    # Mouse actions
    def mouse_down(self, button: MouseButtonType):
        """
        Simulate a mouse down action on the specified button.

        Parameters:
            button (MouseButtonType): The mouse button to press (default: 'left').
        """
        payload = {"button": MOUSE_BUTTON_MAP[button]}
        self._add_action(command.mouse.button_down, payload)

    def mouse_up(self, button: MouseButtonType = MouseButton.LEFT):
        """
        Simulate a mouse up action on the specified button.

        Parameters:
            button (MouseButtonType): The mouse button to release (default: 'left').
        """
        payload = {"button": MOUSE_BUTTON_MAP[button]}
        self._add_action(command.mouse.button_up, payload)

    def move_to(self, x: float, y: float):
        """
        Move the mouse to the specified x, y coordinates.

        Parameters:
            x (float): The x-coordinate to move the mouse to.
            y (float): The y-coordinate to move the mouse to.
        """
        payload = {"x": x, "y": y}
        self._add_action(command.mouse.moveto, payload)

    # Keyboard actions
    def key_down(self, key: str):
        """
        Simulate a key down action.

        Parameters:
            key (str): The key to press down.
        """
        payload = {"value": key}
        self._add_action(command.keyboard.keys, payload)

    def key_up(self, key: str):
        """
        Simulate a key up action.

        Parameters:
            key (str): The key to release.
        """
        payload = {"value": key}
        self._add_action(command.keyboard.keys, payload)

    # Touch actions
    def touch_down(
        self,
        finger: TouchFingerType,
        x: float,
        y: float,
    ):
        """
        Simulate a touch down action at the specified coordinates with the specified finger.

        Parameters:
            finger (TouchFingerType): The finger identifier (default: 'one').
            x (float): The x-coordinate for the touch down action (optional).
            y (float): The y-coordinate for the touch down action (optional).
        """
        payload = {"finger": TOUCH_FINGER_MAP[finger], "x": x, "y": y}
        self._add_action(command.touch.down, payload)

    def touch_up(
        self,
        finger: TouchFingerType,
        x: float,
        y: float,
    ):
        """
        Simulate a touch up action at the specified coordinates with the specified finger.

        Parameters:
            finger (TouchFingerType): The finger identifier (default: 'one').
            x (float): The x-coordinate for the touch up action (optional).
            y (float): The y-coordinate for the touch up action (optional).
        """
        payload = {"finger": TOUCH_FINGER_MAP[finger], "x": x, "y": y}
        self._add_action(command.touch.up, payload)

    def touch_move(
        self,
        finger: TouchFingerType,
        x: float,
        y: float,
    ):
        """
        Simulate a touch move action to the specified coordinates with the specified finger.

        Parameters:
            finger (TouchFingerType): The finger identifier (default: 'one').
            x (float): The x-coordinate for the touch move action (optional).
            y (float): The y-coordinate for the touch move action (optional).
        """
        payload = {"finger": TOUCH_FINGER_MAP[finger], "x": x, "y": y}
        self._add_action(command.touch.move, payload)

    # Wait action (custom implementation)
    def wait(self, milliseconds):
        """
        Wait for the specified amount of time.

        Parameters:
            milliseconds (int): The time to wait in milliseconds.
        """
        self._add_action("wait", {"milliseconds": milliseconds})

    def _execute_command(self, cmd, payload):
        """
        Execute the command using the bridge.

        Parameters:
            cmd (dict or str): The command to execute. If it's a dictionary, it's assumed to be a WinAppDriver API command.
                               If it's a string, it's assumed to be a custom method.
            payload (dict): The payload associated with the command.
        """
        if isinstance(cmd, dict):
            # If command is a dictionary, it's a WinAppDriver command
            self.bridge.execute(cmd, self._get_default_params(), payload)
        else:
            # If command is a string, it's a custom method
            if cmd == "wait":
                self._wait(payload["milliseconds"])

    @staticmethod
    def _wait(milliseconds):
        """
        Custom wait implementation.

        Parameters:
            milliseconds (int): Time to wait in milliseconds.
        """
        time.sleep(milliseconds / 1000)

    def perform(self):
        """
        Perform all actions in the actions stack.

        This method iterates over the actions stack and executes each action using the bridge or a custom method.
        """
        for cmd, payload in self.actions_stack:
            self._execute_command(cmd, payload)
        self.actions_stack = []  # Clear the actions stack after execution
