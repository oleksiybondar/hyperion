import time
from typing import Type

from hyperiontf.typing import TimeoutException

DEFAULT_EXCEPTION_MESSAGE = "'{name}' function timed out in {timeout} seconds!"


def wait(
    exception_class: Type[Exception] = TimeoutException,
    exception_message_template: str = DEFAULT_EXCEPTION_MESSAGE,
    sleep_interval=0.5,
):
    """
    A decorator that repeatedly calls the decorated function until a non-None result is returned or a timeout is reached.

    Args:
        exception_class (Exception): The type of exception to be raised on timeout.
        exception_message_template (str): A template string for the exception message.
        sleep_interval (float, optional): The interval between retries in seconds. Defaults to 0.5.

    Returns:
        The decorated function, modified to include the waiting and timeout logic.
    """

    def decorator(func):
        """
        The actual decorator function that takes the function to be decorated.

        Args:
            func (callable): The function to be decorated.

        Returns:
            callable: The wrapper function.
        """

        def wrapper(self, *args, timeout=5, raise_exception=True, **kwargs):
            """
            The wrapper function that adds the waiting and timeout functionality to the decorated function.

            Args:
                *args: Variable length argument list for the decorated function.
                timeout (int, optional): The timeout in seconds. Defaults to 5.
                raise_exception (bool, optional): Flag to raise an exception if the timeout is reached without a successful result. Defaults to True.
                **kwargs: Arbitrary keyword arguments for the decorated function.

            Returns:
                The result of the decorated function if successful within the timeout period; otherwise, None or raises an exception.
            """
            deadline = time.time() + timeout
            while time.time() < deadline:
                try:
                    result = func(self, *args, **kwargs)
                    if result:
                        return self
                except Exception:
                    # Handle any exceptions that might occur in the function call.
                    pass
                time.sleep(
                    sleep_interval
                )  # Sleep for the specified interval between retries.

            if raise_exception:
                raise exception_class(
                    exception_message_template.format(
                        timeout=timeout, name=func.__name__
                    )
                )
            return self

        return wrapper

    return decorator
