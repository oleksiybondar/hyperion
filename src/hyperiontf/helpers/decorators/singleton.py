def Singleton(cls):
    """
    Decorator to make a class Singleton by adding a custom __new__ method which ensures that only one instance can be
    created.

    NOTE: The class to be decorated should not implement a __new__ method.

    :param cls: The class to decorate.
    :return: The decorated class.
    """
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper
