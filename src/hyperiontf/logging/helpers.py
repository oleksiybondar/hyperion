"""
Function: Escape Special Characters to HTML Entities
===================================================

This function escapes special characters in a given string, converting them to their corresponding HTML entities.
The escaped characters include backslashes ('\\') and double quotes ('"').

"""

import html


def escape(text: str) -> str:
    """
    Escape special characters in the input string to their corresponding HTML entities.

    :param text: The input string containing the text to be escaped.
    :type text: str

    :return: The escaped string with special characters converted to HTML entities.
    :rtype: str
    """
    return html.escape(text.replace("\\", "\\\\").replace('"', '\\"'))
