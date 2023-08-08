from datetime import datetime
import pytest
import sys

from hyperiontf.logging import getLogger
from hyperiontf.helpers.string_helpers import method_name_to_human_readable
from hyperiontf.ui.automation_adapter_manager import AutomationAdaptersManager

logger = getLogger()

known_reserved_markers = [
    "skip",
    "skipif",
    "xfail",
    "parametrize",
    "usefixtures",
    "filterwarnings",
    "tryfirst",
    "trylast",
]


def init_test_log(node):
    logger.init_test_log(node.name)


def add_failure_exception(node):
    # TODO: this doesnt work, must be updated in future, for now Hyperion expectation exceptions are duplicated with
    #       logger.critical, need to find better approach with node data
    logger.critical("Test Failed with Exception", exc_info=sys.exc_info())
    AutomationAdaptersManager().make_state_dump()


def add_test_status(node):
    last_entry = list(node.stash._storage.values()).pop()
    if last_entry.get("call"):
        if last_entry["call"]:
            status = "Passed"
        else:
            status = "Failed"
            add_failure_exception(node)
    elif last_entry.get("setup"):
        status = "Failed"
        add_failure_exception(node)
    else:
        status = "Skipped"

    logger.add_meta("testStatus", status)


def add_test_tags(node):
    tags = extract_tags_from_node(node)

    if len(tags) > 0:
        logger.add_meta("testTags", list(set(tags)))


def extract_tags_from_node(node):
    tags = []
    for marker in node.own_markers:
        if marker.name == "tag" or marker.name == "tags":
            tags += marker.args
        if marker not in known_reserved_markers:
            tags.append(marker.name)
    return tags


def add_test_description(node):
    name = node.name.split("[")[0]
    description = getattr(node.module, name).__doc__
    if description:
        logger.add_meta("testDescription", description.strip())


@pytest.fixture(autouse=True)
def automatic_log_setup(request):
    start_time = datetime.now()
    test_name = method_name_to_human_readable(request.node.name)
    init_test_log(request.node)
    logger.add_meta("testName", test_name)
    logger.info(f"Starting '{test_name}' test execution")
    add_test_description(request.node)
    add_test_tags(request.node)
    yield
    logger.add_meta("testDuration", str(datetime.now() - start_time))
    add_test_status(request.node)
    AutomationAdaptersManager().quit_all()
