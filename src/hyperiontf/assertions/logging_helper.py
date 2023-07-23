from typing import Optional
from .failed_expectation import ExpectationFailed


def convert_args_into_kwargs(method, args, kwargs):
    """
    Convert Positional Arguments into Keyword Arguments.

    This function takes a method, a list of positional arguments (args),
    and a dictionary of keyword arguments (kwargs) and converts the
    positional arguments into keyword arguments using the parameter names
    from the method's signature.

    Parameters:
        method (function): The method for which arguments are being converted.
        args (list): A list of positional arguments passed to the method.
        kwargs (dict): A dictionary of keyword arguments passed to the method.

    Returns:
        dict: A dictionary containing both the original keyword arguments
              and the converted positional arguments as keyword arguments.

    Example:
        def my_method(self, a, b, c=10):
            return a + b + c

        args = [1, 2]
        kwargs = {'c': 3}
        result_kwargs = convert_args_into_kwargs(my_method, args, kwargs)
        # Output: {'a': 1, 'b': 2, 'c': 3}

    Notes:
        - If the method is a class method or static method, the 'self' or 'cls'
          parameter should be excluded from the method's signature.
        - For Python 3.10+, you can use the new PEP 618 syntax to simplify
          positional argument handling using method.__code__.co_posonlyargcount.
    """
    mapped_args_to_kwargs = {}
    # Map positional arguments to their corresponding parameter names
    offset = 1 if method.__code__.co_varnames[0] == "self" else 0
    for i, arg in enumerate(args):
        # Get the parameter name at the same position as the argument
        arg_name = method.__code__.co_varnames[i + offset]
        # Add the argument to the dictionary with its parameter name as the key
        mapped_args_to_kwargs[arg_name] = arg

    # Combine the original keyword arguments with the mapped positional arguments
    return {**kwargs, **mapped_args_to_kwargs}


def expect_logging_helper(original_method):
    """
    A decorator for expectation methods in the Expect class.
    It handles logging of the result, and raises an Exception if the expectation fails.
    This decorator also controls whether to log results or not, through the `log_results` argument.

    Parameters
    ----------
    original_method : callable
        The original method in the Expect class that's being decorated.

    Returns
    -------
    callable
        A wrapped version of the original method that includes additional logging and error handling.
    """

    def wrapper(
        self,
        *args,
        not_an_assertion: Optional[bool] = False,
        log_results: bool = True,
        **kwargs,
    ):
        """
        The wrapper function that will replace the original method.

        Parameters
        ----------
        self : Expect
            The instance of the Expect class. Passed automatically.
        *args
            The arguments passed to the original method.
        not_an_assertion : bool, optional
            Whether this is not an assertion. If true, it indicates a verification and does not raise an Exception.
            Defaults to False, meaning it is an assertion and will raise an Exception upon failure.
        log_results : bool, optional
            Whether to log the results of the expectation. Useful in case of nested calls where logging once suffices.
            Defaults to True, meaning results will be logged.
        **kwargs
            The keyword arguments passed to the original method.

        Returns
        -------
        Expect or raises Exception
            Returns an instance of the Expect class if the expectation passes,
            raises an Exception if the expectation fails.
        """
        result = original_method(self, *args, **kwargs)
        if log_results:
            self._log_results(
                result,
                method=original_method.__name__,
                is_assertion=not not_an_assertion,
                e_args=args,
                e_kwargs=convert_args_into_kwargs(original_method, list(args), kwargs),
            )

        if not result:
            if not_an_assertion:
                return ExpectationFailed()

            raise Exception(f"Expectation {original_method.__name__} failed")

        return self

    return wrapper
