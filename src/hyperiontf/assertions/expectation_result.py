from typing import Optional, Type, Any
from hyperiontf.logging.logger import Logger, getLogger
from hyperiontf.typing import (
    LoggerSource,
    FailedExpectationException,
    ExpectationStatus,
    ComparisonType,
)

DEFAULT_EXPECT_LOGGER = getLogger(LoggerSource.EXPECT)


class ExpectationResult:
    """
    A class to represent the result of an expectation in a testing framework.

    This class plays a crucial role in handling both verifications and assertions
    within the framework. It encapsulates the outcome of a comparison, including
    its state (pass/fail), actual and expected values, and other pertinent details.
    The class provides enhanced logging capabilities, ensuring detailed information
    is available for debugging and analysis. In the context of verifications, it logs
    messages at different levels (debug, info, warning), aiding complex logic analysis.
    For assertions, it logs success messages and raises exceptions on failures.

    Attributes:
        result (bool): The boolean outcome of the comparison.
        actual_value (Any): The actual value obtained in the comparison.
        expected_value (Any): The expected value in the comparison.
        method (str): The comparison method used.
        is_assertion (Optional[bool]): Flag indicating if the result is from an assertion.
        logger (Optional[Logger]): Logger object for logging the result.
        sender (Optional[str]): Identifier of the result's sender.
        diff (Optional[str]): String describing the difference between actual and expected values.
        human_readable_description (Optional[str]): Human-friendly description of the comparison.
        extra (Optional[dict]): Additional information for logging.

    The class also includes properties for quick access to the type of expectation,
    its status, a descriptive action, and detailed comparison information. These properties
    enhance the readability and utility of the class in various testing scenarios.
    """

    def __init__(
        self,
        result: bool,
        actual_value: Any,
        expected_value: Any,
        method: str,
        is_assertion: Optional[bool] = True,
        logger: Optional[Logger] = DEFAULT_EXPECT_LOGGER,
        sender: Optional[str] = LoggerSource.EXPECT,
        diff: Optional[str] = None,
        human_readable_description: Optional[str] = None,
        prefix: Optional[str] = None,
        extra: Optional[dict] = None,
    ):
        """
        Initializes a new instance of the ExpectationResult class.

        Args:
            result (bool): The outcome of the expectation. True indicates a pass (expectation met),
                           and False indicates a failure (expectation not met).
            actual_value (Any): The actual value obtained during the expectation evaluation.
                                This can be of any type depending on the context of the test.
            expected_value (Any): The expected value against which the actual value is compared.
                                  This can vary in type based on the expectation.
            method (str): The name of the method used for the expectation. This is used for logging
                          and reporting purposes to identify the specific expectation.
            is_assertion (Optional[bool]): A flag indicating whether the expectation is an assertion.
                                           Defaults to True. Assertions typically raise an exception
                                           on failure, whereas verifications log the outcome.
            logger (Optional[Logger]): The logger object used for logging the outcome of the expectation.
                                       Defaults to a logger obtained from `getLogger(LoggerSource.EXPECT)`.
            sender (Optional[str]): An identifier for the sender of the log messages.
                                    Defaults to `LoggerSource.EXPECT`.
            diff (Optional[str]): A string describing the difference between the actual and expected
                                  values, if applicable. Useful for detailed logging.
            human_readable_description (Optional[str]): A human-friendly description of the expectation
                                                        and its context, enhancing the readability of logs.
            prefix (Optional[str]): A string...
            extra (Optional[dict]): Additional data to be included in log messages.
                                    This can be used to pass extra information relevant to the expectation.

        This constructor sets up the expectation result with all necessary details for effective
        logging and reporting within the framework. It captures both the state of the expectation
        and contextual information, facilitating better diagnostics and debugging.
        """
        self.result = result
        self.actual_value = actual_value
        self.expected_value = expected_value
        self.method = method
        self.is_assertion = is_assertion
        self.logger = logger
        self.sender = sender
        self.diff = diff
        self.prefix = prefix
        self.human_readable_description = human_readable_description
        self.extra = extra

    @property
    def expectation_type(self) -> str:
        """
        Describes the type of expectation: Assertion or Verification.

        Returns:
            str: 'ASSERTION' if the expectation is an assertion (is_assertion is True),
                 'VERIFICATION' otherwise. Assertions are typically used in tests and
                 raise exceptions on failure, while verifications are used within the
                 framework and log outcomes without raising exceptions.
        """
        if self.is_assertion:
            return ComparisonType.ASSERTION

        return ComparisonType.VERIFICATION

    @property
    def status(self) -> str:
        """
        Provides the status of the expectation result.

        Returns:
            str: 'PASS' if the expectation result is True, indicating the expectation was met.
                 'FAIL' if the expectation result is False, indicating the expectation was not met.
        """
        if self.result:
            return ExpectationStatus.PASS

        return ExpectationStatus.FAIL

    @property
    def action(self) -> str:
        """
        Provides a human-readable description of the action performed.

        This property uses the `human_readable_description` if provided,
        otherwise, it defaults to a modified version of the `method` string.

        Returns:
            str: A string describing the action or method in a user-friendly format.
        """
        if self.human_readable_description is not None:
            return self.human_readable_description

        return self.method.replace("_", " ")

    @property
    def comparison_info(self) -> str:
        """
        Provides detailed information about the comparison made.

        For passed expectations, this includes a brief summary (typically the actual value).
        For failed expectations, it provides a more detailed report, including both actual
        and expected values, and a description of differences if available.

        Returns:
            str: A string detailing the comparison, tailored based on the result of the expectation.
        """
        if self.result:
            return self._short_comparison_info

        return self._full_comparison_info

    @property
    def _short_comparison_info(self):
        """
        Provides a brief summary of the comparison, typically used for passed expectations.

        Returns:
            str: A string summarizing the actual value of the expectation.
        """
        return f"Actual value:\n{self.actual_value}"

    @property
    def _full_comparison_info(self):
        """
        Provides a detailed description of the comparison, typically used for failed expectations.

        This includes details of the actual and expected values, and a difference summary if available.

        Returns:
            str: A comprehensive string detailing the actual value, expected value, and differences.
        """
        info = f"{self._short_comparison_info}\nExpected value:\n{self.expected_value}"
        if self.diff is not None:
            info += f"\nDifference:\n{self.diff}"

        return info

    def __bool__(self):
        """
        Returns the boolean value of the comparison result for truthiness testing.

        Returns:
            bool: The boolean result of the comparison.
        """
        return self.result

    def __eq__(self, other):
        """
        Compares the ExpectationResult with a boolean or another ExpectationResult.

        Args:
            other (bool or ExpectationResult): The object to compare with.

        Returns:
            bool: True if equal, False otherwise.
        """
        if isinstance(other, (bool, ExpectationResult, int)):
            return self.result == bool(other)
        return NotImplemented

    def __str__(self):
        """
        Returns the informal string representation of the ExpectationResult.

        Returns:
            str: A concise, user-friendly description of the comparison.
        """
        return f"[{self.sender}] {self.prefix or ''} {self.action} {self.expectation_type} {self.status}.\n{self.comparison_info}"

    def __repr__(self):
        """
        Returns the formal string representation of the ExpectationResult.

        Returns:
            str: A string that represents the object, including all attributes.
        """
        return (
            f"ExpectationResult(result={self.result}, "
            f"actual_value={self.actual_value}, "
            f"expected_value={self.expected_value}, "
            f"method='{self.method}')"
        )

    def raise_exception(
        self, exception_class: Type[Exception] = FailedExpectationException
    ) -> None:
        """
        Raises the specified exception if the comparison result is False.

        Args:
            exception_class (Optional[Type[Exception]]): The type of exception to be raised.
                                                        If None, a default Exception is raised.
        """
        if not self.result:
            message = self.__str__()
            self.logger.fatal(message, extra=self._log_meta)  # type: ignore
            raise exception_class(message)

    def log_debug(self):
        """
        Logs the result at the debug level.

        This method is primarily used in the context of verifications within the framework,
        providing detailed logging useful for debugging and understanding the flow of complex logic.
        """
        self.logger.debug(self.__str__(), extra=self._log_meta)

    def log_info(self):
        """
        Logs the result at the info level.

        Useful for recording informational messages about the expectation results,
        providing a balance between verbosity and relevance.
        """
        self.logger.info(self.__str__(), extra=self._log_meta)

    def log_warning(self):
        """
        Logs the result at the warning level.

        This method is particularly useful in scenarios where expectation results
        may indicate potential issues or require attention, without being outright failures.
        """
        self.logger.warning(self.__str__(), extra=self._log_meta)

    def log_error(self):
        """
        Logs the result at the error level.

        Used in scenarios where the expectation failure is critical and indicative
        of significant issues in the test or framework logic.
        """
        self.logger.error(self.__str__(), extra=self._log_meta)

    @property
    def _log_meta(self):
        meta = {"assertion": self.result} if self.is_assertion else {}

        if self.extra is not None:
            meta = {**self.extra, **meta}

        return meta
