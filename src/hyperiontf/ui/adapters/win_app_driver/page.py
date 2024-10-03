import copy
from typing import Dict, Any, List
from hyperiontf.typing import (
    WIN_APP_DRIVER_ROOT_HANDLE,
    APPIUM_DEFAULT_URL,
    HyperionException,
)
from hyperiontf.ui import By
from hyperiontf.ui.adapters.win_app_driver.bridge import Bridge
from hyperiontf.ui.adapters.win_app_driver.element import Element
from hyperiontf.ui.adapters.win_app_driver.action_builder import WinActionBuilder
import hyperiontf.ui.adapters.win_app_driver.command as command
import base64
import urllib.parse


class Page:

    @staticmethod
    def launch_app(caps: dict):
        desired_cap = copy.deepcopy(caps)
        if "remote_url" in desired_cap.keys():
            hub_url = desired_cap.pop("remote_url")
        else:
            hub_url = APPIUM_DEFAULT_URL
        # just delete it as it's a framework specific
        desired_cap.pop("automation")
        desired_cap.pop("automationName")

        return Page(hub_url, desired_cap)

    def __init__(self, url: str, capabilities: Dict[str, Any]):
        """
        Initialize the WinAppDriver with the provided URL and capabilities.

        :param url: The URL where the WinAppDriver server is running.
        :param capabilities: A dictionary of capabilities for the WinAppDriver session.
        """
        parsed_url = urllib.parse.urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port

        self.caps = capabilities

        # Use default port 4723 if no port is specified in the URL
        self.bridge = Bridge(url=host, port=port or 4723)
        self.session_id = self._create_session(capabilities)

    def _create_session(self, capabilities: Dict[str, Any]) -> str:
        """
        Create a new session with the provided capabilities.

        :param capabilities: A dictionary of capabilities for the session.
        :return: The session ID for the new session.
        """
        response = self.bridge.execute(command.session.new, {}, capabilities)
        return response["sessionId"]

    @property
    def window_handle(self) -> str:
        """
        Get the current window handle. If no handle is present (i.e., for 'Root'), return WIN_APP_DRIVER_ROOT_HANDLE.
        """
        try:
            handle = self.bridge.execute(
                command.window.handle, {"sessionId": self.session_id}
            )
            return handle if handle else WIN_APP_DRIVER_ROOT_HANDLE
        except HyperionException:
            return WIN_APP_DRIVER_ROOT_HANDLE

    @property
    def action_builder(self) -> WinActionBuilder:
        return WinActionBuilder(self.bridge)

    @property
    def window_handles(self) -> List[str]:
        """
        Get all window handles. If no handles are present, return a list with WIN_APP_DRIVER_ROOT_HANDLE.
        """
        handles = self.bridge.execute(
            command.window.handles, {"sessionId": self.session_id}
        )
        if not handles:
            handles = [WIN_APP_DRIVER_ROOT_HANDLE]
        return handles

    def find_element(self, locator: By) -> Element:
        """
        Find a single element using the provided locator.

        :param locator: The locator object (By) for finding the element.
        :return: An Element instance representing the found element.
        """
        return Element(
            self.bridge.execute(
                command.element.find_element,
                {"sessionId": self.session_id},
                {"using": locator.by, "value": locator.value},
            ),
            self.bridge,
        )

    def find_elements(self, locator: By) -> List[Element]:
        """
        Find multiple elements using the provided locator.

        :param locator: The locator object (By) for finding the elements.
        :return: A list of Element instances representing the found elements.
        """
        elements = self.bridge.execute(
            command.element.find_elements,
            {"sessionId": self.session_id},
            {"using": locator.by, "value": locator.value},
        )
        return [Element(element["ELEMENT"], self.bridge) for element in elements]

    def open(self, url: str):
        """
        Open the specified URL in the WinAppDriver session.

        :param url: The URL to navigate to.
        """
        self.bridge.execute(
            {"method": "POST", "endpointTemplate": "/session/{sessionId}/url"},
            {"sessionId": self.session_id},
            {"url": url},
        )

    @property
    def title(self) -> str:
        """Retrieve the title of the current window."""
        return self.bridge.execute(command.driver.title, {"sessionId": self.session_id})

    @property
    def url(self) -> str:
        """Retrieve the current URL of the session."""
        return self.caps["app"]

    def switch_to_default_content(self):
        """Switch back to the default content (main frame)."""
        pass

    def switch_to_iframe(self, iframe: Element):
        """Switch to the specified iframe."""
        pass

    def switch_to_window(self, handle: str):
        """Switch to a specific window by its handle."""
        self.bridge.execute(
            command.window.new_window,
            {"sessionId": self.session_id},
            {"handle": handle},
        )

    def close(self):
        """Close the current window."""
        self.bridge.execute(
            command.window.delete_window, {"sessionId": self.session_id}
        )

    def quit(self):
        """End the WinAppDriver session."""
        self.bridge.execute(command.session.delete, {"sessionId": self.session_id})

    def execute_script(self, script: str, *args: Any) -> Any:
        """
        Execute JavaScript or a similar script in the current context.

        :param script: The script to execute.
        :param args: Any arguments to pass to the script.
        :return: The result of the script execution.
        """
        pass

    @property
    def screenshot_as_base64(self) -> str:
        """Take a screenshot of the current window and return it as a base64 string."""
        return self.bridge.execute(
            command.driver.screenshot, {"sessionId": self.session_id}
        )

    def screenshot(self, path: str) -> None:
        """
        Save a screenshot to the specified file path.

        :param path: The file path to save the screenshot.
        """
        base64_image = self.screenshot_as_base64
        with open(path, "wb") as file:
            file.write(base64.b64decode(base64_image))

    @property
    def page_source(self) -> str:
        """Retrieve the page source of the current window."""
        return self.bridge.execute(
            command.driver.source, {"sessionId": self.session_id}
        )

    @property
    def size(self) -> Dict[str, int]:
        """Retrieve the size (width and height) of the window."""
        return self.bridge.execute(command.window.size, {"sessionId": self.session_id})

    @property
    def location(self) -> Dict[str, int]:
        """Retrieve the location (x and y coordinates) of the window."""
        return self.bridge.execute(
            command.window.get_position, {"sessionId": self.session_id}
        )

    @property
    def rect(self) -> Dict[str, int]:
        """Retrieve the rectangle (location and size) of the window."""
        location = self.location
        size = self.size
        return {**location, **size}

    def set_window_size(self, width: int, height: int):
        """Set the size of the current window."""
        self.bridge.execute(
            command.window.set_size,
            {"sessionId": self.session_id},
            {"width": width, "height": height},
        )

    def set_window_location(self, x: int, y: int):
        """Set the location of the current window."""
        self.bridge.execute(
            command.window.set_position,
            {"sessionId": self.session_id},
            {"x": x, "y": y},
        )

    def set_window_rect(self, x: int, y: int, width: int, height: int):
        """Set the rectangle (size and position) of the current window."""
        self.bridge.execute(
            command.window.set_window_handle_size,
            {"sessionId": self.session_id},
            {"x": x, "y": y, "width": width, "height": height},
        )

    def dump(self) -> List[Dict[str, str]]:
        """
        Capture and return screenshots and page sources for each window.
        This is typically used for debugging and logging.
        """
        attachments = []

        for index, window in enumerate(self.window_handles):
            if window != WIN_APP_DRIVER_ROOT_HANDLE:
                self.switch_to_window(window)

            base_64_img_URL = f"data:image/png;base64,{self.screenshot_as_base64}"
            attachments.append(
                {
                    "title": f"Window {index + 1} screenshot",
                    "type": "image",
                    "url": base_64_img_URL,
                }
            )

            base_64_src_url = (
                f"data:text/xml;base64,"
                f"{base64.b64encode(self.page_source.encode('utf-8')).decode('utf-8')}"
            )
            attachments.append(
                {
                    "title": f"Window {index + 1} page source",
                    "type": "html",
                    "url": base_64_src_url,
                }
            )

        return attachments
