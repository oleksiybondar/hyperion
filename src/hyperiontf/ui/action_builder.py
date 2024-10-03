from hyperiontf.logging import getLogger
from hyperiontf.typing import (
    LoggerSource,
    MouseButtonType,
    MouseButton,
    TouchFingerType,
    TouchFinger,
    Element,
)
from hyperiontf.ui.decorators.action_builder_auto_log import auto_log

logger = getLogger(LoggerSource.ACTION_BUILDER)

DRAG_ACTION_TRIGGER_TIME = 250  # Time delay for drag actions in milliseconds


class ActionBuilder:
    """
    The ActionBuilder class provides methods to perform user interactions such as mouse actions,
    keyboard actions, and touch actions. It logs all performed actions and delegates execution
    to an adapter.

    Attributes:
        _builder_adapter: Adapter object responsible for executing the actions.
        _actions_log: List of logged actions.
        sender: Source identifier for logging purposes.
        logger: Logger instance for logging actions.
    """

    def __init__(self, builder_adapter):
        """
        Initialize the ActionBuilder with the given builder adapter.

        Parameters:
            builder_adapter: The adapter responsible for executing the actions. It must implement
                             the required methods used by the ActionBuilder.
        """
        self._builder_adapter = builder_adapter
        self._actions_log = []
        self.sender = LoggerSource.ACTION_BUILDER
        self.logger = logger

    def _log_action(self, action_name: str, details: dict):
        """
        Helper method to log each action performed.

        Parameters:
            action_name (str): Name of the action being performed.
            details (dict): Dictionary containing details about the action parameters.
        """
        log_entry = f"Action: {action_name}({details})"
        self._actions_log.append(log_entry)

    def _log_actions(self):
        """
        Logs all the actions that have been performed during the current sequence.
        """
        actions_string = "\n".join(self._actions_log)
        self.logger.info(
            f"[{self.sender}] Performing actions sequence:\n{actions_string}"
        )

    # Base mouse actions
    @auto_log
    def mouse_down(self, button: MouseButtonType):
        """
        Press down the specified mouse button.

        Parameters:
            button (MouseButtonType): The mouse button to press down. Should be an instance of
                                      MouseButtonType, e.g., MouseButton.LEFT, MouseButton.RIGHT, etc.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self._builder_adapter.mouse_down(button)

    @auto_log
    def mouse_up(self, button: MouseButtonType):
        """
        Release the specified mouse button.

        Parameters:
            button (MouseButtonType): The mouse button to release.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self._builder_adapter.mouse_up(button)

    @auto_log
    def mouse_move_to(self, x: float, y: float):
        """
        Move the mouse pointer to the specified coordinates.

        Parameters:
            x (float): The x-coordinate to move the mouse to.
            y (float): The y-coordinate to move the mouse to.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self._builder_adapter.move_to(x, y)

    # Base keyboard actions
    @auto_log
    def key_down(self, key: str):
        """
        Press down the specified key.

        Parameters:
            key (str): The key to press down. This should be a string representing the key.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self._builder_adapter.key_down(key)

    @auto_log
    def key_up(self, key: str):
        """
        Release the specified key.

        Parameters:
            key (str): The key to release.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self._builder_adapter.key_up(key)

    # Base touch actions
    @auto_log
    def touch_down(self, finger: TouchFingerType):
        """
        Simulate a touch down action with the specified finger.

        Parameters:
            finger (TouchFingerType): The finger to use for the touch action.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self._builder_adapter.touch_down(finger)

    @auto_log
    def touch_up(self, finger: TouchFingerType):
        """
        Simulate lifting the specified finger from a touch action.

        Parameters:
            finger (TouchFingerType): The finger to lift up.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self._builder_adapter.touch_up(finger)

    @auto_log
    def touch_move_to(self, x: float, y: float, finger: TouchFingerType):
        """
        Move the touch point to the specified coordinates using the specified finger.

        Parameters:
            x (float): The x-coordinate to move the touch point to.
            y (float): The y-coordinate to move the touch point to.
            finger (TouchFingerType): The finger to use for the touch move action.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self._builder_adapter.touch_move_to(finger, x, y)

    @auto_log
    def wait(self, milliseconds: int):
        """
        Wait for the specified amount of time.

        Parameters:
            milliseconds (int): The amount of time to wait in milliseconds.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self._builder_adapter.wait(milliseconds)

    def click(self):
        """
        Perform a left mouse click action.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self.mouse_down(MouseButton.LEFT)
        return self.mouse_up(MouseButton.LEFT)

    def right_click(self):
        """
        Perform a right mouse click action.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self.mouse_down(MouseButton.RIGHT)
        return self.mouse_up(MouseButton.RIGHT)

    def click_by(self, x: float, y: float):
        """
        Move the mouse to the specified coordinates and perform a left click.

        Parameters:
            x (float): The x-coordinate to move the mouse to.
            y (float): The y-coordinate to move the mouse to.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self.mouse_move_to(x, y)
        return self.click()

    def right_click_by(self, x: float, y: float):
        """
        Move the mouse to the specified coordinates and perform a right click.

        Parameters:
            x (float): The x-coordinate to move the mouse to.
            y (float): The y-coordinate to move the mouse to.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self.mouse_move_to(x, y)
        return self.right_click()

    def click_on_element(self, element: Element):
        """
        Click on the specified element.

        Parameters:
            element (Element): The element to click on.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        coordinates = self._extract_coordinates(element)
        return self.click_by(*coordinates)

    def right_click_on_element(self, element: Element):
        """
        Right click on the specified element.

        Parameters:
            element (Element): The element to click on.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        coordinates = self._extract_coordinates(element)
        return self.right_click_by(*coordinates)

    def tap(self):
        """
        Perform a tap action using one finger.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self.touch_down(TouchFinger.ONE)
        return self.touch_up(TouchFinger.ONE)

    def tap_by(self, x: float, y: float):
        """
        Move to the specified coordinates and perform a tap action.

        Parameters:
            x (float): The x-coordinate to move to.
            y (float): The y-coordinate to move to.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self.touch_move_to(x, y, TouchFinger.ONE)
        return self.tap()

    def tap_on_element(self, element: Element):
        """
        Tap on the specified element.

        Parameters:
            element (Element): The element to tap on.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        coordinates = self._extract_coordinates(element)
        return self.tap_by(*coordinates)

    def drag_and_drop_by(
        self, start_x: float, start_y: float, end_x: float, end_y: float
    ):
        """
        Perform a drag-and-drop action from the start coordinates to the end coordinates.

        Parameters:
            start_x (float): The starting x-coordinate.
            start_y (float): The starting y-coordinate.
            end_x (float): The ending x-coordinate.
            end_y (float): The ending y-coordinate.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self.mouse_move_to(start_x, start_y)
        self.mouse_down(MouseButton.LEFT)
        self.wait(DRAG_ACTION_TRIGGER_TIME)
        self.mouse_move_to(end_x, end_y)
        self.wait(DRAG_ACTION_TRIGGER_TIME)
        return self.mouse_up(MouseButton.LEFT)

    def drag_element_by(self, element: Element, end_x: float, end_y: float):
        """
        Drag the specified element by the given x and y offsets.

        Parameters:
            element (Element): The element to drag.
            end_x (float): The x-coordinate to move the mouse to.
            end_y (float): The y-coordinate to move the mouse to.
        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        start_x, start_y = self._extract_coordinates(element)
        return self.drag_and_drop_by(start_x, start_y, end_x, end_y)

    def drag_element_on_element(self, start_element: Element, end_element: Element):
        """
        Drag the start_element and drop it onto the end_element.

        Parameters:
            start_element (Element): The element to drag.
            end_element (Element): The element to drop onto.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        start_coordinates = self._extract_coordinates(start_element)
        end_coordinates = self._extract_coordinates(end_element)
        return self.drag_and_drop_by(*start_coordinates, *end_coordinates)

    @staticmethod
    def _extract_coordinates(element: Element):
        """
        Extract the center coordinates (x, y) of the given element.

        Parameters:
            element (Element): The element from which to extract coordinates.

        Returns:
            List[float]: A list containing the x and y coordinates of the element's center.
        """
        rect = element.get_rect(log=False)  # type: ignore
        center_x = rect["x"] + rect["width"] / 2
        center_y = rect["y"] + rect["height"] / 2
        return [center_x, center_y]

    def perform(self, log: bool = True):
        """
        Execute all the actions that have been added to the builder.

        Parameters:
            log (bool): Whether to log the action sequence. Defaults to True.

        Returns:
            ActionBuilder: Returns self to allow method chaining.
        """
        self._builder_adapter.perform()
        if log:
            self._log_actions()

        # Clear actions log after execution
        self._actions_log = []
        return self
