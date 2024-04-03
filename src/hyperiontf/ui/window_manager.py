from typing import Optional, Union
from hyperiontf.logging import getLogger, Logger
from .automation_adapter_manager import AutomationAdaptersManager
from hyperiontf.typing import AnyPageObject, LoggerSource


class WindowManager:
    """
    A class designed to manage window activation/switching. It ensures robustness, simplicity, and scalability.

    It utilizes static instances for maintaining a current window handle tied to an application instance. It allows
    each page with its own WindowManager instance to verify the linked page's active status, minimizing time-consuming
    API calls to the driver wrapped by the automation adapter. API calls are only triggered when needed.
    """

    def __init__(
        self,
        owner: AnyPageObject,
        logger: Logger = getLogger(LoggerSource.PAGE_OBJECT),
        window_handle: Optional[str] = None,
    ) -> None:
        """
        Initialize the WindowManager object.

        :param owner: The owner of the WindowManager which could be a WebPage, WebView, MobileScreen, or DesktopWindow.
        :param logger: The logger to use for logging events.
        :param window_handle: The window handle for the instance.
        """
        self.owner = owner
        self.logger = logger
        self.adapters_manager = AutomationAdaptersManager()
        self.window_handle = window_handle
        self._update_window_handle()

    @property
    def _current_window_handle(self) -> str:
        return self.adapters_manager.get_meta(
            self.owner.automation_adapter, "current_window_handle"
        )

    @_current_window_handle.setter
    def _current_window_handle(self, handle: Union[str | None]):
        self.adapters_manager.set_meta(
            self.owner.automation_adapter, "current_window_handle", handle
        )

    def _update_window_handle(self):
        """
        Updates the window handle of the current WindowManager instance. If the window handle is not provided during
        initialization, it attempts to use the handle from the associated automation instance. If that's not available,
        it fetches the handle using the _fetch_window_handle() method.
        """
        if (
            self.window_handle
        ):  # if window handle is already defined, no need for update
            return

        # try to update from the current window handle of the automation instance
        if self._current_window_handle is not None:
            self.window_handle = self._current_window_handle
            return

        # if the automation instance does not have a window handle, fetch the handle
        self.window_handle = self._fetch_window_handle()
        self._current_window_handle = self.window_handle

    def _fetch_window_handle(self):
        """
        Fetch the current window handle.

        :return: The current window handle.
        """
        handle = self.owner.automation_adapter.window_handle
        self.logger.debug(
            f"[{self.owner.__full_name__}] Retrieved the current window handle: {handle}"
        )
        return handle

    def is_active(self) -> bool:
        """
        Check if the current window is active.

        :return: True if the window is active, False otherwise.
        """
        return self._current_window_handle == self.window_handle

    def activate(self) -> None:
        """
        Activates the window if it's not currently active.
        """
        if not self.is_active():
            self.logger.debug(
                f"[{self.owner.__full_name__}] Activating the window with handle: {self.window_handle}"
            )
            self.owner.automation_adapter.switch_to_window(self.window_handle)
            self._current_window_handle = self.window_handle  # type: ignore

    def move(self, x: int, y: int):
        """
        Moves the window to a new location.

        This method first ensures the window is active before moving it to the specified coordinates.

        :param x: The horizontal position (in pixels) where the window should be moved to.
        :param y: The vertical position (in pixels) where the window should be moved to.
        """
        self.activate()
        self.logger.info(
            f"[{self.owner.__full_name__}] Mowing the window to: x: {x}, y: {y}"
        )
        self.owner.automation_adapter.set_window_location(x, y)
        self.location = {"x": x, "y": y}

    def resize(self, width: int, height: int):
        """
        Resizes the window to the specified dimensions.

        This method first activates the window if it is not already active, then resizes it to the specified width and height.

        :param width: The new width (in pixels) for the window.
        :param height: The new height (in pixels) for the window.
        """
        self.activate()
        self.logger.info(
            f"[{self.owner.__full_name__}] Resizing the window to: x: {width}, y: {height}"
        )
        self.owner.automation_adapter.set_window_size(width, height)
        self.size = {"width": width, "height": height}

    @property
    def location(self):
        """
        Gets the current location of the window.

        This property retrieves the current location of the window, including its x and y coordinates in pixels. If the location is not already known, it fetches the location from the automation adapter and caches it.

        :return: A dictionary with keys 'x' and 'y' representing the location of the window in pixels.
        """
        current_location = self.adapters_manager.get_meta(
            self.owner.automation_adapter, "current_window_location"
        )
        if current_location:
            return current_location

        current_location = self.owner.automation_adapter.location
        self.logger.debug(
            f"[{self.owner.__full_name__}"
            f"[{self.owner.__full_name__}] Fetching window location: x: {current_location['x']}, y: {current_location['y']}"
        )
        self.location = current_location
        return current_location

    @location.setter
    def location(self, new_location):
        """
        Sets the current location of the window.

        This method updates the window's location using the automation adapter and caches the new location.

        :param new_location: A dictionary with keys 'x' and 'y' representing the new location of the window in pixels.
        """
        self.adapters_manager.set_meta(
            self.owner.automation_adapter, "current_window_location", new_location
        )

    @property
    def size(self):
        """
        Gets the current size of the window.

        This property retrieves the current size of the window, including its width and height in pixels. If the size is not already known, it fetches the size from the automation adapter and caches it.

        :return: A dictionary with keys 'width' and 'height' representing the size of the window in pixels.
        """
        current_size = self.adapters_manager.get_meta(
            self.owner.automation_adapter, "current_window_size"
        )
        if current_size:
            return current_size

        current_size = self.owner.automation_adapter.size

        self.logger.debug(
            f"[{self.owner.__full_name__}"
            f"[{self.owner.__full_name__}] Fetching window size: width: {current_size['width']}, height: {current_size['height']}"
        )
        self.size = current_size
        return current_size

    @size.setter
    def size(self, new_size):
        """
        Sets the current size of the window.

        This method updates the window's size using the automation adapter and caches the new size.

        :param new_size: A dictionary with keys 'width' and 'height' representing the new size of the window in pixels.
        """
        self.adapters_manager.set_meta(
            self.owner.automation_adapter, "current_window_size", new_size
        )
