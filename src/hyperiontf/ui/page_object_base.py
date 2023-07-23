from typing import Optional
from .automation_adapter_manager import AutomationAdaptersManager


class BasePageObject:
    def __init__(self, automation_descriptor, logger):
        self.automation_adapter = automation_descriptor
        self.__full_name__ = self.__class__.__name__
        self.logger = logger

    def quit(self):
        self.logger.info(f"[{self.__full_name__}] Quitting the browser")
        self.automation_adapter.quit()
        AutomationAdaptersManager().delete(self.automation_adapter)

    def make_screenshot(self, filepath: Optional[str] = None):
        if filepath:
            return self.automation_adapter.screenshot(
                filepath
            )  # Replace with the actual path
        else:
            return self.automation_adapter.screenshot_as_base64

    def screenshot(
        self,
        message: Optional[str] = "Screenshot",
        title: Optional[str] = "Regular screenshot",
    ):
        base_64_img_url = f"data:text/html;{self.make_screenshot()}"
        self.logger.info(
            message,
            extra={
                "attachments": [
                    {"title": title, "type": "image", "url": base_64_img_url}
                ]
            },
        )
