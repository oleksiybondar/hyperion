from typing import Optional, Type, Union, Any
from hyperiontf.logging.logger import Logger
from hyperiontf.ui.color import Color
from hyperiontf.image_processing.image import Image
from .decorators import auto_log, type_check
from hyperiontf.assertions.strategy.default_strategy import DefaultStrategy
from hyperiontf.assertions.strategy.numeric_strategy import NumericStrategy
from hyperiontf.assertions.strategy.string_strategy import StringStrategy
from hyperiontf.assertions.strategy.array_strategy import ArrayStrategy
from hyperiontf.assertions.strategy.dict_strategy import DictStrategy
from hyperiontf.assertions.strategy.color_strategy import ColorStrategy
from hyperiontf.assertions.strategy.filesystem_strategy import FileSystemStrategy
from hyperiontf.assertions.strategy.image_strategy import ImageStrategy
from .expectation_result import ExpectationResult
from .image_expectation_result import ImageExpectationResult

STRATEGIES_MAP = {
    "bool": NumericStrategy,
    "int": NumericStrategy,
    "float": NumericStrategy,
    "str": StringStrategy,
    "list": ArrayStrategy,
    "set": ArrayStrategy,
    "tuple": ArrayStrategy,
    "dict": DictStrategy,
    "Color": ColorStrategy,
    "File": FileSystemStrategy,
    "Dir": FileSystemStrategy,
    "Image": ImageStrategy,
}


class Expect:
    """
    A central class in the testing framework that provides a fluent interface for asserting
    various conditions on a given value. It dynamically selects an appropriate strategy
    based on the type of the actual value to perform type-specific or general assertions.

    This class is relatively private and is not intended for direct use in tests; instead,
    helper methods `expect` and `verify` are provided for public use. The lowercase `expect`
    function is an entry point that facilitates assertions, raising exceptions on failure,
    whereas `verify` is used for non-assertive checks, logging outcomes as informational
    without raising exceptions, making it suitable for more flexible validation scenarios.

    Attributes:
        actual_value (Any): The value to be tested or verified.
        is_assertion (bool): A flag indicating if the Expect instance is being used for
                             assertions (True) or verifications (False).
        logger (Optional[Logger]): Logger object for logging outcomes of the checks.
        sender (Optional[str]): Identifier for the sender of log messages.
        strategy (Union[DefaultStrategy, Type[DefaultStrategy]]): The strategy object
                     determined based on the actual value's type, responsible for
                     executing the specific comparison methods.

    The class originally leveraged Python's dynamic `__getattr__` feature to proxy method
    calls to the appropriate strategy, allowing for a compact implementation. However, this
    dynamic approach was revised in favor of explicitly defining wrapper methods for each
    strategy. This decision, influenced by the capabilities of ChatGPT, aimed to enhance
    the developer experience by providing clear type hints and verbose docstrings that
    detail cross-referencing types and expected behaviors, thus making the API more
    intuitive and the code more maintainable and extendable.

    The extensive logging capability of the `Expect` class and its strategies is a key
    feature, offering detailed insights into the checks performed, especially valuable
    in non-assertion contexts where results are logged for informational purposes,
    regardless of the outcome. This approach ensures that users benefit from comprehensive
    feedback on their tests' behavior and outcomes.

    Example Usage:
        expect(some_value).is_none()  # Checks if some_value is None, raising an exception on failure.
        verify(another_value).is_int()  # Checks if another_value is an integer, logging the outcome.

    The STRATEGIES_MAP dictionary maps types to their corresponding strategy classes,
    allowing the Expect class to dynamically select the appropriate strategy based on
    the actual value's type, facilitating a wide range of assertions and verifications
    across different data types and conditions.
    """

    def __init__(
        self,
        actual_value,
        is_assertion,
        sender: Optional[str] = None,
        logger: Optional[Logger] = None,
        prefix: Optional[str] = None,
    ):
        self.actual_value = actual_value
        self.is_assertion = is_assertion
        self.logger = logger
        self.sender = sender
        self.strategy: Union[DefaultStrategy, Type[DefaultStrategy]] = (
            STRATEGIES_MAP.get(actual_value.__class__.__name__, DefaultStrategy)(
                actual_value
            )
        )
        self.prefix = prefix

    @auto_log
    def to_be(self, expected_value: Any) -> Type[ExpectationResult]:
        """
        Asserts that the actual value is equal to the expected value. The definition of equality
        is strategy-specific: for numeric types, it means numerical equality; for strings, it means
        exact string match; for files, it may involve comparing file contents or checksums; and for
        collections, it could mean structural equality.

        This method is applicable across various types, including but not limited to numbers, strings,
        lists, sets, tuples, dictionaries, and file system entities.

        Args:
            expected_value (Any): The expected value for comparison.

        Returns:
            Expect: The Expect instance to allow for method chaining.

        Note:
            The behavior and interpretation of "equality" can vary significantly across different types.
            Refer to the documentation of the specific strategy classes for more detailed descriptions
            of how equality is determined for each type.
        """
        return self.strategy.to_be(expected_value)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy, ArrayStrategy])
    def to_contain(self, expected_value: Union[str, Any]) -> ExpectationResult:
        """
        Asserts that the actual value contains the expected value. For strings, this means the actual
        string contains the expected substring. For collections (e.g., lists, sets, tuples), it checks
        if the expected item is present within the collection.

        This method is applicable to strings and collection-like types, enhancing flexibility in
        assertions related to content inclusion.

        Args:
            expected_value (Union[str, Any]): The expected item or substring to check for presence
                                              within the actual value.

        Returns:
            Expect: The Expect instance to allow for method chaining.

        Note:
            The interpretation of "containment" varies by the type of the actual value. For exact
            behavior and limitations, refer to the documentation of the specific strategy classes
            applicable to the actual value's type.
        """
        return self.strategy.to_contain(expected_value)  # type: ignore

    @auto_log
    def not_to_be(self, expected_value: Any) -> Type[ExpectationResult]:
        """
        Asserts that the actual value is not equal to the expected value. The interpretation of inequality
        is strategy-specific and can range from simple value mismatches to complex structural differences
        in collections or files.

        This method is universally applicable, suitable for numbers, strings, collections (lists, sets, tuples),
        dictionaries, and file system entities, ensuring that the actual value does not match the expected value
        as defined by the context of the type.

        Args:
            expected_value (Any): The expected value the actual value should not equal to. This could be
                                  a simple data type, a collection, or even a file system entity depending on
                                  the strategy in use.

        Returns:
            Expect: The Expect instance to allow for method chaining.

        Note:
            The specifics of what constitutes "not being equal" varies significantly across different data types
            and structures. It's essential to consider the context and the type of the actual value when using
            this assertion.
        """
        return self.strategy.not_to_be(expected_value)  # type: ignore

    @auto_log
    def is_none(self) -> ExpectationResult:
        """
        Asserts that the actual value is None. This method is universally applicable across all types,
        ensuring that the actual value is explicitly None. It is a fundamental check used to verify
        the absence of a value or that a variable or expression evaluates to None.

        Returns:
            ExpectationResult: An object representing the result of the check, including details such as
                               the actual value, the expected condition (being None), and whether the check
                               passed or failed.

        Note:
            This assertion is type-agnostic and can be used directly without considerations of the actual
            value's type, making it one of the most basic assertions available.
        """
        return self.strategy.is_none()  # type: ignore

    @auto_log
    def is_not_none(self) -> ExpectationResult:
        """
        Asserts that the actual value is not None. This method is universally applicable across all types,
        ensuring that the actual value exists and is not explicitly None. It is a fundamental check used to
        verify the presence of a value or that a variable or expression evaluates to something other than None.

        Returns:
            ExpectationResult: An object representing the result of the check, including details such as
                               the actual value, the expected condition (not being None), and whether the check
                               passed or failed.

        Note:
            This assertion is type-agnostic and can be used directly without considerations of the actual
            value's type, making it one of the essential assertions for validating the existence of a value.
        """
        return self.strategy.is_not_none()  # type: ignore

    @auto_log
    def is_a(self, cls: Type) -> ExpectationResult:
        """
        Asserts that the actual value is an instance of a specified class or type. This method is versatile and
        can be applied to various data types, from primitive types like integers and strings to complex objects
        like custom classes and data structures.

        The method is particularly useful for type-safe operations, ensuring that the actual value conforms to
        expected type constraints, thereby facilitating more robust and error-free code.

        Args:
            cls (Type): The class or type that the actual value is expected to be an instance of.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual value
                               is an instance of the specified class or type, along with the actual and expected values.

        Note:
            While this assertion is broadly applicable, the interpretation of being an instance of a class may vary
            slightly depending on the strategy and the specific type checks involved. It's recommended to consult
            the documentation of the specific strategy classes for more nuanced details on type compatibility and
            instance checks.
        """
        return self.strategy.is_a(cls)  # type: ignore

    @auto_log
    def is_not_a(self, cls: Type) -> ExpectationResult:
        """
        Asserts that the actual value is not an instance of a specified class or type. This method is universally
        applicable across all data types, allowing for checks against undesired type conformity, thus ensuring
        that the actual value maintains expected type boundaries and constraints.

        This assertion is crucial for cases where specific type exclusions are necessary, either to prevent
        type-related errors or to enforce data integrity within a particular domain of the application.

        Args:
            cls (Type): The class or type that the actual value is expected not to be an instance of.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual value
                               is not an instance of the specified class or type, along with the actual and expected values.

        Note:
            This assertion's applicability and importance lie in its ability to enforce type constraints and exclusions
            across a wide range of contexts. It's a fundamental check for ensuring that variables or expressions do not
            inadvertently become instances of unwanted types.
        """
        return self.strategy.is_not_a(cls)  # type: ignore

    @auto_log
    def is_type_of(self, cls: Type) -> ExpectationResult:
        """
        Asserts that the actual value's type is exactly the specified class or type, not considering subclassing.
        This method provides a strict type check, ensuring that the actual value matches the expected type without
        any allowance for inheritance hierarchies. It's particularly useful in contexts where precise type control
        is necessary, such as when working with data structures or APIs that require specific types for correctness.

        Args:
            cls (Type): The class or type that the actual value is expected to exactly match.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual value's
                               type exactly matches the specified class or type. The result includes the actual and
                               expected types, and whether the strict type check passed or failed.

        Note:
            This assertion differs from `is_a` by not accepting instances of subclasses as valid. It enforces an
            exact type match, providing a higher degree of type specificity and control. Use this method when you
            need to ensure that no subclass instances are mistakenly treated as acceptable.
        """
        return self.strategy.is_type_of(cls)  # type: ignore

    @auto_log
    def is_not_type_of(self, cls: Type) -> ExpectationResult:
        """
        Asserts that the actual value's type does not exactly match the specified class or type. This method is used
        for strict type exclusion checks, ensuring that the actual value is not of the specified type, disregarding
        subclass relationships. It is particularly useful in scenarios where certain types must be explicitly avoided,
        either due to their behavior, characteristics, or the requirements of a given context.

        Args:
            cls (Type): The class or type that the actual value is expected not to match exactly.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual value's
                               type differs from the specified class or type. Includes information on the actual and
                               expected types, and whether the strict type exclusion check passed or failed.

        Note:
            Unlike `is_a` or `is_type_of`, this assertion strictly ensures that the actual value is not an instance
            of the specified type, including direct instances without considering subclass instances as equivalent.
            It provides a mechanism for enforcing type diversity and preventing type-specific behaviors or errors.
        """
        return self.strategy.is_not_type_of(cls)  # type: ignore

    @auto_log
    def is_string(self) -> ExpectationResult:
        """
        Asserts that the actual value is of type string. This method is essential for validating that the
        data being tested is in text format, which is a common requirement in various testing scenarios,
        including input validation, parsing, and formatting tasks.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the
                               actual value is a string. It includes details on the check performed,
                               the actual value, and whether the check passed or failed.

        Note:
            This assertion is particularly useful for ensuring that variables or expressions expected
            to produce text output indeed do so, aiding in the robustness and reliability of tests
            focused on string handling.
        """
        return self.strategy.is_string()  # type: ignore

    @auto_log
    def is_not_string(self) -> ExpectationResult:
        """
        Asserts that the actual value is not of type string. This method is used to ensure that the data
        being tested does not conform to text format when such a format is not expected, which can be
        crucial for type safety and correct data handling in various contexts.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the
                               actual value is not a string. It details the check performed, the actual
                               value, and whether the check passed or failed.

        Note:
            Utilizing this assertion helps maintain type integrity by verifying that variables or
            expressions that are not expected to produce string output adhere to those expectations,
            contributing to the overall reliability of the application or testing suite.
        """
        return self.strategy.is_not_string()  # type: ignore

    @auto_log
    def is_int(self) -> ExpectationResult:
        """
        Asserts that the actual value is of type integer. This method is vital for validating that
        data being tested conforms to an integer format, a common requirement in various scenarios
        where exact numeric values without decimal places are necessary.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is an integer. It includes details on the check performed,
                               the actual value, and whether the check passed or failed.

        Note:
            This assertion is particularly useful for ensuring that variables or expressions expected
            to produce integer output indeed do so, aiding in the reliability of tests focused on
            numeric handling and calculations.
        """
        return self.strategy.is_int()  # type: ignore

    @auto_log
    def is_not_int(self) -> ExpectationResult:
        """
        Asserts that the actual value is not of type integer. This method ensures that the data
        being tested does not conform to an integer format when such a format is not expected,
        crucial for maintaining type safety and correct numeric handling in various contexts.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is not an integer. It details the check performed,
                               the actual value, and whether the check passed or failed.

        Note:
            Utilizing this assertion helps maintain numeric type integrity by verifying that variables
            or expressions not expected to produce integer output adhere to those expectations,
            contributing to the overall data reliability.
        """
        return self.strategy.is_not_int()  # type: ignore

    @auto_log
    def is_float(self) -> ExpectationResult:
        """
        Asserts that the actual value is of type floating point. This method is essential for
        validating that data being tested conforms to a float format, necessary in scenarios
        where precision decimal values are required.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is a floating point number. It includes details on
                               the check performed, the actual value, and whether the check passed or failed.

        Note:
            This assertion ensures that variables or expressions expected to produce floating point
            output do so accurately, aiding in the precision and correctness of numeric calculations
            and validations.
        """
        return self.strategy.is_float()  # type: ignore

    @auto_log
    def is_not_float(self) -> ExpectationResult:
        """
        Asserts that the actual value is not of type floating point. This method ensures that the
        data being tested does not conform to a float format when such precision is not expected,
        important for maintaining numeric precision and type safety across different parts of an
        application or testing framework.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is not a floating point number. It details the check
                               performed, the actual value, and whether the check passed or failed.

        Note:
            By verifying that variables or expressions do not inadvertently produce floating point
            output when not expected, this assertion contributes to the overall accuracy and reliability
            of numeric data handling.
        """
        return self.strategy.is_not_float()  # type: ignore

    @auto_log
    def is_bool(self) -> ExpectationResult:
        """
        Asserts that the actual value is of type boolean. This method is essential for validating
        that data being tested conforms to a boolean format, necessary in scenarios where binary
        decisions or flags are required.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is a boolean. It includes details on the check performed,
                               the actual value, and whether the check passed or failed.

        Note:
            This assertion is particularly useful for ensuring that variables or expressions expected
            to result in boolean output (True or False) do so accurately, aiding in the correctness
            of conditional logic and binary decision-making processes.
        """
        return self.strategy.is_bool()  # type: ignore

    @auto_log
    def is_not_bool(self) -> ExpectationResult:
        """
        Asserts that the actual value is not of type boolean. This method ensures that the data
        being tested does not conform to a boolean format when such a format is not expected,
        important for maintaining type correctness and logical integrity in various contexts.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is not a boolean. It details the check performed,
                               the actual value, and whether the check passed or failed.

        Note:
            Utilizing this assertion helps maintain logical and type integrity by verifying that
            variables or expressions not expected to produce boolean output adhere to those
            expectations, contributing to the overall reliability of logical operations.
        """
        return self.strategy.is_not_bool()  # type: ignore

    @auto_log
    def is_date(self) -> ExpectationResult:
        """
        Asserts that the actual value is of type date. This method is crucial for validating that
        data being tested conforms to a date format, essential in scenarios involving scheduling,
        timelines, or any date-specific operations.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is a date. It includes details on the check performed,
                               the actual value, and whether the check passed or failed.

        Note:
            This assertion ensures that variables or expressions expected to represent calendar dates
            accurately do so, aiding in the accuracy and reliability of date-based calculations and validations.
        """
        return self.strategy.is_date()  # type: ignore

    @auto_log
    def is_not_date(self) -> ExpectationResult:
        """
        Asserts that the actual value is not of type date. This method is used to ensure that the data
        being tested does not conform to a date format when such specificity is not expected, crucial
        for maintaining data type diversity and correctness in temporal contexts.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is not a date. It details the check performed, the actual
                               value, and whether the check passed or failed.

        Note:
            By verifying that variables or expressions do not inadvertently produce date output when not
            expected, this assertion contributes to the overall temporal accuracy and data integrity.
        """
        return self.strategy.is_not_date()  # type: ignore

    @auto_log
    def is_time(self) -> ExpectationResult:
        """
        Asserts that the actual value is of type time. This method is vital for validating that data
        being tested conforms to a time format, necessary in scenarios where precise timekeeping or
        scheduling is involved.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is a time. It includes details on the check performed,
                               the actual value, and whether the check passed or failed.

        Note:
            This assertion is particularly useful for ensuring that variables or expressions expected
            to result in time output do so with precision, supporting the accuracy of time-based
            operations and schedules.
        """
        return self.strategy.is_time()  # type: ignore

    @auto_log
    def is_not_time(self) -> ExpectationResult:
        """
        Asserts that the actual value is not of type time. This method ensures that the data being
        tested does not conform to a time format when such precision is not expected, important for
        maintaining accurate and type-appropriate temporal data handling.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is not a time. It details the check performed, the actual
                               value, and whether the check passed or failed.

        Note:
            Utilizing this assertion helps ensure that time-based variables or expressions maintain
            their intended precision and type, avoiding unintended time type assignments and supporting
            the integrity of temporal data.
        """
        return self.strategy.is_not_time()  # type: ignore

    @auto_log
    def is_datetime(self) -> ExpectationResult:
        """
        Asserts that the actual value is of type datetime. This method is crucial for validating that
        data being tested conforms to a datetime format, essential in scenarios involving precise time
        and date operations, scheduling, or any temporal-specific operations.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is a datetime object. It includes details on the check
                               performed, the actual value, and whether the check passed or failed.

        Note:
            This assertion ensures that variables or expressions expected to represent specific points
            in time accurately do so, aiding in the reliability and precision of datetime-based calculations
            and validations.
        """
        return self.strategy.is_datetime()  # type: ignore

    @auto_log
    def is_list(self) -> ExpectationResult:
        """
        Asserts that the actual value is of type list. This method is essential for validating that data
        being tested conforms to a list format, necessary in scenarios where sequence order, collection
        operations, or list-specific manipulations are involved.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is a list. It includes details on the check performed,
                               the actual value, and whether the check passed or failed.

        Note:
            This assertion is particularly useful for ensuring that variables or expressions expected to
            produce list structures do so accurately, supporting the effectiveness of list-based operations
            and data handling.
        """
        return self.strategy.is_list()  # type: ignore

    @auto_log
    def is_dict(self) -> ExpectationResult:
        """
        Asserts that the actual value is of type dictionary. This method is critical for validating that
        data being tested conforms to a dictionary format, crucial in scenarios where key-value pair mappings,
        hash tables, or associative array manipulations are involved.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether
                               the actual value is a dictionary. It includes details on the check performed,
                               the actual value, and whether the check passed or failed.

        Note:
            This assertion ensures that variables or expressions expected to represent dictionary
            structures accurately do so, aiding in the precision and reliability of dictionary-based
            operations and data management.
        """
        return self.strategy.is_dict()  # type: ignore

    @auto_log
    def is_not_datetime(self) -> ExpectationResult:
        """
        Asserts that the actual value is not of type datetime. This method is important for scenarios where
        datetime objects are not expected, ensuring that data does not inadvertently conform to datetime formats
        when such precision and structure are unnecessary or could lead to errors.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual value
                               is not a datetime object. It includes details on the check performed, the actual value,
                               and whether the check passed or failed.

        Note:
            Utilizing this assertion helps in maintaining the intended data types within an application or testing
            environment, avoiding unexpected datetime type assignments that could affect the logic or operations
            relying on specific type constraints.
        """
        return self.strategy.is_not_datetime()  # type: ignore

    @auto_log
    def is_not_list(self) -> ExpectationResult:
        """
        Asserts that the actual value is not of type list. This method is useful for ensuring that data does not
        unintentionally conform to list structures, especially in contexts where sequence or collection types are
        not desired and could impact the processing or handling of the data incorrectly.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual value
                               is not a list. It includes details on the check performed, the actual value, and whether
                               the check passed or failed.

        Note:
            By verifying that variables or expressions do not produce list outputs when not expected, this assertion
            contributes to maintaining accurate and intended data structures, supporting the integrity of data handling.
        """
        return self.strategy.is_not_list()  # type: ignore

    @auto_log
    def is_not_dict(self) -> ExpectationResult:
        """
        Asserts that the actual value is not of type dictionary. This method is critical in contexts where dictionary
        or associative array formats are not expected, ensuring that data structures do not mistakenly adopt key-value
        pair mappings that could complicate or invalidate the intended data processing or manipulation.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual value
                               is not a dictionary. It includes details on the check performed, the actual value,
                               and whether the check passed or failed.

        Note:
            This assertion is vital for preventing unintended dictionary type assignments, preserving the clarity and
            correctness of data structures within applications or during testing, thereby aiding in the precision of
            data management and operations.
        """
        return self.strategy.is_not_dict()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy])
    def to_start_with(self, prefix: str) -> ExpectationResult:
        """
        Asserts that the actual string value starts with the specified prefix. This method is essential
        for validating string formatting, patterns, or protocols where a specific starting sequence is required.

        Args:
            prefix (str): The substring that the actual value is expected to start with.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the
                               actual string starts with the specified prefix, including the actual value
                               and whether the check passed or failed.

        Note:
            This assertion is particularly useful in testing and validating string data for compliance with
            expected formats, patterns, or protocols that dictate specific starting sequences.
        """
        return self.strategy.to_start_with(prefix)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy])
    def to_end_with(self, suffix: str) -> ExpectationResult:
        """
        Asserts that the actual string value ends with the specified suffix. This method is vital for checking
        string termination patterns or suffixes, ensuring that strings conclude with expected sequences.

        Args:
            suffix (str): The substring that the actual value is expected to end with.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual
                               string ends with the specified suffix, the actual value, and whether the
                               check passed or failed.

        Note:
            Utilizing this assertion aids in verifying that strings adhere to required ending patterns or suffixes,
            crucial for format validation and consistency in string data handling.
        """
        return self.strategy.to_end_with(suffix)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy])
    def to_match(self, pattern: str) -> ExpectationResult:
        """
        Asserts that the actual string value matches a specified regular expression pattern. This method is
        indispensable for complex string validation tasks, allowing for the verification of string formats,
        content, and structures against sophisticated patterns.

        Args:
            pattern (str): The regular expression pattern the actual string is expected to match.

        Returns:
            ExpectationResult: An object representing the result of the regex match check, including whether
                               the actual string matches the pattern, the actual value, and whether the check
                               passed or failed.

        Note:
            This assertion enables comprehensive validation of string data against complex patterns, supporting
            rigorous format and content checks.
        """
        return self.strategy.to_match(pattern)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy, ArrayStrategy])
    def to_be_empty(self) -> ExpectationResult:
        """
        Asserts that the actual string or collection (list, set, tuple) is empty or, for strings, contains only whitespace.
        This method is critical for validating that fields meant to hold textual data or collections are either not
        populated or contain non-meaningful data (such as whitespace for strings).

        For strings, it checks if the string is empty or contains only whitespace. For collections like lists, sets,
        and tuples, it verifies that the collection is empty.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual string
                               or collection is empty/whitespace-only, including the actual value, and whether
                               the check passed or failed.

        Note:
            This assertion is useful in ensuring data cleanliness and validation, particularly in scenarios where
            empty or whitespace-only strings, or empty collections, signify specific states or conditions.
        """
        return self.strategy.to_be_empty()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy])
    def not_to_start_with(self, prefix: str) -> ExpectationResult:
        """
        Asserts that the actual string value does not start with the specified prefix. This method is essential for
        cases where beginning with a certain sequence is not desired or could indicate an error.

        Args:
            prefix (str): The substring that the actual value is expected not to start with.

        Returns:
            ExpectationResult: An object representing the result of the check, including details on whether the actual
                               string does not start with the specified prefix, the actual value, and whether the check
                               passed or failed.

        Note:
            This assertion helps avoid unintended formatting or content at the start of strings, enhancing data validation.
        """
        return self.strategy.not_to_start_with(prefix)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy])
    def not_to_end_with(self, suffix: str) -> ExpectationResult:
        """
        Asserts that the actual string value does not end with the specified suffix. This method is vital for scenarios
        where terminating with a certain sequence is undesirable or incorrect.

        Args:
            suffix (str): The substring that the actual value is expected not to end with.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual string does
                               not end with the specified suffix, including the actual value and whether the check passed or failed.

        Note:
            Utilizing this assertion aids in ensuring strings do not mistakenly adopt specific ending sequences, supporting
            accurate format and content control.
        """
        return self.strategy.not_to_end_with(suffix)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy])
    def not_to_match(self, pattern: str) -> ExpectationResult:
        """
        Asserts that the actual string value does not match the specified regular expression pattern. This method is
        crucial for validating that string formats, contents, or structures do not align with unwanted patterns.

        Args:
            pattern (str): The regular expression pattern the actual string is expected not to match.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual string does
                               not match the pattern, including the actual value and whether the check passed or failed.

        Note:
            This assertion is key to avoiding specific, potentially problematic patterns in string data, facilitating
            more precise and restrictive format validations.
        """
        return self.strategy.not_to_match(pattern)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy, ArrayStrategy])
    def not_to_be_empty(self) -> ExpectationResult:
        """
        Asserts that the actual string or collection (list, set, tuple) is not empty. For strings, this method checks that
        the string is not empty nor contains only whitespace characters. For collections, it ensures that they are not empty,
        affirming the presence of elements within the collection.

        This method is crucial for scenarios where the presence of meaningful data in strings or collections is required,
        serving as a validation step to ensure data fields are appropriately populated and do not merely contain empty or
        whitespace-only values.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual string or
                               collection is not empty (and not just whitespace for strings), including the actual value,
                               and whether the check passed or failed.

        Note:
            Utilizing this assertion is essential in data validation processes where empty strings or collections could
            signify missing, incomplete, or incorrect data. It aids in maintaining the integrity and completeness of the
            data being handled or tested.
        """
        return self.strategy.not_to_be_empty()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy, ArrayStrategy])
    def to_have_length(self, expected_length: int) -> ExpectationResult:
        """
        Asserts that the actual string or collection (list, set, tuple) has a specific length. This method is crucial for
        scenarios where the exact size of the data structure is a significant factor, such as validating input or output data
        constraints, ensuring array sizes for algorithmic processing, or verifying string content length for formatting requirements.

        Args:
            expected_length (int): The expected length of the string or collection.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual string or
                               collection matches the specified length, including details on the actual size and whether
                               the check passed or failed.

        Note:
            This assertion facilitates precise control over the size of data structures, aiding in the enforcement of
            specific length requirements for strings and collections within applications or testing environments.
        """
        return self.strategy.to_have_length(expected_length)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy, ArrayStrategy])
    def not_to_have_length(self, unexpected_length: int) -> ExpectationResult:
        """
        Asserts that the actual string or collection (list, set, tuple) does not have a specific length. This method is useful
        for scenarios where certain sizes of data structures are to be avoided, such as preventing overly long input strings or
        ensuring collections do not exceed capacity constraints.

        Args:
            unexpected_length (int): The length that the actual string or collection is expected not to match.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual string or
                               collection does not match the specified length, including details on the actual size and
                               whether the check passed or failed.

        Note:
            This assertion is critical for avoiding specific data structure sizes, contributing to the robustness and
            reliability of data handling by enforcing size limitations or expectations.
        """
        return self.strategy.not_to_have_length(unexpected_length)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[StringStrategy])
    def to_contain_in_order(self, *elements) -> ExpectationResult:
        """
        Asserts that the actual string or collection (list, set, tuple) contains the specified elements in order. For strings,
        this method checks for the sequence of substrings; for collections, it verifies the order of elements. This assertion
        is vital for validating ordered data structures where the sequence of elements or characters is crucial.

        Args:
            *elements: The elements or substrings expected to appear in order within the actual value.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual string or
                               collection contains the specified elements in the given order, and whether the check
                               passed or failed.

        Note:
            Utilizing this assertion supports scenarios requiring strict order adherence within strings or collections,
            ensuring that elements appear exactly as specified, which is essential for sequence validation and integrity.
        """
        return self.strategy.to_contain_in_order(*elements)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[ArrayStrategy])
    def to_contain_exactly(self, *expected_elements) -> ExpectationResult:
        """
        Asserts that the actual collection (list, set, tuple) contains exactly the specified elements, no more, no less.
        This method ensures the precise composition of the collection, crucial for scenarios where the exact set of elements
        is necessary for correctness, such as validating the output of operations or the state of data structures.

        Args:
            *expected_elements: The elements expected to be exactly present in the collection.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual collection
                               contains exactly the specified elements, including the actual elements and whether the
                               check passed or failed.

        Note:
            This assertion is vital for verifying the exact composition of collections, supporting strict validation of
            element presence and ensuring no unexpected elements are included or required elements are omitted.
        """
        return self.strategy.to_contain_exactly(*expected_elements)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[ArrayStrategy])
    def to_contain_any_of(self, *expected_elements) -> ExpectationResult:
        """
        Asserts that the actual collection (list, set, tuple) contains any of the specified elements. This method is useful
        for cases where the presence of one or more elements from a specific set is sufficient for the collection's validity,
        allowing for flexibility in the composition of the collection.

        Args:
            *expected_elements: Elements at least one of which is expected to be found in the collection.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual collection
                               contains any of the specified elements, including which elements were found and whether
                               the check passed or failed.

        Note:
            Utilizing this assertion allows for the verification of partial composition requirements, ensuring that
            collections include one or more elements from a specified set, which can be crucial for data integrity
            and operational correctness.
        """
        return self.strategy.to_contain_any_of(*expected_elements)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[ArrayStrategy])
    def not_to_contain_any_of(self, *unwanted_elements) -> ExpectationResult:
        """
        Asserts that the actual collection (list, set, tuple) does not contain any of the specified elements. This method
        is crucial for ensuring that collections are free from unwanted elements, supporting scenarios where the exclusion
        of specific elements is necessary for data purity, security, or correctness.

        Args:
            *unwanted_elements: Elements none of which are expected to be found in the collection.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual collection
                               does not contain any of the specified unwanted elements, including the actual elements
                               and whether the check passed or failed.

        Note:
            This assertion aids in enforcing strict exclusion criteria for collections, ensuring that they do not
            inadvertently contain elements that could compromise data integrity, security, or operational logic.
        """
        return self.strategy.not_to_contain_any_of(*unwanted_elements)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[DictStrategy])
    def to_contain_key(self, key) -> ExpectationResult:
        """
        Asserts that the actual dictionary contains the specified key. This method is crucial for validating
        the structure and completeness of dictionary data, ensuring that expected keys are present.

        Args:
            key: The key expected to be present in the dictionary.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual
                               dictionary contains the specified key, including the actual keys and whether
                               the check passed or failed.

        Note:
            This assertion is vital for verifying the presence of specific keys within dictionaries, aiding in
            the validation of data structure integrity and the correctness of dictionary contents.
        """
        return self.strategy.to_contain_key(key)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[DictStrategy])
    def to_contain_keys(self, *keys) -> ExpectationResult:
        """
        Asserts that the actual dictionary contains all the specified keys. This method is used to ensure the
        dictionary's structure includes a specific set of keys, important for data completeness and integrity.

        Args:
            *keys: The keys expected to be present in the dictionary.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual
                               dictionary contains all the specified keys, with details on the actual keys and
                               whether the check passed or failed.

        Note:
            Employing this assertion helps in confirming the presence of multiple specific keys within a dictionary,
            supporting comprehensive validations of dictionary structures and their alignment with expected schemas.
        """
        return self.strategy.to_contain_keys(*keys)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[DictStrategy])
    def to_contain_value(self, value) -> ExpectationResult:
        """
        Asserts that the actual dictionary contains the specified value. This method is important for confirming
        that dictionaries hold expected values, crucial for validating the content and utility of the data structure.

        Args:
            value: The value expected to be present in the dictionary.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual
                               dictionary contains the specified value, including the actual values and whether
                               the check passed or failed.

        Note:
            This assertion ensures that dictionaries include specific values, aiding in the comprehensive validation
            of data content and enhancing the integrity and usability of dictionary-based data structures.
        """
        return self.strategy.to_contain_value(value)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[DictStrategy])
    def not_to_contain_key(self, key) -> ExpectationResult:
        """
        Asserts that the actual dictionary does not contain the specified key. This method is crucial for ensuring
        dictionaries do not include unintended keys, supporting data purity and structure validation.

        Args:
            key: The key expected not to be present in the dictionary.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual
                               dictionary does not contain the specified key, with details on the actual keys and
                               whether the check passed or failed.

        Note:
            Utilizing this assertion is essential for validating that dictionaries are free from unwanted keys,
            contributing to the accuracy and cleanliness of data structures.
        """
        return self.strategy.not_to_contain_key(key)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[DictStrategy])
    def not_to_contain_keys(self, *keys) -> ExpectationResult:
        """
        Asserts that the actual dictionary does not contain any of the specified keys. This method ensures that
        dictionaries are devoid of a set of unwanted keys, vital for maintaining data integrity and structure.

        Args:
            *keys: Keys expected not to be present in the dictionary.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual dictionary
                               does not contain any of the specified keys, with an overview of the actual keys and whether
                               the check passed or failed.

        Note:
            This assertion is key to ensuring dictionaries exclude specific keys, aiding in the strict control over
            dictionary contents and supporting the validation of data structure exclusiveness.
        """
        return self.strategy.not_to_contain_keys(*keys)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[DictStrategy])
    def not_to_contain_value(self, value) -> ExpectationResult:
        """
        Asserts that the actual dictionary does not contain the specified value. This method is used to verify that
        dictionaries exclude specific unwanted values, important for data content validation and integrity.

        Args:
            value: The value expected not to be present in the dictionary.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual dictionary
                               does not contain the specified value, including the actual values and whether the check
                               passed or failed.

        Note:
            Employing this assertion assists in confirming the absence of specific values within dictionaries,
            crucial for maintaining the purity and intended utility of the data structure.
        """
        return self.strategy.not_to_contain_value(value)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[DictStrategy])
    def to_match_schema(self, schema: Union[dict, str]) -> ExpectationResult:
        """
        Asserts that the actual dictionary matches a specified JSON schema. This method is crucial for validating
        complex data structures, ensuring that dictionaries conform to predefined formats, structures, and type
        requirements as defined by the JSON schema. It is particularly useful for API response validation, configuration
        data verification, and ensuring data integrity across various application components.

        Args:
            schema (Union[dict, str]): The JSON schema to validate against, provided either as a dictionary representing
                                       the schema or a string path to a JSON schema file.

        Returns:
            ExpectationResult: An object representing the result of the schema validation, detailing whether the actual
                               dictionary matches the specified JSON schema, including the validation outcome and any
                               schema validation errors encountered.

        Note:
            This assertion leverages the JSON Schema standard to provide comprehensive and flexible data validation,
            supporting a wide range of use cases from simple data structure checks to complex content validation
            scenarios. It is a powerful tool for maintaining data quality and structure conformity within applications.
        """
        return self.strategy.to_match_schema(schema)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[FileSystemStrategy])
    def to_be_file(self) -> ExpectationResult:
        """
        Asserts that the actual value represents a file in the filesystem. This method is essential for verifying
        that a given path or entity corresponds to a file, not a directory or other filesystem object, which is
        crucial for operations expecting to interact with file content.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual filesystem
                               entity is a file, including the path checked and whether the check passed or failed.

        Note:
            Utilizing this assertion ensures that file-specific operations, such as reading or writing content, are
            performed on valid file entities, aiding in the prevention of errors and the enforcement of filesystem
            integrity within applications or testing environments.
        """
        return self.strategy.to_be_file()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[FileSystemStrategy, ImageStrategy])
    def to_exist(self) -> ExpectationResult:
        """
        Asserts that the actual filesystem entity, whether a file or directory, exists at the specified path. This method
        is vital for confirming the presence of expected filesystem objects before proceeding with operations that require
        their existence, such as opening files or traversing directories.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the filesystem entity
                               exists, including the path checked and whether the check passed or failed.

        Note:
            This assertion is fundamental to ensuring the readiness of the filesystem for operations, supporting the
            robust handling of file and directory access, modification, and validation tasks.
        """
        return self.strategy.to_exist()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[FileSystemStrategy, ImageStrategy])
    def not_to_exist(self) -> ExpectationResult:
        """
        Asserts that the actual filesystem entity, whether a file or directory, does not exists at the specified path.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the filesystem entity
                               does not exists, including the path checked and whether the check passed or failed.

        Note:
            This assertion is fundamental to ensuring the readiness of the filesystem for operations, supporting the
            robust handling of file and directory access, modification, and validation tasks.
        """
        return self.strategy.not_to_exist()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[FileSystemStrategy])
    def to_be_directory(self) -> ExpectationResult:
        """
        Asserts that the actual value represents a directory in the filesystem. This method is critical for validating
        that a given path or entity corresponds to a directory, ensuring that operations expecting to interact with
        directory structures, such as listing contents or creating subdirectories, are feasible.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual filesystem
                               entity is a directory, including the path checked and whether the check passed or failed.

        Note:
            Employing this assertion verifies that directory-specific operations are executed on valid directory entities,
            aiding in the management and organization of filesystem structures within applications or during testing.
        """
        return self.strategy.to_be_directory()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[FileSystemStrategy])
    def to_have_size(self, expected_size: int) -> ExpectationResult:
        """
        Asserts that the actual filesystem entity (file or directory) has a specific size in bytes. This method is essential
        for validating the size of files or directories, ensuring they meet expected size constraints, whether to confirm
        file content integrity, to ensure directories are not overly large, or to match specific application requirements.

        Args:
            expected_size (int): The expected size in bytes of the file or directory.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual filesystem
                               entity matches the specified size, including the actual size and whether the check passed
                               or failed.

        Note:
            This assertion supports precise control over filesystem entity sizes, aiding in the verification of file and
            directory characteristics important for storage management, content validation, and application-specific
            constraints.
        """
        return self.strategy.to_have_size(expected_size)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[FileSystemStrategy])
    def not_to_have_size(self, unexpected_size: int) -> ExpectationResult:
        """
        Asserts that the actual filesystem entity (file or directory) does not have a specific size in bytes. This method
        is useful for scenarios where files or directories must not match a certain size, whether to avoid specific content
        sizes, to ensure directories do not fall under specific size limitations, or to prevent size-based constraints from
        being met.

        Args:
            unexpected_size (int): The size in bytes that the file or directory is expected not to have.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual filesystem
                               entity does not match the specified size, including the actual size and whether the check
                               passed or failed.

        Note:
            Utilizing this assertion ensures that filesystem entities do not inadvertently meet specific size criteria,
            contributing to the robustness and specificity of filesystem management and data validation processes.
        """
        return self.strategy.not_to_have_size(unexpected_size)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def to_be_odd(self) -> ExpectationResult:
        """
        Asserts that the actual numeric value is odd. This method is crucial for validating that a number
        does not divide evenly by two, indicating its odd nature, which can be important for certain mathematical,
        algorithmic, or data processing operations where odd numbers have specific significance.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual
                               numeric value is odd, including the actual value and whether the check passed
                               or failed.

        Note:
            This assertion is particularly useful in scenarios where the distinction between odd and even numbers
            impacts the logic or outcome of operations, supporting precise numeric validations.
        """
        return self.strategy.to_be_odd()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def to_be_even(self) -> ExpectationResult:
        """
        Asserts that the actual numeric value is even. This method validates that a number divides evenly by two,
        categorizing it as even, which is essential for operations, calculations, or conditions where even numbers
        are specifically required or expected.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual
                               numeric value is even, with details on the actual value and whether the check
                               passed or failed.

        Note:
            Employing this assertion helps ensure that numeric values meet specific evenness criteria, crucial for
            mathematical, algorithmic, or data processing tasks where even numbers play a pivotal role.
        """
        return self.strategy.to_be_even()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def to_be_positive(self) -> ExpectationResult:
        """
        Asserts that the actual numeric value is positive. This method is vital for confirming that a number is greater
        than zero, relevant in contexts where positive values are necessary for correctness, such as financial calculations,
        measurements, and various forms of data analysis.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual numeric
                               value is positive, including the actual value and whether the check passed or failed.

        Note:
            This assertion ensures that numbers adhere to positivity requirements, supporting operations and validations
            where negative values are not permissible or meaningful.
        """
        return self.strategy.to_be_positive()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def to_be_negative(self) -> ExpectationResult:
        """
        Asserts that the actual numeric value is negative. This method is crucial for ensuring that a number is less than
        zero, important for conditions, calculations, or analyses where negative values have specific implications or are
        expected based on the context.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual numeric
                               value is negative, with details on the actual value and whether the check passed or failed.

        Note:
            Utilizing this assertion facilitates the verification of numeric values against negativity criteria, vital
            for scenarios where the presence of negative numbers is significant or required.
        """
        return self.strategy.to_be_negative()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def to_be_in_between(
        self, lower_bound: float, upper_bound: float
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value is within a specified range, exclusive of the boundary values. This method
        is essential for ensuring that numbers fall within expected limits, crucial for operations or conditions that
        require values to be constrained within specific bounds.

        Args:
            lower_bound (float): The lower limit of the range, exclusive.
            upper_bound (float): The upper limit of the range, exclusive.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual numeric
                               value lies within the specified range, including the actual value, the specified range,
                               and whether the check passed or failed.

        Note:
            This assertion facilitates precise numeric range validations, supporting scenarios where value constraints
            within specific bounds are critical to the correctness and functionality of operations or analyses.
        """
        return self.strategy.to_be_in_between(lower_bound, upper_bound)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def not_to_be_in_between(
        self, lower_bound: float, upper_bound: float
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value does not lie within a specified range, exclusive of the boundary values. This method
        is useful for scenarios where values must be outside certain limits, either below the lower bound or above the upper bound,
        important for conditions that exclude a specific range of values.

        Args:
            lower_bound (float): The lower limit of the range, exclusive.
            upper_bound (float): The upper limit of the range, exclusive.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual numeric
                               value is outside the specified range, with details on the actual value, the specified range,
                               and whether the check passed or failed.

        Note:
            Employing this assertion ensures that numeric values do not fall within undesired ranges, crucial for maintaining
            exclusivity or specificity in numeric validations and analyses.
        """
        return self.strategy.not_to_be_in_between(lower_bound, upper_bound)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def to_be_close_to(
        self, expected_value: float, tolerance: float
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value is approximately equal to the expected value within a specified tolerance.
        This method is indispensable for validating numeric values where exact matches are impractical due to precision
        limitations or when slight deviations are acceptable.

        Args:
            expected_value (float): The value to which the actual value is compared.
            tolerance (float): The maximum allowed difference between the actual and expected values for the comparison to pass.

        Returns:
            ExpectationResult: An object representing the result of the comparison, detailing whether the actual numeric
                               value is within the tolerance range of the expected value, including the actual and expected
                               values, the tolerance, and whether the check passed or failed.

        Note:
            This assertion is key for performing flexible numeric comparisons, accommodating scenarios where slight variations
            from the expected value are permissible, supporting robustness in numeric validations.
        """
        return self.strategy.to_be_close_to(expected_value, tolerance)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def to_be_multiple_of(self, multiplier: float) -> ExpectationResult:
        """
        Asserts that the actual numeric value is a multiple of another specified value. This method is critical for verifying
        divisibility and multiplicative relationships, important in various mathematical, financial, or logical operations
        where specific multiples are required or expected.

        Args:
            multiplier (float): The value of which the actual value should be a multiple.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual numeric value
                               is a multiple of the specified value, including the actual value, the multiplier, and whether
                               the check passed or failed.

        Note:
            Utilizing this assertion helps ensure compliance with specific multiplicative requirements, aiding in the
            validation of numerical relationships and divisibility conditions.
        """
        return self.strategy.to_be_multiple_of(multiplier)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def to_be_in_range(
        self, lower_bound: float, upper_bound: float
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value lies within a specified range, inclusive of the boundary values. This method
        is essential for scenarios requiring values to be constrained within specified bounds, including the limits themselves,
        crucial for validations where inclusivity of boundary values is necessary.

        Args:
            lower_bound (float): The inclusive lower limit of the range.
            upper_bound (float): The inclusive upper limit of the range.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual numeric
                               value falls within the inclusive range, with details on the actual value, the specified
                               range, and whether the check passed or failed.

        Note:
            This assertion facilitates numeric validations with inclusive boundary conditions, accommodating scenarios
            where boundary values are considered valid and significant for the operation or condition being validated.
        """
        return self.strategy.to_be_in_range(lower_bound, upper_bound)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def not_to_be_in_range(
        self, lower_bound: float, upper_bound: float
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value does not lie within a specified range, inclusive of the boundary values. This method
        is useful for conditions where values must be explicitly outside the specified limits, important for excluding a specific
        range of values, including the boundaries, from being considered valid.

        Args:
            lower_bound (float): The inclusive lower limit of the range to be excluded.
            upper_bound (float): The inclusive upper limit of the range to be excluded.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual numeric
                               value falls outside the inclusive range, with an overview of the actual value, the specified
                               range, and whether the check passed or failed.

        Note:
            Employing this assertion ensures numeric values fall outside of undesired inclusive ranges, crucial for maintaining
            exclusivity in numeric validations and analyses where specific ranges of values are not permissible.
        """
        return self.strategy.not_to_be_in_range(lower_bound, upper_bound)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def to_be_zero(self) -> ExpectationResult:
        """
        Asserts that the actual numeric value is zero. This method is crucial for validating scenarios where the
        value is expected to result in zero, a common condition in calculations, reset operations, or when checking
        for the absence of a quantity.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual numeric
                               value is zero, including the actual value and whether the check passed or failed.

        Note:
            This assertion is particularly useful for confirming the neutral or null state of numeric calculations
            or conditions, aiding in the precision and accuracy of numeric validations.
        """
        return self.strategy.to_be_zero()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def not_to_be_odd(self) -> ExpectationResult:
        """
        Asserts that the actual numeric value is not odd. This method is useful for ensuring that numbers are even,
        excluding odd numbers from passing the check, important in contexts where even numbers are required or expected
        due to their properties or the requirements of a given operation.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual numeric
                               value is not odd, with details on the actual value and whether the check passed or failed.

        Note:
            Employing this assertion helps exclude odd numbers from consideration, supporting scenarios or calculations
            where evenness is a critical attribute of the numeric values involved.
        """
        return self.strategy.not_to_be_odd()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def not_to_be_even(self) -> ExpectationResult:
        """
        Asserts that the actual numeric value is not even. This method is essential for scenarios that specifically
        require odd numbers, ensuring that even numbers do not satisfy the condition, important for operations or
        validations where the distinct properties of odd numbers are necessary.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual numeric
                               value is not even, including the actual value and whether the check passed or failed.

        Note:
            Utilizing this assertion facilitates the exclusion of even numbers in validations, emphasizing the
            requirement for odd numbers due to their unique characteristics or the specific needs of the operation.
        """
        return self.strategy.not_to_be_even()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def not_to_be_positive(self) -> ExpectationResult:
        """
        Asserts that the actual numeric value is not positive. This method is vital for validating that numbers are
        either negative or zero, excluding positive numbers from passing the check, crucial for contexts where non-positive
        values are required due to the nature of the operation or the expected outcomes.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual numeric
                               value is not positive, with details on the actual value and whether the check passed or failed.

        Note:
            This assertion ensures that numeric values are suitable for conditions or operations where positivity is
            not permissible, supporting accurate and specific numeric validations where negative or neutral values are
            relevant.
        """
        return self.strategy.not_to_be_positive()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def not_to_be_negative(self) -> ExpectationResult:
        """
        Asserts that the actual numeric value is not negative, meaning it is zero or positive. This method is crucial
        for scenarios requiring non-negative numbers, ensuring values are suitable for operations or contexts where
        negatives are not permissible.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual numeric
                               value is not negative, including the actual value and whether the check passed or failed.

        Note:
            Employing this assertion aids in confirming suitability for contexts demanding non-negative numbers,
            enhancing validations where negativity would be incorrect or undesirable.
        """
        return self.strategy.not_to_be_negative()  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def not_to_be_close_to(
        self, expected_value: float, tolerance: float
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value is not approximately equal to the expected value within a specified tolerance.
        This method is vital for scenarios where numeric values must distinctly differ from a reference value beyond a minimal
        margin, crucial for avoiding near-matches that could lead to incorrect assumptions or outcomes.

        Args:
            expected_value (float): The value that the actual value should not approximate.
            tolerance (float): The tolerance within which the actual value should not fall around the expected value.

        Returns:
            ExpectationResult: An object representing the result of the check, indicating whether the actual numeric
                               value differs from the expected value by more than the specified tolerance, including
                               the actual and expected values, the tolerance, and whether the check passed or failed.

        Note:
            This assertion is key for ensuring clear differentiation from specific numeric benchmarks, supporting
            precise control over acceptable value ranges and distinctions in numeric validations.
        """
        return self.strategy.not_to_be_close_to(expected_value, tolerance)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def not_to_be_multiple_of(self, multiplier: float) -> ExpectationResult:
        """
        Asserts that the actual numeric value is not a multiple of another specified value. This method ensures
        that the actual value does not divide evenly by the multiplier, important for validating numerical properties
        or requirements where being a multiple would be incorrect or problematic.

        Args:
            multiplier (float): The number that the actual value should not be a multiple of.

        Returns:
            ExpectationResult: An object representing the result of the check, detailing whether the actual numeric
                               value is not a multiple of the specified number, including the actual value, the
                               multiplier, and whether the check passed or failed.

        Note:
            Utilizing this assertion facilitates numeric validations where specific multiplicative relationships
            are to be avoided, enhancing the specificity and accuracy of numerical checks.
        """
        return self.strategy.not_to_be_multiple_of(multiplier)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy, ColorStrategy])
    def to_be_greater_than(
        self, expected_value: Union[bool, int, float, Color, str]
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value or color's grayscale value is greater than the specified comparison value or
        color's grayscale value. This method is versatile, supporting comparisons against both numeric values and colors,
        where color values can be specified as a Color object or a string in RGB, RGBA, or HEX formats. For color comparisons,
        the grayscale value of the color is used to determine "greater than" relationships.

        Args:
            expected_value (Union[bool, int, float, Color, str]): The numeric value or color (as a Color object or a color
                                                                  string in RGB, RGBA, HEX formats) that the actual value
                                                                  is expected to exceed. Color strings will be auto-parsed.

        Returns:
            ExpectationResult: An object representing the result of the comparison, detailing whether the actual numeric
                               value or color's grayscale value exceeds the specified comparison value or color's grayscale
                               value, including the actual and comparison values, and whether the check passed or failed.

        Note:
            This assertion is particularly useful for scenarios requiring validation of numerical thresholds or color
            intensity comparisons. It accommodates a broad range of validation tasks, from simple numerical comparisons
            to complex visual properties assessments, by interpreting color comparisons through grayscale values, ensuring
            a consistent basis for comparison across different representations.
        """
        return self.strategy.to_be_greater_than(expected_value)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy, ColorStrategy])
    def to_be_less_than(
        self, expected_value: Union[bool, int, float, Color, str]
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value or color's grayscale value is less than the specified comparison value or
        color's grayscale value. This method supports comparisons against both numeric values and colors, where color values
        can be specified as a Color object or a string in RGB, RGBA, or HEX formats. For color comparisons, the grayscale
        value of the color is used to determine "less than" relationships.

        Args:
            expected_value (Union[bool, int, float, Color, str]): The numeric value or color (as a Color object or a color
                                                                  string in RGB, RGBA, HEX formats) that the actual value
                                                                  is expected to be less than. Color strings will be auto-parsed.

        Returns:
            ExpectationResult: An object representing the result of the comparison, detailing whether the actual numeric
                               value or color's grayscale value is less than the specified comparison value or color's
                               grayscale value, including the actual and comparison values, and whether the check passed
                               or failed.

        Note:
            This assertion is critical for validating that values fall below specified numerical thresholds or color
            intensities, accommodating a wide range of comparisons from numerical values to complex visual properties,
            ensuring comparisons are grounded in grayscale values for color.
        """
        return self.strategy.to_be_less_than(expected_value)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy, ColorStrategy])
    def to_be_greater_than_or_equal_to(
        self, expected_value: Union[bool, int, float, Color, str]
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value or color's grayscale value is greater than or equal to the specified comparison
        value or color's grayscale value. This method enables comparisons with numeric values and colors, including color
        values specified as a Color object or a string. Grayscale values are used for color comparisons to establish "greater
        than or equal to" relationships.

        Args:
            expected_value (Union[bool, int, float, Color, str]): The numeric value or color to compare against, where
                                                                  colors can be provided as Color objects or strings in
                                                                  RGB, RGBA, HEX formats and will be auto-parsed.

        Returns:
            ExpectationResult: An object detailing the comparison's outcome, showing whether the actual value meets or
                               exceeds the specified value or color's grayscale value, along with the comparison metrics
                               and the check's result.

        Note:
            Ideal for scenarios requiring minimum threshold validations or color intensity checks, this method's
            flexibility supports a broad spectrum of validation tasks, leveraging grayscale values for color comparisons.
        """
        return self.strategy.to_be_greater_than_or_equal_to(expected_value)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy, ColorStrategy])
    def to_be_less_than_or_equal_to(
        self, expected_value: Union[bool, int, float, Color, str]
    ) -> ExpectationResult:
        """
        Asserts that the actual numeric value or color's grayscale value is less than or equal to the specified comparison
        value or color's grayscale value. This method is adaptable for comparisons against both numeric values and colors,
        where color values can be specified as a Color object or a string in RGB, RGBA, or HEX formats. For color comparisons,
        the grayscale value of the color is used to determine "less than or equal to" relationships, ensuring a fair and
        consistent basis for comparison.

        Args:
            expected_value (Union[bool, int, float, Color, str]): The numeric value or color (as a Color object or a color
                                                                  string in RGB, RGBA, HEX formats) that the actual value
                                                                  is expected to be less than or equal to. Color strings
                                                                  will be auto-parsed into Color objects for comparison.

        Returns:
            ExpectationResult: An object representing the result of the comparison, detailing whether the actual numeric
                               value or color's grayscale value is less than or equal to the specified comparison value
                               or color's grayscale value, including the actual and comparison values, and whether the
                               check passed or failed.

        Note:
            This assertion is particularly valuable in scenarios requiring validation against upper limits or ensuring
            color intensities do not exceed specified levels. It accommodates a broad range of validation tasks by
            interpreting color comparisons through grayscale values, facilitating consistent and meaningful comparisons
            across different representations and formats.
        """
        return self.strategy.to_be_less_than_or_equal_to(expected_value)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[NumericStrategy])
    def to_be_divisible_by(self, divisor: float) -> ExpectationResult:
        """
        Asserts that the actual numeric value is divisible by the specified divisor. This method is crucial for validating
        mathematical properties of numbers, ensuring that the actual value can be evenly divided by another number, which
        is significant for operations, algorithms, or conditions predicated on divisibility.

        Args:
            divisor (float): The number by which the actual numeric value should be divisible.

        Returns:
            ExpectationResult: An object representing the result of the divisibility check, detailing whether the actual
                               numeric value is divisible by the specified divisor, including the actual value, the divisor,
                               and whether the check passed or failed.

        Note:
            This assertion is particularly useful in scenarios where divisibility is a key factor in the logic or outcome
            of operations, supporting precise validations of numerical relationships and ensuring compliance with specific
            mathematical conditions.
        """
        return self.strategy.to_be_divisible_by(divisor)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[ColorStrategy])
    def to_be_approximately_equal(
        self,
        expected_value: Union[Color, str],
        percentage_threshold: int = 5,
        alpha_threshold: float = 0.1,
    ) -> ExpectationResult:
        """
        Asserts that the actual Color object is approximately equal to another specified Color object or a color defined
        by a string (in RGB, RGBA, or HEX format), within defined thresholds for grayscale percentage difference and alpha
        component difference. This method is essential for validating color similarities where exact matches are not
        required, accommodating minor variances in color representation or perception.

        Args:
            expected_value (Union[Color, str]): The expected Color object or color string (RGB, RGBA, HEX) to compare
                                                against the actual Color object.
            percentage_threshold (int): The maximum allowed percentage difference in grayscale values between the actual
                                        and expected Color objects to still consider them approximately equal.
            alpha_threshold (float): The maximum allowed difference in the alpha component (transparency) between the
                                     actual and expected Color objects to still consider them approximately equal.

        Returns:
            ExpectationResult: An object representing the result of the color comparison, detailing whether the actual
                               Color object is within the specified thresholds of the expected color, including the actual
                               and expected colors, the thresholds used for comparison, and whether the check passed or failed.

        Note:
            This assertion supports nuanced color comparisons, acknowledging slight variations in color and transparency
            that may be acceptable in many applications. It allows for flexible validation of color properties, ensuring
            that colors are similar to an acceptable degree based on the provided thresholds.
        """
        return self.strategy.to_be_approximately_equal(  # type: ignore
            expected_value, percentage_threshold, alpha_threshold
        )  # type: ignore

    @auto_log
    @type_check(supported_strategies=[ImageStrategy])
    def to_be_similar(
        self,
        expected_value: Union[str, Image],
        mismatch_threshold: float = 10,
        compare_regions: Optional[list] = None,
        exclude_regions: Optional[list] = None,
    ) -> ImageExpectationResult:
        """
        Asserts that the actual image is similar to the expected image within a defined mismatch threshold,
        optionally considering or ignoring specific regions for a more targeted comparison.

        This method compares the actual image to the expected image, allowing for a specified degree of variation
        between them as defined by the mismatch_threshold. The comparison can be fine-tuned by specifying regions
        of the image to specifically compare or exclude from the comparison. The comparison algorithm assesses
        similarity on a pixel-by-pixel basis, adjusted for the designated threshold and regional focus.

        The mismatch_threshold parameter defines the acceptable percentage difference between the images, allowing
        for minor variations due to compression artifacts, rendering differences, or other acceptable noise. The
        method supports selective focus through compare_regions and selective ignorance via exclude_regions, enabling
        nuanced comparison scenarios where full image matching is unnecessary or impractical.

        Args:
            expected_value (Image): The expected image to compare against the actual image. It should be an instance
                                    of the Image class, encapsulating the image data along with any relevant metadata.
            mismatch_threshold (float): The permissible percentage difference between the images, representing the
                                        tolerance for discrepancies to still consider the images as similar.
            compare_regions (Optional[list]): Optional list of regions to specifically include in the comparison, with
                                              each region defined as a dictionary containing 'x', 'y', 'width', and 'height'.
            exclude_regions (Optional[list]): Optional list of regions to exclude from the comparison, with each region
                                              similarly defined as a dictionary.

        Returns:
            ImageExpectationResult: An object encapsulating the comparison result, indicating whether the actual image
                                    is considered similar to the expected image within the threshold and any specified
                                    regional focus. The result includes a similarity score and may include a difference
                                    image for visualization.
        """
        return self.strategy.to_be_similar(expected_value, mismatch_threshold, compare_regions, exclude_regions)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[ImageStrategy])
    def to_match_in_specified_regions(
        self,
        expected_value: Image,
        compare_regions: list,
        mismatch_threshold: float = 0,
    ) -> ImageExpectationResult:
        """
        Asserts that selected regions within the actual image match corresponding regions in the expected image,
        within an optional mismatch threshold. This method allows focused comparison on parts of the images that
        are of particular interest, potentially ignoring the rest of the image content.

        The compare_regions argument should be a list of dictionaries, each defining a region with 'x', 'y', 'width',
        and 'height' keys. The comparison assesses each specified region independently, comparing the actual image's
        region against the corresponding region in the expected image. If a mismatch_threshold is provided, minor
        differences between the compared regions up to the specified threshold are tolerated.

        This method is especially useful for scenarios where only certain parts of the image are relevant for
        comparison, allowing testers to specify exactly which regions should match between the actual and expected
        images, thus providing granular control over the comparison process.

        Args:
            expected_value (Image): The expected image to compare against the actual image. It should be an instance
                                    of the Image class, containing the image data along with any relevant metadata.
            compare_regions (list): A list of dictionaries, each specifying a rectangular region in the images to
                                    compare. Each dictionary should have 'x', 'y', 'width', and 'height' keys.
            mismatch_threshold (float, optional): An optional threshold for allowed mismatch percentage within the
                                                  specified regions, defaulting to 0 for an exact match requirement.

        Returns:
            ImageExpectationResult: An object encapsulating the comparison result, indicating whether the specified
                                    regions of the actual image match those in the expected image within the given
                                    tolerance. Includes detailed results for each region compared, and a comprehensive
                                    match assessment.
        """
        return self.strategy.to_match_in_specified_regions(expected_value, compare_regions, mismatch_threshold)  # type: ignore

    @auto_log
    @type_check(supported_strategies=[ImageStrategy])
    def to_match_excluding_regions(
        self,
        expected_value: Image,
        exclude_regions: list,
        mismatch_threshold: float = 0,
    ) -> ImageExpectationResult:
        """
        Asserts that the actual image matches the expected image, excluding the differences in specified regions,
        within a permissible mismatch threshold. This method allows exclusion of certain image areas from the
        comparison, focusing the match assessment on the remaining regions.

        The exclude_regions argument should be a list of dictionaries, each dictating a region to be excluded with
        'x', 'y', 'width', and 'height' keys. These regions are ignored during the comparison, enabling testers to
        isolate and exclude areas with known or irrelevant differences. The mismatch_threshold parameter allows
        a defined tolerance level for the matching process in the non-excluded areas of the images.

        This functionality is particularly valuable when certain image sections are dynamic or irrelevant to the
        test's intent, enabling precise and focused image analysis that disregards these areas.

        Args:
            expected_value (Image): The expected image to compare against the actual image, encapsulating the image
                                    data along with any pertinent metadata.
            exclude_regions (list): A list of dictionaries, each specifying a rectangular region in the images to
                                    be excluded from the comparison. Each dictionary should define 'x', 'y', 'width',
                                    and 'height' keys.
            mismatch_threshold (float, optional): An optional threshold defining the allowed percentage of mismatch
                                                 in the non-excluded areas, with 0 requiring exact match.

        Returns:
            ImageExpectationResult: An object detailing the comparison results, indicating whether the non-excluded
                                    regions of the actual image match the expected image within the set mismatch
                                    tolerance. The result object provides an aggregate assessment and may include
                                    detailed analysis or visualization data.
        """
        return self.strategy.to_match_excluding_regions(expected_value, exclude_regions, mismatch_threshold)  # type: ignore
