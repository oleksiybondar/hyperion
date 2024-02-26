def are_rectangles_equal(rect1, rect2) -> bool:
    """
    Compare two rectangles to determine if they are equal.

    Each rectangle is represented as a dictionary or dict-like object with four mandatory keys:
    - 'x' (float): The x-coordinate of the rectangle's top-left corner.
    - 'y' (float): The y-coordinate of the rectangle's top-left corner.
    - 'height' (float): The height of the rectangle.
    - 'width' (float): The width of the rectangle.

    Parameters:
    - rect1 (dict): The first rectangle to compare.
    - rect2 (dict): The second rectangle to compare.

    Returns:
    - bool: True if the rectangles are equal in position (x, y) and size (width, height), False otherwise.
    """
    return (
        rect1["x"] == rect2["x"]
        and rect1["y"] == rect2["y"]
        and rect1["height"] == rect2["height"]
        and rect1["width"] == rect2["width"]
    )
