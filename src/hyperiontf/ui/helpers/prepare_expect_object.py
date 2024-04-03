from typing import Any

from hyperiontf.logging import Logger
from hyperiontf.assertions.expect import Expect


def prepare_expect_object(
    page_object, actual_value: Any, is_assertion: bool, prefix: str, logger: Logger
):
    """
    Prepares an Expect object configured for either assertion or verification against an element's properties.
    This method centralizes the creation of Expect objects, setting them up with the necessary context for
    performing comparisons, logging outcomes, and controlling test flow based on the operation type (assertion
    or verification).

    The method distinguishes between assertions and verifications by the is_assertion parameter. Assertions
    will halt test execution on failure by raising an exception, while verifications log the outcome and
    allow the test to continue, enhancing traceability and flexibility in test scripting.

    Parameters:
        page_object: An instance of Page or Iframe or Screen or Widget or Element
        actual_value (str|bool): The actual value retrieved from the element, to be compared against an expected value.
        is_assertion (bool): Indicates whether the Expect object is being prepared for an assertion (True)
                             or a verification (False). This controls whether failures result in raised exceptions
                             or logged outcomes without stopping the test.
        prefix (str): A message prefix to prepend to log entries, providing context about the comparison being performed.
        logger (Logger): An instance of the Logger

    Returns:
        Expect: An Expect object configured with the actual value, logging details, and operational mode (assert or verify),
                ready for performing comparisons and handling outcomes appropriately.
    """
    return Expect(
        actual_value,
        sender=page_object.__full_name__,
        logger=logger,
        is_assertion=is_assertion,
        prefix=prefix,
    )
