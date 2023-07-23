import re
from typing import List


def camel_case_split(text: str) -> List[str]:
    """
    Splits a CamelCase formatted text into individual words.

    This function takes a string with words written in CamelCase format (e.g., "CamelCaseFormattedText") and splits it
    into individual words. It identifies the word boundaries by detecting uppercase letters that are not at the start
    of the string. It returns a list of words.

    :param text: The CamelCase formatted text to split.
    :return: A list of individual words from the input text.
    """
    return re.findall(r"[A-Za-z](?:[a-z]+|[A-Z]*(?=[A-Z]|$))", text)


def snake_notation_split(text: str) -> List[str]:
    """
    Splits a snake_case formatted text into individual words.

    This function takes a string with words written in snake_case format (e.g., "snake_case_formatted_text") and splits
    it into individual words. It uses the underscore character ('_') to identify word boundaries and returns a list of
    words.

    :param text: The snake_case formatted text to split.
    :return: A list of individual words from the input text.
    """
    return text.split("_")


def method_name_to_human_readable(text: str) -> str:
    """
    Converts a method name to human-readable form.

    This function takes a method name, which can be written in either CamelCase or snake_case format, and converts it to
    a human-readable form. It first splits the method name into individual words using the `camel_case_split` and
    `snake_notation_split` functions. Then, it combines the words and capitalizes the first letter to create a
    human-readable representation.

    :param text: The method name to convert.
    :return: The human-readable representation of the method name.
    """
    return (
        " ".join(camel_case_split(" ".join(snake_notation_split(text))))
        .lower()
        .capitalize()
    )


def camel_to_snake_case(camel_str):
    """
    Convert a camelCase string to snake_case.

    Parameters:
        camel_str (str): The camelCase string to be converted.

    Returns:
        str: The string converted to snake_case.

    Examples:
        camel_to_snake_case("camelCaseString") -> "camel_case_string"
        camel_to_snake_case("anotherExampleString") -> "another_example_string"
    """
    result = [camel_str[0].lower()]
    for char in camel_str[1:]:
        if char.isupper():
            result.append("_")
        result.append(char.lower())
    return "".join(result)


def snake_to_camel_case(snake_str):
    """
    Convert a snake_case string to camelCase.

    Parameters:
        snake_str (str): The snake_case string to be converted.

    Returns:
        str: The string converted to camelCase.

    Examples:
        to_camel_case("snake_case_string") -> "snakeCaseString"
        to_camel_case("another_example_string") -> "anotherExampleString"
    """
    components = snake_str.split("_")
    return components[0] + "".join(x.title() for x in components[1:])
