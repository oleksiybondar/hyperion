from functools import wraps
import inspect


def auto_log(func):
    """Decorator to log the action and return self for chaining."""

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        # Get the function name dynamically for logging
        action_name = func.__name__

        # Create a dictionary of argument names and their values
        signature = inspect.signature(func)
        arg_names = signature.parameters.keys()
        details = {name: value for name, value in zip(arg_names, args)}
        details.update(kwargs)  # Add named arguments (if any)

        # Log the action
        self._log_action(action_name, details)

        # Call the original method
        func(self, *args, **kwargs)

        # Return self for chaining
        return self

    return wrapper
