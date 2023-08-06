from typing import Optional
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
    def _current_window_handle(self):
        return self.adapters_manager.get_meta(
            self.owner.automation_adapter, "current_window_handle"
        )

    @_current_window_handle.setter
    def _current_window_handle(self, handle: str):
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
            self._current_window_handle = self.window_handle
