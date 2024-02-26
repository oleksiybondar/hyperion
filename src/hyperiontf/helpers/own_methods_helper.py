"""
Module Constants:
------------------
PROTECTED_METHODS_PATTERN:
    A regular expression pattern used to match method names that start and end with '__' (dunder methods).
    Methods with such names will be ignored by the auto-logging decorator.
"""

from typing import List, Type
import re

PROTECTED_METHODS_PATTERN = "^__.*?__$"


def extend_with_parent_methods(base_class, parent_class, instance_methods):
    while parent_class is not base_class:
        for method_name in dir(parent_class):
            if method_name not in instance_methods and not bool(
                re.match(PROTECTED_METHODS_PATTERN, method_name)
            ):
                instance_methods.append(method_name)
        parent_class = parent_class.__bases__[0]


def get_instance_unique_methods(
    instance: object, base_class: Type[object]
) -> List[str]:
    """
    Retrieves the unique methods specific to the given instance compared to its base class.

    This function takes an instance and a base class as input. It then traverses the instance's class hierarchy
    to find the unique methods that are defined in the instance's class or any of its parent classes, but not
    in the base class.

    :param instance: The object instance whose unique methods are to be retrieved.
    :param base_class: The base class to compare against when finding unique methods.
    :return: A list of method names that are unique to the instance compared to the base class.
    """
    base_class_methods = dir(base_class)
    instance_methods = dir(instance)
    parent_class = instance.__class__.__bases__[0]

    # Traverse the class hierarchy up to the base_class to find unique methods
    extend_with_parent_methods(base_class, parent_class, instance_methods)

    # Filter out the method names that are also present in the base_class
    return [method for method in instance_methods if method not in base_class_methods]
