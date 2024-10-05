from functools import wraps
from typing import Callable


def auto_log(func):
    """
    Decorator to automatically handle logging and exceptions based on assertion status.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        result.is_assertion = self.is_assertion
        result.prefix = self.prefix
        if self.sender:
            result.sender = self.sender
        if self.logger:
            result.logger = self.logger
        if self.is_assertion:
            if result.result:
                result.log_info()
            else:
                result.raise_exception()
        else:
            result.log_debug()
        return result

    return wrapper


def type_check(supported_strategies):
    """
    Decorator to check if the method is supported by the actual value's type.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            if not any(
                isinstance(self.actual_value, tuple(strategy.types))
                for strategy in supported_strategies
            ):
                supported_types = ", ".join(
                    sorted(
                        set(
                            t.__name__
                            for strategy in supported_strategies
                            for t in strategy.types
                        )
                    )
                )
                raise TypeError(
                    f"{func.__name__} can be called for types {supported_types}, "
                    f"but got {type(self.actual_value).__name__}."
                )
            return func(self, *args, **kwargs)

        return wrapper

    return decorator
