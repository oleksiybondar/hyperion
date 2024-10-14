class HyperionException(Exception):
    """
    Base exception class that caches the last exception information.

    Attributes:
        last_exec_info (tuple): A tuple containing the last cached exception details:
            (exc_type, exc_value, exc_traceback). This is updated each time an exception
            of this type (or its subclass) is created.
    """

    last_exec_info = (None, None, None)

    def __init__(self, *args):
        """
        Initializes the exception and caches the current exception details.
        The class caches the exception type, instance, and the current traceback
        when an instance of this exception (or its subclass) is created.

        Args:
            *args: Arguments to be passed to the base Exception class.
        """
        super().__init__(*args)

        # Cache the exception type, value (self), and the current traceback
        exc_type = self.__class__
        exc_value = self

        # Store the information as a tuple in last_exec_info
        HyperionException.last_exec_info = (exc_type, exc_value, None)
