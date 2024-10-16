import pytest
from hyperiontf.executors.pytest.helper.test_case import TestCase


@pytest.fixture(autouse=True)
def hyperion_test_case_setup(request):
    reporter = TestCase(request)
    request.addfinalizer(reporter.finalize)
