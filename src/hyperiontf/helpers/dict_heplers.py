import copy
from .string_helpers import snake_to_camel_case


def transform_keys_to_camel_case(data):
    """
    Transforms the keys of a dictionary (or nested dictionary) from snake_case to camelCase.

    Parameters:
        data (dict): The dictionary whose keys are to be transformed.

    Returns:
        dict: A deep copy of the original dictionary, but with keys in camelCase.

    Examples:
        transform_keys_to_camel_case({"snake_case_key": "value"}) -> {"snakeCaseKey": "value"}
        transform_keys_to_camel_case({"nested_key": {"snake_case_key": "value"}}) -> {"nestedKey": {"snakeCaseKey": "value"}}
    """
    new_data = copy.deepcopy(data)
    if isinstance(new_data, dict):
        return {
            snake_to_camel_case(k): transform_keys_to_camel_case(v)
            for k, v in new_data.items()
        }
    elif isinstance(new_data, list):
        return [transform_keys_to_camel_case(v) for v in new_data]
    else:
        return new_data
