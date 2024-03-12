from typing import Any, Optional, cast
from hyperiontf.typing import ViewportLabel, LoggerSource, ViewportLabelType
from hyperiontf.logging import Logger, getLogger
from hyperiontf.configuration import config
from .automation_adapter_manager import AutomationAdaptersManager


class ViewportManager:
    def __init__(
        self, owner: Any, logger: Logger = getLogger(LoggerSource.PAGE_OBJECT)
    ):
        """
        Construct a ViewportManager.

        Parameters:
            owner (Any): The owner object, which can be a WebPage, MobileScreen, DesktopWindow, etc.
            logger: The logger to use for logging events.
        """
        self.adapters_manager = AutomationAdaptersManager()
        self.owner = owner
        self.logger = logger
        self._viewport_label: Optional[ViewportLabelType] = None

    @property
    def current_viewport(self) -> ViewportLabelType:
        """
        Retrieve the current viewport. If the viewport is not set, it calculates a new one.

        Returns:
            ViewportLabel: The current viewport label.
        """
        if self._is_page_object:
            self._viewport_label = self.adapters_manager.get_meta(
                self.owner.automation_adapter, "current_viewport"
            )

        if self._viewport_label is None:
            self.calculate_viewport()

        return cast(ViewportLabelType, self._viewport_label)

    @property
    def size(self):
        current_size = self.adapters_manager.get_meta(
            self._adapter, "current_document_size"
        )
        if current_size is not None:
            return current_size

        current_size = self._get_document_size()
        self.logger.debug(
            f"[{self.owner.__full_name__}"
            f"[{self.owner.__full_name__}] Fetching document size: width: {current_size['width']}, height: {current_size['height']}"
        )
        self.size = current_size
        return current_size

    @size.setter
    def size(self, new_size):
        """
        updates the current size of the document.
        """
        self.adapters_manager.set_meta(self._adapter, "current_document_size", new_size)

    @property
    def device_pixel_ratio(self):
        """
        Retrieve the device pixel ratio (DPR) for the current environment.

        This property first attempts to get the DPR from previously stored metadata. If not available,
        it executes a JavaScript command via the automation adapter to obtain the window's device pixel ratio.
        The retrieved DPR is then stored as metadata for future access to avoid repeated JS execution.

        Returns:
            float: The device pixel ratio. Returns 1.0 if the DPR cannot be determined, ensuring
                   there's always a fallback value for further calculations.

        """
        pixel_ratio = self.adapters_manager.get_meta(
            self.owner.root.automation_adapter, "device_pixel_ratio"
        )

        if pixel_ratio:
            return pixel_ratio

        pixel_ratio = (
            self.owner.root.automation_adapter.execute_script(
                "return window.devicePixelRatio"
            )
            or 1.0
        )
        self.logger.debug(
            f"[{self.owner.__full_name__}"
            f"[{self.owner.__full_name__}] Fetching device pixel ratio: {pixel_ratio}"
        )

        self.adapters_manager.set_meta(
            self.owner.root.automation_adapter, "pixel_ratio", pixel_ratio
        )
        return pixel_ratio

    @staticmethod
    def _get_viewport_label(width: int) -> ViewportLabelType:
        """
        Determine the viewport label based on a given width by initiating a chain of
        viewport size checks starting from the smallest size.

        Parameters:
            width (int): The input width for which the viewport label is to be determined.

        Returns:
            ViewportLabel: The corresponding viewport label for the given width.
        """
        return ViewportManager._viewport_xs_or_larger(width)

    @staticmethod
    def _viewport_xs_or_larger(width: int) -> ViewportLabelType:
        """
        Check if the width qualifies for 'XS' viewport label, otherwise delegate to
        the next larger viewport size check.

        Parameters:
            width (int): The width to be checked against the 'XS' viewport size.

        Returns:
            ViewportLabel: The viewport label for the given width.
        """
        if width < config.page_object.viewport_sm:
            return ViewportLabel.XS

        return ViewportManager._viewport_sm_or_larger(width)

    @staticmethod
    def _viewport_sm_or_larger(width: int) -> ViewportLabelType:
        """
        Check if the width qualifies for 'SM' viewport label, otherwise delegate to
        the next larger viewport size check.

        Parameters:
            width (int): The width to be checked against the 'SM' viewport size.

        Returns:
            ViewportLabel: The viewport label for the given width.
        """
        if width < config.page_object.viewport_md:
            return ViewportLabel.SM

        return ViewportManager._viewport_md_or_larger(width)

    @staticmethod
    def _viewport_md_or_larger(width: int) -> ViewportLabelType:
        """
        Check if the width qualifies for 'MD' viewport label, otherwise delegate to
        the next larger viewport size check.

        Parameters:
            width (int): The width to be checked against the 'SM' viewport size.

        Returns:
            ViewportLabel: The viewport label for the given width.
        """
        if width < config.page_object.viewport_lg:
            return ViewportLabel.MD

        return ViewportManager._viewport_lg_or_larger(width)

    @staticmethod
    def _viewport_lg_or_larger(width: int) -> ViewportLabelType:
        """
        Check if the width qualifies for 'LG' viewport label, otherwise delegate to
        the next larger viewport size check.

        Parameters:
            width (int): The width to be checked against the 'LG' viewport size.

        Returns:
            ViewportLabel: The viewport label for the given width.
        """
        if width < config.page_object.viewport_xl:
            return ViewportLabel.LG

        return ViewportManager._viewport_xl_or_larger(width)

    @staticmethod
    def _viewport_xl_or_larger(width: int) -> ViewportLabelType:
        """
        Check if the width qualifies for 'XL' viewport label, otherwise default to
        the largest viewport label 'XXL'.

        Parameters:
            width (int): The width to be checked against the 'XL' viewport size.

        Returns:
            ViewportLabel: The viewport label for the given width.
        """
        if width < config.page_object.viewport_xxl:
            return ViewportLabel.XL

        return ViewportLabel.XXL

    def calculate_viewport(
        self, force_recalculation: bool = False
    ) -> ViewportLabelType:
        """
        Calculate and set the viewport. If 'force_recalculation' is set to True, or if the viewport
        label is None, then a new viewport is calculated.

        Parameters:
            force_recalculation (bool): Flag indicating whether to forcefully recalculate the viewport.

        Returns:
            ViewportLabel: The calculated viewport label.
        """
        if force_recalculation or self._viewport_label is None:
            self.size = self._get_document_size()
            self._viewport_label = self._get_viewport_label(self.width)
            self.logger.debug(
                f"[{self.owner.__full_name__}] Resolved document viewport: {self._viewport_label}"
            )

            if self._is_page_object:
                self.adapters_manager.set_meta(
                    self._adapter,
                    "current_viewport",
                    self._viewport_label,
                )

        return self._viewport_label

    def set_viewport(self, viewport: ViewportLabelType):
        """
        Set the viewport to a specified size.

        This method adjusts the size of the viewport based on a given viewport label.
        It retrieves the default resolution for the specified viewport and resizes the window
        to match that resolution.

        Parameters:
            viewport (ViewportLabelType): The viewport label indicating the target viewport size.
        """
        needed_size = self._get_default_viewport_size(viewport)
        self.resize(needed_size["width"], needed_size["height"])

    @staticmethod
    def _get_default_viewport_size(viewport: ViewportLabelType) -> dict:
        """
        Retrieve the default size for a given viewport label.

        This static method accesses configuration to get the default resolution associated with a specified viewport label.
        It's used to determine the width and height that correspond to a viewport label, facilitating operations like resizing.

        Parameters:
            viewport (ViewportLabelType): The viewport label for which to retrieve the default size.

        Returns:
            dict: A dictionary with 'width' and 'height' keys indicating the default size for the given viewport label.
        """
        attr_name = f"default_{viewport}_resolution"
        resolution = getattr(config.page_object, attr_name)
        parts = resolution.split("x")
        return {"width": int(parts[0]), "height": int(parts[1])}

    def resize(self, width: int, height: Optional[int] = None) -> None:
        """
        Resize the window to specified dimensions.

        This method resizes the window to the given width and height. If the height is not specified,
        it maintains the current height. It also accounts for any offsets (like toolbars or window borders)
        to ensure the content area matches the specified dimensions.

        Parameters:
            width (int): The target width for the window.
            height (Optional[int]): The target height for the window. If None, the current height is maintained.
        """
        window_size = self._calculate_window_size(width, height)

        self.owner.root.window_manager.resize(
            window_size["width"], window_size["height"]
        )
        self.calculate_viewport(True)

    def _calculate_window_size(self, width: int, height: Optional[int]) -> dict:
        """
        Calculate the size of the window including offsets.

        This method calculates the size that the window needs to be set to, taking into account
        the desired content size and any offsets that exist (e.g., for toolbars, scrollbars, or window borders).
        It's used when resizing the window to ensure the content area matches the specified dimensions.

        Parameters:
            width (int): The desired width of the content area.
            height (Optional[int]): The desired height of the content area. If None, it defaults to the current content height.

        Returns:
            dict: A dictionary with 'width' and 'height' keys indicating the total window size needed to achieve the desired content size.
        """
        offset_size = self.window_offset_size
        if height is None:
            height = self.height
        return {
            "width": width + offset_size["width"],
            "height": height + offset_size["height"],
        }

    @property
    def window_offset_size(self) -> dict:
        """
        Get the size of window offsets like toolbars and window borders.

        This property retrieves the size differences between the outer window dimensions and the
        dimensions of the viewport/document. It's used to accurately resize the window so that the
        document matches the desired size.

        Returns:
            dict: A dictionary containing the width and height offsets of the window.
        """
        offset_size = self.adapters_manager.get_meta(
            self.owner.root, "window_offset_size"
        )
        if offset_size is not None:
            return offset_size

        offset_size = self._calculate_window_offset_size()
        self.adapters_manager.set_meta(
            self.owner.root, "window_offset_size", offset_size
        )
        return offset_size

    def _calculate_window_offset_size(self) -> dict:
        """
        Calculate the window offset size.

        This internal method calculates the difference between the window size and the document size,
        providing the offsets due to toolbars, borders, and other non-document UI elements. It's used
        to help adjust window sizes accurately when resizing.

        Returns:
            dict: A dictionary with 'width' and 'height' keys indicating the offset sizes.
        """
        current_window_size = self.owner.root.window_manager.size
        current_document_size = self.size

        return {
            "width": current_window_size["width"] - current_document_size["width"],
            "height": current_window_size["height"] - current_document_size["height"],
        }

    @property
    def _is_page_object(self):
        """
        Determine if the owner object is a recognized page object type.

        This checks if the owner is an instance of one of the known page object classes,
        which include WebPage, MobileScreen, and DesktopWindow. This property is used internally
        to tailor behavior based on the type of the owner object.

        Returns:
            bool: True if the owner is an instance of a recognized page object type, False otherwise.
        """
        from hyperiontf.ui.webpage import WebPage
        from hyperiontf.ui.mobile_screen import MobileScreen
        from hyperiontf.ui.desktop_window import DesktopWindow

        return isinstance(self.owner, (WebPage, MobileScreen, DesktopWindow))

    @property
    def _is_web(self) -> bool:
        """
        Check if the owner object is a web page.

        Determines if the owner of this viewport manager is an instance of the WebPage class,
        indicating that the current context is a web environment.

        Returns:
            bool: True if the owner is a WebPage instance, False otherwise.
        """
        from hyperiontf.ui.webpage import WebPage

        return isinstance(self.owner, WebPage)

    @property
    def _is_mobile(self) -> bool:
        """
        Check if the owner object is a mobile screen.

        Determines if the owner of this viewport manager is an instance of the MobileScreen class,
        indicating that the current context is a mobile environment.

        Returns:
            bool: True if the owner is a MobileScreen instance, False otherwise.
        """
        from hyperiontf.ui.mobile_screen import MobileScreen

        return isinstance(self.owner, MobileScreen)

    @property
    def _is_desktop(self) -> bool:
        """
        Check if the owner object is a desktop window.

        Determines if the owner of this viewport manager is an instance of the DesktopWindow class,
        indicating that the current context is a desktop environment.

        Returns:
            bool: True if the owner is a DesktopWindow instance, False otherwise.
        """
        from hyperiontf.ui.desktop_window import DesktopWindow

        return isinstance(self.owner, DesktopWindow)

    @property
    def _adapter(self):
        """
        Get the appropriate automation adapter based on the owner's environment.

        This property determines the correct automation adapter to use based on the owner's
        environment (web, mobile, or desktop). If the owner is a web page object, it returns
        the web automation adapter. Otherwise, it defaults to the root automation adapter.

        Returns:
            The automation adapter corresponding to the owner's environment.
        """
        if self._is_web:
            return self.owner.automation_adapter

        return self.owner.root.automation_adapter

    def _get_document_size(self) -> dict:
        """
        Get the size of the document based on the owner's environment.

        This method determines the document size by checking the owner's environment and calling
        the appropriate method to fetch the document size for web, mobile, or desktop environments.

        Returns:
            dict: A dictionary containing the width and height of the document.
        """
        if self._is_web:
            return self._get_web_document_size()
        elif self._is_mobile:
            return self._get_mobile_document_size()
        elif self._is_desktop:
            return self._get_desktop_document_size()
        else:
            # In case it is a component, we revert to web document size
            return self._get_web_document_size()

    def _get_web_document_size(self) -> dict:
        """
        Get the document size for a mobile environment.

        This method is designed for retrieving the document size in a mobile environment.
        It works correctly for iOS but may not return accurate results for Android. For Android,
        a different approach that accounts for device pixel ratio might be necessary.

        Returns:
            dict: A dictionary containing the width and height of the document in a mobile environment.
        """
        script = "return {width: document.body.clientWidth, height: document.body.clientHeight};"
        return self._adapter.execute_script(script)

    def _get_mobile_document_size(self):
        """
        Get the document size for a mobile environment.

        This method is designed to retrieve the document size in mobile environments. It is currently
        optimized for iOS devices, where it can accurately determine the document size. However, for
        Android devices, the method may not return precise dimensions due to differences in how document
        sizes are calculated without considering the device pixel ratio (DPR).

        TODO: Improve Android support by incorporating device pixel ratio adjustments or utilizing
        a more suitable method for fetching document dimensions that accurately reflects the
        visible content area on Android devices.

        Returns:
            dict: A dictionary containing the width and height of the document in a mobile environment.
                  For Android, these values may represent the physical screen size rather than the adjusted
                  content area.
        """
        return self._adapter.get_window_size()

    def _get_desktop_document_size(self):
        """
        Get the size of the document in a desktop environment.

        This method retrieves the size of the window for desktop applications. It's relevant when the viewport manager
        is used in the context of desktop applications, ensuring that operations considering the document size
        are based on the actual size of the application window.

        Returns:
            dict: A dictionary containing the width and height of the document (or application window) in a desktop environment.
        """
        return self._adapter.get_window_size()

    @property
    def width(self) -> int:
        """
        Get the width of the current document.

        This property retrieves the width of the document currently managed by the viewport manager.
        It's a convenience wrapper around the size property, providing direct access to the width.

        Returns:
            int: The width of the current document.
        """
        return self.size["width"]

    @property
    def height(self) -> int:
        """
        Get the height of the current document.

        This property retrieves the height of the document currently managed by the viewport manager.
        It's a convenience wrapper around the size property, providing direct access to the height.

        Returns:
            int: The height of the current document.
        """
        return self.size["height"]
