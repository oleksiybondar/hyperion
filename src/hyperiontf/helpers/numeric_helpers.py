def greatest_common_divisor(a, b):
    """
    Calculate the Greatest Common Divisor (GCD) of two numbers.

    Args:
        a (int): The first number.
        b (int): The second number.

    Returns:
        int: The GCD of a and b.
    """
    while b:
        a, b = b, a % b
    return a
