class ExpectationFailed:
    """
    This is a special class that represents a failed expectation.
    It will be returned when an expectation fails, and it will do nothing for all method calls, allowing chaining.
    """

    def __getattr__(self, _):
        # Return self for any method calls, effectively doing nothing.
        return self

    def __bool__(self):
        # Return False in boolean context.
        return False
