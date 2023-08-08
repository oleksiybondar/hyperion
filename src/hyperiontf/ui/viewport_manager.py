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
        self.adapter_manager = AutomationAdaptersManager()
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
            self._viewport_label = self.adapter_manager.get_meta(
                self.owner.automation_adapter, "current_viewport"
            )

        if self._viewport_label is None:
            self.calculate_viewport()

        return cast(ViewportLabelType, self._viewport_label)

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
        if width < config.page_object.viewport_lg:
            return ViewportLabel.SM

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
            document_width = self._get_document_width()
            self._viewport_label = self._get_viewport_label(document_width)
            self.logger.debug(
                f"[{self.owner.__full_name__}] Resolved document viewport: {self._viewport_label}"
            )

            if self._is_page_object:
                self.adapter_manager.set_meta(
                    self.owner.automation_adapter,
                    "current_viewport",
                    self._viewport_label,
                )

        return self._viewport_label

    def set_viewport(self, viewport: ViewportLabelType):
        """
        Set the viewport manually.

        Parameters:
            viewport (ViewportLabel): The viewport label to be set.
        """
        self._viewport_label = viewport
        if self._is_page_object:
            self.adapter_manager.set_meta(
                self.owner.automation_adapter, "current_viewport", self._viewport_label
            )

    def _get_web_document_width(self) -> int:
        """
        Determine the width of the document in a web context.

        Returns:
            int: The width of the document.
        """

        if self._is_web:
            width = self.owner.automation_adapter.execute_script(
                "return document.body.clientWidth;"
            )
        else:
            width = self.owner.root.automation_adapter.execute_script(
                "return document.body.clientWidth;"
            )
        self.logger.debug(
            f"[{self.owner.__full_name__}] Fetched document width: {width}"
        )
        if self._is_web:
            self.adapter_manager.set_meta(
                self.owner.automation_adapter, "document_width", width
            )

        return width

    def _get_mobile_document_width(self) -> int:
        """
        Determine the width of the document in a mobile context.

        Returns:
            int: The width of the document.

        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        return 1440
        # placeholder for mobile-specific implementation
        # raise NotImplementedError("Method to get document width for mobile is not yet implemented.")

    def _get_desktop_document_width(self) -> int:
        """
        Determine the width of the document in a desktop context.

        Returns:
            int: The width of the document.

        Raises:
            NotImplementedError: This method is not yet implemented.
        """
        # placeholder for desktop-specific implementation
        return 1440
        # raise NotImplementedError("Method to get document width for desktop is not yet implemented.")

    def _get_document_width(self) -> int:
        """
        Retrieve the width of the document based on the context (web, mobile, desktop).

        Returns:
            int: The width of the document.
        """
        if self._is_web:
            return self._get_web_document_width()
        elif self._is_mobile:
            return self._get_mobile_document_width()
        elif self._is_desktop:
            return self._get_desktop_document_width()
        else:
            # In case it is a component, we revert to web document width
            return self._get_web_document_width()

    @property
    def _is_page_object(self):
        from hyperiontf.ui.webpage import WebPage
        from hyperiontf.ui.mobile_screen import MobileScreen
        from hyperiontf.ui.desktop_window import DesktopWindow

        return isinstance(self.owner, (WebPage, MobileScreen, DesktopWindow))

    @property
    def _is_web(self):
        from hyperiontf.ui.webpage import WebPage

        return isinstance(self.owner, WebPage)

    @property
    def _is_mobile(self):
        from hyperiontf.ui.mobile_screen import MobileScreen

        return isinstance(self.owner, MobileScreen)

    @property
    def _is_desktop(self):
        from hyperiontf.ui.desktop_window import DesktopWindow

        return isinstance(self.owner, DesktopWindow)
