from typing import Callable, Any
from hyperiontf.helpers.wagner_fischer import string_diff, array_diff
from hyperiontf.helpers.dict_diff import dict_diff
from functools import wraps


def with_diff(method: Callable[[Any, Any], str]) -> Callable:
    """
    A decorator factory that creates a decorator to augment a function's output with difference analysis.

    This decorator applies a specified difference method (such as string_diff, array_diff, or dict_diff)
    to the output of the decorated function, allowing for a detailed comparison between the actual and
    expected results.

    Args:
        method (Callable[[Any, Any], str]): The difference method to be applied. It should take two arguments
                                            (actual and expected) and return a string representing the difference.

    Returns:
        Callable: A decorator that can be applied to a function.
    """

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(self, *args, **kwargs) -> Any:
            result = func(self, *args, **kwargs)
            if not result.result and args:
                # Use the first positional argument as the expected value
                expected_value = args[0]

                # Compute the difference and extend the result with the difference information
                result.diff = method(self.actual_value, expected_value)
            return result

        return wrapper

    return decorator


def with_string_diff(func: Callable) -> Callable:
    """
    Decorator to add a detailed string difference to the output of a function using the string_diff method.

    This decorator is specifically designed for functions that perform string comparisons,
    where the expected value is the first positional argument. It is applied only if the
    comparison fails (result is False) and at least one positional argument is present.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function with string difference analysis capability.
    """
    return with_diff(method=string_diff)(func)


def with_array_diff(func: Callable) -> Callable:
    """
    Decorator to add a detailed array difference to the output of a function using the array_diff method.

    This decorator is particularly useful for functions comparing arrays, where the expected array
    is the first positional argument. It applies the array_diff method to analyze differences when
    the comparison fails and at least one positional argument is provided.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function with array difference analysis capability.
    """
    return with_diff(method=array_diff)(func)


def with_dict_diff(func: Callable) -> Callable:
    """
    Decorator to add a detailed dictionary difference to the output of a function using the dict_diff method.

    Designed for functions that compare dictionaries, this decorator uses dict_diff to analyze and
    provide a detailed comparison when the function's comparison fails. It assumes the first positional
    argument is the expected dictionary.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function with dictionary difference analysis capability.
    """
    return with_diff(method=dict_diff)(func)
