import pytest
import types
import inspect
from hyperiontf.logging import getLogger

logger = getLogger("Fixture")


def fixture(
    scope="function",
    params=None,
    autouse: bool = False,
    ids=None,
    name=None,
    log: bool = True,
):
    """
    Custom decorator for creating pytest fixtures with additional logging capabilities.

    This decorator wraps pytest.fixture and adds extra logging functionalities.
    Due to the way pytest's dependency injection system works, a pytest fixture is
    essentially a factory function whose arguments are other fixtures. These arguments
    are not directly passed to the function, but instead, their values are determined
    by pytest at runtime.

    Therefore, in order to correctly log and track these fixtures, the wrapper function
    in the decorator needs to be aware of the arguments of the original fixture function.
    To dynamically handle this, we use Python's introspection capability to extract the
    argument names from the original function and then build a new function via the 'exec'
    function that has the same argument list. This way, the wrapper function will have the
    same signature as the original function and pytest can correctly inject the required
    fixtures.

    Args:
        scope (str, optional): The scope of the fixture. Default is "function".
        params (list or None, optional): List of parameters for the fixture. Default is None.
        autouse (bool, optional): If True, the fixture is automatically used. Default is False.
        ids (list or None, optional): List of string ids for the fixture parameters. Default is None.
        name (str or None, optional): Name of the fixture. Default is None.
        log (bool, optional): If True, the fixture will create a log folder. Default is True.

    Returns:
        Callable: The wrapper function for the fixture.

    Example:
        # Usage of the custom fixture decorator
        @fixture(scope='function')
        def my_fixture():
            # Fixture logic here
            yield result
    """

    def inner_decorator(fixture_function):
        # Get the names of the arguments to the original fixture function
        sig = inspect.signature(fixture_function)
        arg_names = ", ".join(sig.parameters.keys())

        func_string = f"""
@pytest.fixture(scope=scope, params=params, autouse=autouse, ids=ids, name=name)
def wrapper({arg_names}):
    # Custom logging logic to push the fixture name to the logger folder
    if log:
        logger.push_folder(fixture_function.__name__)

    # Call the original fixture function with arguments
    result = fixture_function({arg_names})

    # Check if the fixture function returned a generator and get the result if so
    while isinstance(result, types.GeneratorType):
        result = next(result)

    # Yield the result to the test function
    result = yield result

    # Custom logging logic to pop the fixture name from the logger folder
    if log:
        logger.pop_folder()

    return result
"""
        evaluation_scope = {
            "scope": scope,
            "params": params,
            "autouse": autouse,
            "ids": ids,
            "name": name,
            "fixture_function": fixture_function,
            "pytest": pytest,
            "logger": logger,
            "log": log,
            "types": types,
        }

        # Use exec to create the function in the local namespace
        local_namespace = {}
        exec(func_string, evaluation_scope, local_namespace)
        return local_namespace["wrapper"]

    return inner_decorator
