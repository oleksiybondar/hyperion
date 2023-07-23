from typing import Optional

from hyperiontf.logging import getLogger
from hyperiontf.typing import NoSuchElementException
from hyperiontf.ui.decorators.element_error_recovery import error_recovery

from .locatable import LocatableElement

logger = getLogger("Element")


class Element(LocatableElement):
    def __init__(self, parent, locator, name):
        super().__init__(parent, locator, name)

    def is_interactive(self):
        if self.element_adapter is NoSuchElementException:
            raise self.element_adapter
        # TODO: add extra interactivity verifications

    @error_recovery(logger=logger)
    def send_keys(self, data):
        logger.info(f"[{self.__full_name__}] sending input data:\n{data}")
        self.element_adapter.send_keys(data)

    fill = send_keys

    @error_recovery(logger=logger)
    def clear(self):
        logger.info(f"[{self.__full_name__}] clearing input")
        self.element_adapter.clear()

    @error_recovery(logger=logger)
    def clear_and_fill(self, data):
        logger.info(
            f"[{self.__full_name__}] clearing input and sending new input data:\n{data}"
        )
        self.element_adapter.clear()
        self.element_adapter.send_keys(data)

    @error_recovery(logger=logger)
    def click(self):
        logger.info(f"[{self.__full_name__}] click")
        self.element_adapter.click()

    @error_recovery(logger=logger)
    def submit(self):
        logger.info(f"[{self.__full_name__}] submit")
        self.element_adapter.submit()

    @error_recovery(logger=logger)
    def get_text(self, log: bool = True):
        text = self.element_adapter.text.strip()
        if log:
            logger.info(f"[{self.__full_name__}] getting element's text:\n{text}")
        return text

    @error_recovery(logger=logger)
    def get_attribute(self, attr_name: str, log: bool = True):
        text = self.element_adapter.attribute(attr_name).strip()
        if log:
            logger.info(
                f"[{self.__full_name__}] getting element's '{attr_name}' attribute value:\n{text}"
            )
        return text

    @error_recovery(logger=logger)
    def get_style(self, attr_name: str, log: bool = True):
        text = self.element_adapter.style(attr_name)
        if log:
            logger.info(
                f"[{self.__full_name__}] getting element's '{attr_name}' style property value:\n{text}"
            )
        return text

    @error_recovery(logger=logger)
    def make_screenshot(self, filepath: Optional[str] = None):
        if filepath:
            return self.element_adapter.screenshot(
                filepath
            )  # Replace with the actual path
        else:
            return self.element_adapter.scrrenshot_as_base64

    def screenshot(
        self,
        message: Optional[str] = "Element screen snap",
        title: Optional[str] = "Element screen snap",
    ):
        base_64_img_URL = f"data:text/html;{self.make_screenshot()}"
        logger.info(
            message,
            extra={
                "attachments": [
                    {"title": title, "type": "image", "url": base_64_img_URL}
                ]
            },
        )

    def assert_text(self, expected_text):
        actual_value = self.get_text(log=False)
        if actual_value == expected_text:
            logger.info(
                f"[{self.__full_name__}] asserting element's text. Value match expectations!\nActual"
                f" value: {actual_value}",
                extra={"assertion": True},
            )
            return True
        else:
            message = (
                f"[{self.__full_name__}] asserting element's text. Value missmatch expectations!\nActual value:"
                f"\n{actual_value}\nExpected value:\n{expected_text}"
            )
            logger.error(message, extra={"assertion": False})
            raise Exception(message)

    def assert_attribute(self, attr_name, expected_text):
        actual_value = self.get_attribute(attr_name, log=False)
        if actual_value == expected_text:
            logger.info(
                f"[{self.__full_name__}] asserting element's '{attr_name}' attribute. Value match expectations!"
                f"\nActual value: {actual_value}",
                extra={"assertion": True},
            )
            return True
        else:
            message = (
                f"[{self.__full_name__}] asserting element's '{attr_name}' attribute. Value missmatch "
                f"expectations!\nActual value:\n{actual_value}\nExpected value:\n{expected_text}"
            )
            logger.error(message, extra={"assertion": False})
            raise Exception(message)

    def assert_style(self, attr_name, expected_text):
        actual_value = self.get_style(attr_name, log=False)
        if actual_value == expected_text:
            logger.info(
                f"[{self.__full_name__}] asserting element's '{attr_name}' style value. Value match "
                f"expectations!\nActual value: {actual_value}",
                extra={"assertion": True},
            )
            return True
        else:
            message = (
                f"[{self.__full_name__}] asserting element's '{attr_name}' style value. Value missmatch "
                f"expectations!\nActual value:\n{actual_value}\nExpected value:\n{expected_text}"
            )
            logger.error(message, extra={"assertion": False})
            raise Exception(message)
