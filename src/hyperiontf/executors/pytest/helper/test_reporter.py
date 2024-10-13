from datetime import datetime
import sys
from hyperiontf.configuration import config
from hyperiontf.exception import HyperionException
from hyperiontf.logging import getLogger
from hyperiontf.helpers.string_helpers import method_name_to_human_readable
from hyperiontf.ui.automation_adapter_manager import AutomationAdaptersManager

# List of reserved pytest markers
RESERVED_MARKERS = [
    "skip",  # Marker to skip the test
    "skipif",  # Marker to conditionally skip the test
    "xfail",  # Marker for tests expected to fail
    "parametrize",  # Marker to parametrize test cases
    "usefixtures",  # Marker for tests that use fixtures
    "filterwarnings",  # Marker to filter specific warnings
    "tryfirst",  # Marker for pytest hooks to run first
    "trylast",  # Marker for pytest hooks to run last
]

logger = getLogger()


class TestReporter:
    """
    TestReporter is a helper class designed to manage logging and metadata collection
    for a test during its execution in pytest. It logs the test's start, end, duration,
    and results, and can handle exceptions and dump test state if the test fails.

    It is intended to be used alongside pytest fixtures, ensuring proper logging
    and test result recording.

    Attributes:
        request (FixtureRequest): The pytest request object passed from the fixture.
        start_time (datetime): The timestamp when the test started.
    """

    def __init__(self, request):
        """
        Initialize the TestReporter class and prepare logging for the test.

        Args:
            request (FixtureRequest): The pytest request object containing test metadata.
        """
        self.request = request
        self.start_time = datetime.now()
        self._init_test_log()

    def _init_test_log(self):
        """
        Initialize logging for the test. Logs initial metadata and introductory
        information such as test name, description, and tags.
        """
        logger.init_test_log(self.test_name)
        self._log_initial_meta()
        self._log_intro()

    def _log_intro(self):
        """
        Log an introductory message indicating the start of the test execution.
        """
        logger.info(f"Starting '{self.test_name}' test execution")

    def _log_initial_meta(self):
        """
        Log the initial metadata, including the test name, description, and tags.
        """
        logger.add_meta("testName", self.test_name)
        logger.add_meta("testDescription", self.test_description)
        if len(self.test_tags) > 0:
            logger.add_meta("testTags", self.test_tags)

    def _log_final_meta(self):
        """
        Log final metadata at the end of the test, including the duration and status.
        """
        logger.add_meta("testDuration", str(datetime.now() - self.start_time))
        logger.add_meta("testStatus", self.test_status)

    @staticmethod
    def _close_log_folders():
        """
        Close all open logging folders. This is useful when using structured logging
        formats like HTML, where nested logs can be properly closed.
        """
        logger.pop_all()

    def _log_exception(self):
        """
        Log critical information in case the test fails with an exception.
        """
        if self.test_status == "Failed":
            logger.critical(
                "Test Failed with Exception", exc_info=self._fetch_last_exception()
            )

    @staticmethod
    def _fetch_last_exception():
        """
        Fetch the most recent exception information.

        This method tries to retrieve the most recent exception in the following order:

        1. It first checks if the current exception is available via `sys.exc_info()`.
        2. If no exception is active, it checks if `sys.last_type`, `sys.last_value`,
           and `sys.last_traceback` exist (used in interactive sessions).
        3. If neither of the above provides information, it falls back to the cached
           exception details stored in `HyperionException.last_exec_info`.

        Returns:
            tuple:
                - The type of the last exception (`type` or `None`).
                - The exception instance (`BaseException` or `None`).
                - The traceback object associated with the last exception or cached traceback (or `None`).
        """
        # Get the current active exception from sys.exc_info()
        exc_type, exc_value, exc_traceback = sys.exc_info()

        if exc_type:
            return exc_type, exc_value, exc_traceback

        # Check for exception details in interactive sessions (sys.last_type, etc.)
        if hasattr(sys, "last_type"):
            return (sys.last_type, sys.last_value, sys.last_traceback)

        # Fall back to the cached exception details from HyperionException
        return HyperionException.last_exec_info

    def _log_dumps(self):
        """
        Create a dump of the test's state in case of failure or if post-mortem dumps
        are enabled in the configuration. Dumps are created using the automation adapters.
        """
        if self.test_status == "Failed" or config.page_object.post_morten_dumps:
            AutomationAdaptersManager().make_state_dump()

    @staticmethod
    def _finalize_automation():
        """
        Finalize automation by quitting all automation adapters if auto quit is enabled
        in the configuration.
        """
        if config.page_object.auto_quit:
            AutomationAdaptersManager().quit_all()

    @property
    def test_node(self):
        """
        Return the pytest node for the current test.

        Returns:
            Node: The pytest node object containing test metadata.
        """
        return self.request.node

    @property
    def raw_test_name(self):
        """
        Get the test name as it appears in pytest.request.node object.

        Returns:
           str: raw test name string.
        """
        return self.test_node.name

    @property
    def test_name(self):
        """
        Get the test name in a human-readable format.

        Returns:
            str: The test name converted to a human-readable string.
        """
        return method_name_to_human_readable(self.raw_test_name)

    @property
    def test_tags(self):
        """
        Collect and return a list of all non-reserved markers applied to the test.

        Returns:
            list: A list of tags applied to the test.
        """
        tags = []
        for marker in self.test_node.own_markers:
            if marker.name not in RESERVED_MARKERS:
                tags.append(marker.name)
            if marker.name == "tag" or marker.name == "tags":
                tags += marker.args
        return list(set(tags))

    @property
    def test_status(self):
        """
        Determine and return the current status of the test.

        Returns:
            str: The test status, which can be "Passed", "Failed", or "Skipped".
        """
        last_entry = list(self.test_node.stash._storage.values())[-1]
        if last_entry.get("call"):
            if last_entry["call"]:
                return "Passed"
            else:
                return "Failed"
        elif "setup" in last_entry:
            return "Failed"
        else:
            return "Skipped"

    @property
    def test_description(self):
        """
        Retrieve and return the test's docstring as its description.

        Returns:
            str: The description of the test, extracted from the test function's docstring.
        """
        name = self.raw_test_name.split("[")[0]
        description = getattr(self.test_node.module, name).__doc__ or ""
        return description.strip()

    def finalize(self):
        """
        Finalize the test reporting. This includes logging the final metadata,
        closing log folders, dumping test state if necessary, and finalizing automation adapters.
        """
        self._log_final_meta()
        self._close_log_folders()
        self._log_exception()
        self._log_dumps()
        self._finalize_automation()
