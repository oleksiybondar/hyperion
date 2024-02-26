def clamp(value, minimum, maximum):
    """
    Clamps the given value between the provided minimum and maximum values.

    :param value: The value to be clamped.
    :param minimum: The lower boundary.
    :param maximum: The upper boundary.
    :return: Clamped value.
    """
    return max(minimum, min(value, maximum))


class Color:
    """
    Represents a color defined by its red, green, blue, and alpha components.
    """

    # Class constant for maximum grayscale
    MAX_GRAYSCALE = 0.299 * 255 + 0.587 * 255 + 0.114 * 255

    def __init__(self, red, green, blue, alpha=1.0):
        """
        Initialize a new Color object.

        :param red: Red component (0-255).
        :param green: Green component (0-255).
        :param blue: Blue component (0-255).
        :param alpha: Alpha (transparency) component (0.0-1.0). Default is 1.0 (fully opaque).
        """
        self.red = clamp(red, 0, 255)
        self.green = clamp(green, 0, 255)
        self.blue = clamp(blue, 0, 255)
        self.alpha = clamp(alpha, 0.0, 1.0)

    @staticmethod
    def from_string(color_string: str):
        """
        Create a Color object from a string representation. Delegates to the appropriate method
        based on the format of the input string.

        Supported formats:
        - rgb(255,255,255)
        - rgba(255,255,255,1)
        - #FFFFFF
        - #FFF

        Parameters:
            color_string (str): String representation of the color.

        Returns:
            Color: New Color object created from the string.

        Raises:
            ValueError: If the string format is not recognized.
        """
        if color_string.startswith("rgb"):
            return Color.from_rgb(color_string)

        if color_string.startswith("#"):
            return Color.from_hex(color_string)

        raise ValueError(f"Invalid color string format: {color_string}")

    @staticmethod
    def from_rgb(color_string: str):
        """
        Create a Color object from an RGB or RGBA string representation.

        Expected format: rgb(255,255,255) or rgba(255,255,255,1)

        Parameters:
            color_string (str): RGB or RGBA string representation.

        Returns:
            Color: New Color object created from the RGB(A) string.
        """
        components = color_string.strip("rgba()").split(",")
        red, green, blue = map(int, components[:3])
        alpha = float(components[3]) if len(components) == 4 else 1.0
        return Color(red, green, blue, alpha)

    @staticmethod
    def from_hex(color_string: str):
        """
        Create a Color object from a hex color string. Delegates to the appropriate method
        based on the length of the input string.

        Expected format: #FFFFFF (6 digits) or #FFF (3 digits)

        Parameters:
            color_string (str): Hex color string representation.

        Returns:
            Color: New Color object created from the hex string.
        """
        if len(color_string) == 4:  # short form like #FFF
            return Color.from_hex3(color_string)

        return Color.from_hex6(color_string)

    @staticmethod
    def from_hex6(color_string: str):
        """
        Create a Color object from a 6-digit hex color string.

        Expected format: #FFFFFF

        Parameters:
            color_string (str): 6-digit hex color string representation.

        Returns:
            Color: New Color object created from the hex string.
        """
        red = int(color_string[1:3], 16)
        green = int(color_string[3:5], 16)
        blue = int(color_string[5:7], 16)
        return Color(red, green, blue, 1.0)

    @staticmethod
    def from_hex3(color_string: str):
        """
        Create a Color object from a 3-digit hex color string.

        Expected format: #FFF

        The method doubles each digit to convert it into a 6-digit hex format
        before processing. For example, #ABC becomes #AABBCC.

        Parameters:
            color_string (str): 3-digit hex color string representation.

        Returns:
            Color: New Color object created from the hex string.
        """
        red = int(color_string[1] * 2, 16)
        green = int(color_string[2] * 2, 16)
        blue = int(color_string[3] * 2, 16)
        return Color(red, green, blue, 1.0)

    def grayscale(self):
        """
        Compute the grayscale value of the color using the relative luminance method.

        The relative luminance is calculated using the following formula:
        Y = 0.299R + 0.587G + 0.114B
        where R, G, and B are the red, green, and blue components respectively.

        :return: Grayscale value of the color.
        """
        return 0.299 * self.red + 0.587 * self.green + 0.114 * self.blue

    def approx_eq(self, other, percentage_threshold=5, alpha_threshold=0.1):
        """
        Determine if two colors are approximately equal based on a grayscale and alpha comparison.

        The method checks if the absolute difference between the grayscale values of the two colors is within
        a certain threshold. It also checks if the difference between the alpha values is within a specified threshold.

        :param other: The other Color object to compare against.
        :param percentage_threshold: The maximum allowed percentage difference between the grayscale values.
                                     The actual threshold is computed as a percentage of the maximum possible grayscale
                                     value.
        :param alpha_threshold: The maximum allowed difference between the alpha values.
        :return: True if the colors are approximately equal based on the specified thresholds; False otherwise.
        """
        actual_threshold = Color.MAX_GRAYSCALE * (percentage_threshold / 100)

        grayscale_diff = abs(self.grayscale() - other.grayscale())
        alpha_close = abs(self.alpha - other.alpha) <= alpha_threshold

        return grayscale_diff <= actual_threshold and alpha_close

    def __eq__(self, other):
        """
        Determine if two Color objects are exactly equal.

        :param other: The other Color object to compare against.
        :return: True if the red, green, blue, and alpha values of both colors are exactly the same; False otherwise.
        """
        return (
            self.red == other.red
            and self.green == other.green
            and self.blue == other.blue
            and self.alpha == other.alpha
        )

    def __ne__(self, other):
        """
        Determine if two Color objects are not equal.

        :param other: The other Color object to compare against.
        :return: True if the colors are not the same; False otherwise.
        """
        return not self.__eq__(other)

    def __lt__(self, other):
        """
        Check if the grayscale value of the current Color object is less than that of another.

        :param other: The other Color object to compare against.
        :return: True if the grayscale value of the current color is less than that of the other; False otherwise.
        """
        return self.grayscale() < other.grayscale()

    def __le__(self, other):
        """
        Check if the grayscale value of the current Color object is less than or equal to that of another.

        :param other: The other Color object to compare against.
        :return: True if the grayscale value of the current color is less than or equal to that of the other; False otherwise.
        """
        return self.grayscale() <= other.grayscale()

    def __gt__(self, other):
        """
        Check if the grayscale value of the current Color object is greater than that of another.

        :param other: The other Color object to compare against.
        :return: True if the grayscale value of the current color is greater than that of the other; False otherwise.
        """
        return self.grayscale() > other.grayscale()

    def __ge__(self, other):
        """
        Check if the grayscale value of the current Color object is greater than or equal to that of another.

        :param other: The other Color object to compare against.
        :return: True if the grayscale value of the current color is greater than or equal to that of the other; False otherwise.
        """
        return self.grayscale() >= other.grayscale()

    def __add__(self, other):
        """
        Blend two Color objects together.

        When adding two colors, the individual red, green, blue values are combined,
        but they will never exceed 255. The alpha value is averaged.

        :param other: The other Color object to blend with.
        :return: A new Color object representing the blended color.
        """
        new_red = min(self.red + other.red, 255)
        new_green = min(self.green + other.green, 255)
        new_blue = min(self.blue + other.blue, 255)
        new_alpha = (self.alpha + other.alpha) / 2

        return Color(new_red, new_green, new_blue, new_alpha)

    def __iadd__(self, other):
        """
        Blend the current Color object with another in-place.

        When blending the colors, the individual red, green, blue values of the current color are
        combined with those of the other color, but they will never exceed 255. The alpha value is averaged.

        :param other: The other Color object to blend with.
        :return: The current Color object, modified to represent the blended color.
        """
        if not isinstance(other, Color):
            return NotImplemented

        self.red = min(self.red + other.red, 255)
        self.green = min(self.green + other.green, 255)
        self.blue = min(self.blue + other.blue, 255)
        self.alpha = (self.alpha + other.alpha) / 2
        return self

    def __sub__(self, other):
        """
        Subtract one Color object from another.

        When subtracting two colors, the individual red, green, blue values are decreased
        based on the other color's respective values, but they will never go below 0.
        The alpha value is subtracted directly and clamped between 0 and 1.

        :param other: The Color object to subtract from the current color.
        :return: A new Color object representing the subtracted color.
        """
        new_red = max(self.red - other.red, 0)
        new_green = max(self.green - other.green, 0)
        new_blue = max(self.blue - other.blue, 0)
        new_alpha = clamp(self.alpha - other.alpha, 0, 1)

        return Color(new_red, new_green, new_blue, new_alpha)

    def __isub__(self, other):
        """
        Subtract another Color object from the current one in-place.

        When performing the subtraction, the individual red, green, blue values of the current color
        are decreased based on the other color's respective values, but they will never go below 0.
        The alpha value is subtracted directly and clamped between 0 and 1.

        :param other: The Color object to subtract from the current color.
        :return: The current Color object, modified to represent the subtracted color.
        """

        self.red = max(self.red - other.red, 0)
        self.green = max(self.green - other.green, 0)
        self.blue = max(self.blue - other.blue, 0)
        self.alpha = clamp(self.alpha - other.alpha, 0, 1)
        return self

    def __mul__(self, value):
        """
        Multiply the color with either another Color or a scalar value.

        Multiplication of two colors modulates the individual red, green, blue values
        based on the other color's respective values. If multiplied by a scalar,
        each component (red, green, blue, alpha) of the color is multiplied by that scalar.
        The results are clamped to their respective valid ranges.

        :param value: The Color object or scalar (int, float) to multiply with the current color.
        :return: A new Color object representing the multiplied color.
        """
        if isinstance(value, Color):
            new_red = (self.red * value.red) // 255
            new_green = (self.green * value.green) // 255
            new_blue = (self.blue * value.blue) // 255
            new_alpha = self.alpha * value.alpha
        elif isinstance(value, (int, float)):
            new_red = clamp(int(self.red * value), 0, 255)
            new_green = clamp(int(self.green * value), 0, 255)
            new_blue = clamp(int(self.blue * value), 0, 255)
            new_alpha = clamp(self.alpha * value, 0, 1)
        else:
            return NotImplemented

        return Color(new_red, new_green, new_blue, new_alpha)

    def __imul__(self, value):
        """
        Multiply the current color in-place with either another Color or a scalar value.

        In-place multiplication modulates the individual red, green, blue values
        of the current color based on the other color's respective values or by the scalar.
        The results are clamped to their respective valid ranges.

        :param value: The Color object or scalar (int, float) to multiply with the current color.
        :return: The current Color object, modified to represent the multiplied color.
        """
        if isinstance(value, Color):
            self.red = (self.red * value.red) // 255
            self.green = (self.green * value.green) // 255
            self.blue = (self.blue * value.blue) // 255
            self.alpha *= value.alpha
        elif isinstance(value, (int, float)):
            self.red = clamp(int(self.red * value), 0, 255)
            self.green = clamp(int(self.green * value), 0, 255)
            self.blue = clamp(int(self.blue * value), 0, 255)
            self.alpha = clamp(self.alpha * value, 0, 1)
        else:
            return NotImplemented
        return self

    def __str__(self):
        """
        String representation of the Color object.

        :return: String in the format "rgba(R, G, B, A)".
        """
        return f"rgba({self.red}, {self.green}, {self.blue} ,{self.alpha:.2f})"

    def __repr__(self):
        """
        Returns a string representation suitable for debugging and development.

        :return: String in the format "Color(R, G, B, A)".
        """
        return f"Color({self.red}, {self.green}, {self.blue}, {self.alpha:.2f})"
