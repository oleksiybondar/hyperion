import base64
import hyperiontf.ui.adapters.win_app_driver.command as command
from typing import Dict, Any, List
from hyperiontf.ui import By


class Element:
    def __init__(self, element_id: str, bridge: Any):
        """
        Initialize the Element instance with an element_id and a bridge instance.

        :param element_id: The identifier of the element.
        :param bridge: The bridge instance used to execute command.
        """
        self.element_id = element_id
        self.bridge = bridge

    @property
    def _params(self) -> Dict[str, str]:
        """Return the default params for any command involving this element."""
        return {"sessionId": self.bridge.session_id, "elementId": self.element_id}

    # Properties for is_enabled, is_displayed, is_selected, location, size, rect

    @property
    def is_enabled(self) -> bool:
        """Check if the element is enabled."""
        return self.bridge.execute(command.element.enabled, self._params)

    @property
    def is_displayed(self) -> bool:
        """Check if the element is displayed."""
        return self.bridge.execute(command.element.displayed, self._params)

    @property
    def is_selected(self) -> bool:
        """Check if the element is selected (useful for checkboxes or options)."""
        return self.bridge.execute(command.element.selected, self._params)

    @property
    def location(self) -> Dict[str, int]:
        """Retrieve the location (x and y coordinates) of the element."""
        return self.bridge.execute(command.element.location, self._params)

    @property
    def location_once_scrolled_into_view(self) -> Dict[str, int]:
        """Retrieve the location of the element once it is scrolled into view."""
        return self.bridge.execute(command.element.location_in_view, self._params)

    @property
    def size(self) -> Dict[str, int]:
        """Retrieve the size (width and height) of the element."""
        return self.bridge.execute(command.element.size, self._params)

    @property
    def rect(self) -> Dict[str, int]:
        """Retrieve the rectangle (location and size) of the element."""
        location = self.location
        size = self.size
        return {**location, **size}

    @property
    def text(self) -> str:
        """Retrieve the text content of the element."""
        return self.bridge.execute(command.element.text, self._params)

    # Screenshot handling
    @property
    def screenshot_as_base64(self) -> str:
        """Get the screenshot of the element as a base64 string."""
        return self.bridge.execute(command.element.screenshot, self._params)

    def screenshot(self, path: str) -> None:
        """
        Save the screenshot of the element as a PNG file.

        :param path: The file path to save the screenshot.
        """
        base64_image = self.screenshot_as_base64
        with open(path, "wb") as file:
            file.write(base64.b64decode(base64_image))

    # Element interaction methods
    def click(self) -> Any:
        """Perform a click action on the element."""
        return self.bridge.execute(command.element.click, self._params)

    def clear(self) -> Any:
        """Clear the element (used typically for input fields)."""
        return self.bridge.execute(command.element.clear, self._params)

    def get_attribute(self, attribute_name: str) -> Any:
        """Retrieve a specific attribute value of the element."""
        params = {**self._params, "name": attribute_name}
        return self.bridge.execute(command.element.attribute, params)

    def send_keys(self, keys: str) -> Any:
        """Send keystrokes to the element (typically for input fields)."""
        payload = {"text": keys}
        return self.bridge.execute(command.element.send_keys, self._params, payload)

    # Methods for finding elements using the By locator object

    def find_element(self, locator: By) -> Any:
        """Find a child element inside the current element."""
        payload = {"using": locator.by, "value": locator.value}
        return self.bridge.execute(command.element.find_element, self._params, payload)

    def find_elements(self, locator: By) -> List[Any]:
        """Find all child elements inside the current element."""
        payload = {"using": locator.by, "value": locator.value}
        return self.bridge.execute(command.element.find_elements, self._params, payload)
