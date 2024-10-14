import pytest
from hyperiontf.executors.pytest.helper.test_reporter import TestReporter


@pytest.fixture(autouse=True)
def automatic_log_setup(request):
    reporter = TestReporter(request)
    request.addfinalizer(reporter.finalize)
