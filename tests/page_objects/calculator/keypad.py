from hyperiontf import Widget, elements, By
import time


class Keypad(Widget):
    """
    Represents a keypad widget used for calculator-like functionality.
    Provides methods to interact with numeric keys, operators, and evaluate expressions.
    Supports different platforms (web, mobile, and desktop).
    """

    @property
    def default_locator(self):
        """
        Defines the default locators for the keypad based on the platform.
        """
        return {
            "web": By.css(".buttons"),
            "mobile": {
                "Android": By.id("com.google.android.calculator:id/main_calculator")
            },
            "desktop": {"Darwin": By.xpath("//XCUIElementTypeGroup[2]")},
        }

    @elements
    def buttons(self):
        """
        Locators for the keypad buttons across different platforms.
        """
        return {
            "web": By.tag("button"),
            "mobile": {"Android": By.class_name("android.widget.ImageButton")},
            "desktop": {"Darwin": By.xpath("//XCUIElementTypeButton")},
        }

    def enter_operand(self, number):
        """
        Enters a numeric operand by clicking the corresponding keypad buttons.
        """
        for char in str(number):
            self.buttons[self._get_key_index(char)].click()

    def enter_operator(self, operation):
        """
        Enters an arithmetic operator by clicking the corresponding keypad button.
        """
        self.buttons[self._get_key_index(operation)].click()

    def evaluate_expression(self, operand: float, operator, other_operand: float):
        """
        Evaluates an arithmetic expression by entering the operands and operator.
        Pauses with a sleep time to make the test more verbose (especially for the web).
        """
        self.enter_operand(operand)
        time.sleep(1)  # just so the test would be a bit verbose, especially for web
        self.enter_operator(operator)
        time.sleep(1)  # just so the test would be a bit verbose, especially for web
        self.enter_operand(other_operand)
        time.sleep(1)  # just so the test would be a bit verbose, especially for web
        self.enter_operator("=")
        time.sleep(1)  # just so the test would be a bit verbose, especially for web

    def _get_keys_map(self) -> dict:
        """
        Helper method to map button text to index.
        Traverses the array once to create a map of <button text>: <index>.

        :return: dict
        """
        if not hasattr(self, "mapped_keys"):
            mapped_keys = {}
            for index, button in enumerate(self.buttons):
                value = button.get_text()
                if not value:
                    # Android case
                    value = button.get_attribute("content-desc")
                mapped_keys[value] = index
            setattr(self, "mapped_keys", mapped_keys)

        return getattr(self, "mapped_keys")

    def _get_key_index(self, key):
        """
        Returns the index of a given key using the mapped keys.
        Handles different key representations across platforms.
        Raises an exception if the key is unknown.
        """
        keys_map = self._get_keys_map()
        key_mapping = {
            "1": ["one"],
            "2": ["two"],
            "3": ["three"],
            "4": ["four"],
            "5": ["five"],
            "6": ["six"],
            "7": ["seven"],
            "8": ["eight"],
            "9": ["nine"],
            "0": ["zero"],
            ".": ["point", ","],
            "*": ["multiply", "x", "×"],
            "/": ["divide", "÷"],
            "-": ["subtract", "minus"],
            "+": ["add", "plus"],
            "=": ["equals"],
        }

        value = keys_map.get(key, None)
        if value is not None:
            return value

        for variant in key_mapping[key]:
            value = keys_map.get(variant, None)
            if value is not None:
                return value

        raise Exception(f"Unknown key {key}")
