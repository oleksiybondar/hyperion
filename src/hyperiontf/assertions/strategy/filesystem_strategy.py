from .default_strategy import DefaultStrategy
from hyperiontf.assertions.expectation_result import ExpectationResult
from hyperiontf.fs import File, Dir


class FileSystemStrategy(DefaultStrategy):
    types = [File, Dir]

    def to_be_file(self) -> ExpectationResult:
        """
        Asserts that the actual value is a file.

        Returns:
            ExpectationResult: The result of the assertion.
        """
        result = isinstance(self.actual_value, File)
        message = "Expected to be a file."
        return ExpectationResult(
            result=result,
            actual_value=str(self.actual_value),
            expected_value=None,
            method="to_be_file",
            human_readable_description=message,
        )

    def to_exist(self) -> ExpectationResult:
        """
        Asserts that the file or directory exists.

        Returns:
            ExpectationResult: The result of the assertion.
        """
        result = self.actual_value.exists()
        message = "Expected to exist."
        return ExpectationResult(
            result=result,
            actual_value=str(self.actual_value),
            expected_value=None,
            method="to_exist",
            human_readable_description=message,
        )

    def to_be_directory(self) -> ExpectationResult:
        """
        Asserts that the actual value is a directory.

        Returns:
            ExpectationResult: The result of the assertion.
        """
        result = isinstance(self.actual_value, Dir)
        message = "Expected to be a directory."
        return ExpectationResult(
            result=result,
            actual_value=str(self.actual_value),
            expected_value=None,
            method="to_be_directory",
            human_readable_description=message,
        )

    def to_be(self, expected_value) -> ExpectationResult:
        """
        For files, asserts that the checksum of the actual file matches the expected file's checksum.
        For directories, this assertion could compare directory signatures (e.g., a list of filenames).

        Args:
            expected_value (File or Dir): The expected file or directory to compare against.

        Returns:
            ExpectationResult: The result of the assertion.
        """
        if isinstance(self.actual_value, File) and isinstance(expected_value, File):
            result = self.actual_value.checksum() == expected_value.checksum()
            message = "Expected file checksums to match."

            return ExpectationResult(
                result=result,
                actual_value=str(self.actual_value),
                expected_value=str(expected_value),
                method="to_be",
                human_readable_description=message,
            )

        return super().to_be(expected_value)

    def not_to_exist(self) -> ExpectationResult:
        """
        Asserts that the file or directory does not exist.

        Returns:
            ExpectationResult: The result of the assertion.
        """
        result = not self.actual_value.exists()
        message = "Expected not to exist."
        return ExpectationResult(
            result=result,
            actual_value=str(self.actual_value),
            expected_value=None,
            method="not_to_exist",
            human_readable_description=message,
        )

    def to_have_size(self, expected_size) -> ExpectationResult:
        """
        Asserts that the file or directory has the specified size.

        For a file, this asserts the file size in bytes matches the expected size.
        For a directory, this asserts the total size of all files within the directory matches the expected size.

        Args:
            expected_size (int): The expected size in bytes.

        Returns:
            ExpectationResult: The result of the assertion, indicating whether the actual size matches the expected size.
        """
        actual_size = self.actual_value.size()
        result = actual_size == expected_size
        message = f"Expected size to be {expected_size} bytes."
        return ExpectationResult(
            result=result,
            actual_value=actual_size,
            expected_value=expected_size,
            method="to_have_size",
            human_readable_description=message,
        )

    def not_to_have_size(self, expected_size) -> ExpectationResult:
        """
        Asserts that the file or directory does not have the specified size.

        For a file, this asserts the file size in bytes does not match the expected size.
        For a directory, this asserts the total size of all files within the directory does not match the expected size.

        Args:
            expected_size (int): The size in bytes that the file or directory is expected not to have.

        Returns:
            ExpectationResult: The result of the assertion, indicating whether the actual size differs from the expected size.
        """
        actual_size = self.actual_value.size()
        result = actual_size != expected_size
        message = f"Expected size not to be {expected_size} bytes."
        return ExpectationResult(
            result=result,
            actual_value=actual_size,
            expected_value=expected_size,
            method="not_to_have_size",
            human_readable_description=message,
        )
