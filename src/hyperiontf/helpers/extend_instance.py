import types
import re


def extend_instance_with_module(instance: object, module: types.ModuleType):
    """
    Extend an instance with the methods from a given module.

    This function dynamically adds the methods from the specified module to the provided instance.
    It iterates over all the attributes of the module, and if an attribute is a callable method (not starting and ending
    with "__"), it is added to the instance.

    :param instance: The instance to be extended with the methods from the module.
    :param module: The module containing the methods to be added to the instance.
    """
    for method in dir(module):
        if re.match("^__.*?__$", method):
            continue
        setattr(instance, method, types.MethodType(getattr(module, method), instance))
