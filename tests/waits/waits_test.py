import pytest
from hyperiontf.executors.pytest import automatic_log_setup, fixture  # noqa: F401
from hyperiontf import expect
from hyperiontf.typing import TimeoutException

from page_objects.waits import WaitsPage

from web.caps_variants import caps_variants
import os
import time

# The paths to the test pages
waits_test_page = os.path.join(
    os.path.dirname(__file__), "../resources/test_pages/waits.html"
)

# The URLs of the test pages
page_url = f"file://{waits_test_page}"


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = WaitsPage.start_browser(caps)
    page.open(page_url)
    yield page


@pytest.mark.Wait
@pytest.mark.SingleElement
@pytest.mark.WaitUntilFound
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_element_found(page):
    """
    Test the ability to wait until a specific element is found on the page.

    Scenario:
    - Verify that the target element is not present on the page initially.
    - Trigger an action that is expected to add the target element to the page (e.g., clicking a button).
    - Wait until the target element becomes present on the page.
    - Assert that the target element is indeed present after the action.

    This test verifies the functionality of dynamically adding elements to the page and ensuring that
    the test framework can properly wait for these elements to appear as part of its assertions.
    """
    expect(page.new_element.is_present).to_be(False)
    page.control_panel.add_element_button.click()
    page.new_element.wait_until_found()
    expect(page.new_element.is_present).to_be(True)


@pytest.mark.Wait
@pytest.mark.SingleElement
@pytest.mark.WaitUntilFound
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_element_found_failure(page):
    """
    Test the handling of a timeout when waiting for an element that does not appear on the page.

    Scenario:
    - Verify that the target element is not present on the page initially.
    - Without triggering any action that could add the target element to the page, attempt to wait for the element to become present.
    - Expect a TimeoutException to be raised, indicating that the element did not appear within the specified wait period.

    This test verifies the framework's ability to correctly handle cases where an element is expected to appear but does not, ensuring that appropriate exceptions are thrown to signal a test failure due to unmet conditions.
    """
    expect(page.new_element.is_present).to_be(False)
    with pytest.raises(TimeoutException):
        page.new_element.wait_until_found()


@pytest.mark.Wait
@pytest.mark.SingleElement
@pytest.mark.WaitUntilEnabled
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_element_enabled(page):
    """
    Test the ability to wait until a specific element is enabled on the page.

    Scenario:
    - Verify that the target element is disabled on the page initially.
    - Trigger an action that is expected to enable the target element (e.g., clicking a state change button).
    - Wait until the target element becomes enabled.
    - Assert that the target element is indeed enabled after the action.

    This test verifies the functionality of dynamically changing the state of elements on the page and ensuring that
    the test framework can properly wait for these elements to become enabled as part of its assertions.
    """
    expect(page.disabled_button.is_enabled).to_be(False)
    page.control_panel.state_button.click()
    page.disabled_button.wait_until_enabled()
    expect(page.disabled_button.is_enabled).to_be(True)


@pytest.mark.Wait
@pytest.mark.SingleElement
@pytest.mark.WaitUntilEnabled
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_enabled_failure(page):
    """
    Test the handling of a timeout when waiting for an element to become enabled, but it does not within the specified time.

    Scenario:
    - Verify that the target element is disabled on the page initially.
    - Without triggering any action that could enable the target element, attempt to wait for the element to become enabled.
    - Expect a TimeoutException to be raised, indicating that the element did not become enabled within the specified wait period.

    This test verifies the framework's ability to correctly handle cases where an element's enabled state is expected to change but does not, ensuring that appropriate exceptions are thrown to signal a test failure due to unmet conditions.
    """
    expect(page.disabled_button.is_enabled).to_be(False)
    with pytest.raises(TimeoutException):
        page.disabled_button.wait_until_enabled()


@pytest.mark.Wait
@pytest.mark.SingleElement
@pytest.mark.WaitUntilVisible
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_element_visible(page):
    """
    Test the ability to wait until a specific element becomes visible on the page.

    Scenario:
    - Verify that the target element is not visible on the page initially.
    - Trigger an action that is expected to make the target element visible (e.g., clicking a visibility toggle button).
    - Wait until the target element becomes visible.
    - Assert that the target element is indeed visible after the action.

    This test verifies the functionality of dynamically changing the visibility of elements on the page and ensuring that the test framework can properly wait for these elements to become visible as part of its assertions.
    """
    expect(page.invisible_element.is_visible).to_be(False)
    page.control_panel.visibility_button.click()
    page.invisible_element.wait_until_visible()
    expect(page.invisible_element.is_visible).to_be(True)


@pytest.mark.Wait
@pytest.mark.SingleElement
@pytest.mark.WaitUntilVisible
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_visible_failure(page):
    """
    Test the handling of a timeout when waiting for an element to become visible, but it does not within the specified time.

    Scenario:
    - Verify that the target element is not visible on the page initially.
    - Without triggering any action that could make the target element visible, attempt to wait for the element to become visible.
    - Expect a TimeoutException to be raised, indicating that the element did not become visible within the specified wait period.

    This test verifies the framework's ability to correctly handle cases where an element's visibility is expected to change but does not, ensuring that appropriate exceptions are thrown to signal a test failure due to unmet conditions.
    """
    expect(page.invisible_element.is_visible).to_be(False)
    with pytest.raises(TimeoutException):
        page.invisible_element.wait_until_visible()


@pytest.mark.Wait
@pytest.mark.SingleElement
@pytest.mark.WaitUntilMissing
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_element_missing(page):
    """
    Test the ability to wait until a specific element is no longer present on the page.

    Scenario:
    - Verify that the target element is present on the page initially.
    - Trigger an action that is expected to remove the target element from the page (e.g., clicking a remove element button).
    - Wait until the target element is no longer present.
    - Assert that the target element is indeed not present after the action.

    This test verifies the functionality of dynamically removing elements from the page and ensuring that the test framework can properly wait for these elements to disappear as part of its assertions.
    """
    expect(page.present_element.is_present).to_be(True)
    page.control_panel.remove_element_button.click()
    # increased timeout because when elements is gone it takes time to find it with retries
    page.present_element.wait_until_missing(timeout=10)
    expect(page.present_element.is_present).to_be(False)


@pytest.mark.Wait
@pytest.mark.SingleElement
@pytest.mark.WaitUntilMissing
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_missing_failure(page):
    """
    Test the handling of a timeout when waiting for an element to no longer be present on the page, but it remains present within the specified time.

    Scenario:
    - Verify that the target element is present on the page initially.
    - Without triggering any action that could remove the target element, attempt to wait for the element to no longer be present.
    - Expect a TimeoutException to be raised, indicating that the element remained present beyond the specified wait period.

    This test verifies the framework's ability to correctly handle cases where an element is expected to disappear but does not, ensuring that appropriate exceptions are thrown to signal a test failure due to unmet conditions.
    """
    expect(page.present_element.is_present).to_be(True)
    with pytest.raises(TimeoutException):
        page.invisible_element.wait_until_missing()


@pytest.mark.Wait
@pytest.mark.SingleElement
@pytest.mark.WaitUntilHidden
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_element_hidden(page):
    """
    Test the ability to wait until a specific element becomes hidden on the page.

    Scenario:
    - Trigger an action that makes the target element visible on the page (e.g., clicking a visibility toggle button).
    - Verify that the target element is indeed visible after the action.
    - Trigger another action expected to hide the target element (e.g., clicking the visibility toggle button again).
    - Wait until the target element becomes hidden.
    - Assert that the target element is no longer visible on the page.

    This test verifies the functionality of dynamically changing the visibility of elements on the page and ensuring that the test framework can properly wait for these elements to become hidden as part of its assertions.
    """
    page.control_panel.visibility_button.click()
    time.sleep(
        4
    )  # and action is delayed for 3 seconds, sleeping 4 seconds to make sure action completed
    expect(page.invisible_element.is_visible).to_be(True)
    page.control_panel.visibility_button.click()
    page.invisible_element.wait_until_hidden()
    expect(page.invisible_element.is_visible).to_be(False)


@pytest.mark.Wait
@pytest.mark.SingleElement
@pytest.mark.WaitUntilHidden
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_hidden_failure(page):
    """
    Test the handling of a timeout when waiting for an element to become hidden, but it remains visible within the specified time.

    Scenario:
    - Trigger an action that makes the target element visible on the page.
    - Verify that the target element is indeed visible after the action.
    - Attempt to wait for the element to become hidden without triggering any action that would actually hide it.
    - Expect a TimeoutException to be raised, indicating that the element did not become hidden within the specified wait period.

    This test verifies the framework's ability to correctly handle cases where an element's visibility is expected to change to hidden but does not, ensuring that appropriate exceptions are thrown to signal a test failure due to unmet conditions.
    """
    page.control_panel.visibility_button.click()
    time.sleep(
        4
    )  # and action is delayed for 3 seconds, sleeping 4 seconds to make sure action completed
    expect(page.invisible_element.is_visible).to_be(True)
    with pytest.raises(TimeoutException):
        page.invisible_element.wait_until_hidden()


@pytest.mark.Wait
@pytest.mark.SingleElement
@pytest.mark.WaitUntilAnimationCompleted
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_animation_completed(page):
    """
    Test the ability to wait until the animation of a specific element is completed on the page.

    Scenario:
    - Verify that the target animated element is not present on the page initially.
    - Trigger an action that starts an animation on the target element (e.g., clicking an animation start button).
    - Wait for the animation to complete, considering that the animation duration exceeds the default wait timeout, thus specifying a longer timeout.
    - Assert that the target animated element is present on the page after the animation has completed.

    This test verifies the functionality of waiting for an element's animation to finish, particularly when the animation duration is longer than the default wait timeout, ensuring that the test framework can properly handle extended wait times for animations.
    """
    expect(page.animated_element.is_present).to_be(False)
    page.control_panel.animation_button.click()
    # animation take place 5 seconds + so default 5 seconds timeout will not work
    page.animated_element.wait_until_animation_completed(timeout=10)
    expect(page.animated_element.is_present).to_be(True)


@pytest.mark.Wait
@pytest.mark.WaitUntilFound
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_found_for_arrays(page):
    """
    Test the ability to wait until an array of elements becomes present on the page.

    Scenario:
    - Trigger an action that removes an array of elements from the page.
    - Wait for a specific amount of time to ensure the action has completed.
    - Verify that the array of elements is not present on the page.
    - Trigger another action to add the array of elements back to the page.
    - Wait until the array of elements becomes present again.
    - Assert that the array of elements is indeed present after the action.

    This test verifies the functionality of dynamically handling arrays of elements, ensuring that the test framework can properly wait for these elements to appear as part of its assertions.
    """
    page.control_panel.remove_array_elements_button.click()
    time.sleep(
        4
    )  # and action is delayed for 3 seconds, sleeping 4 seconds to make sure action completed
    expect(page.elements_array.is_present).to_be(False)
    page.control_panel.add_array_element_button.click()
    page.elements_array.wait_until_found()
    expect(page.elements_array.is_present).to_be(True)


@pytest.mark.Wait
@pytest.mark.WaitUntilFound
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_found_failure_for_arrays(page):
    """
    Test the handling of a timeout when waiting for an array of elements to become present, but they do not within the specified time.

    Scenario:
    - Trigger an action that removes an array of elements from the page.
    - Wait for a specific amount of time to ensure the action has completed.
    - Verify that the array of elements is not present on the page.
    - Attempt to wait for the array of elements to become present without triggering any action that would add them back.
    - Expect a TimeoutException to be raised, indicating that the array of elements did not become present within the specified wait period.

    This test verifies the framework's ability to correctly handle cases where an array of elements is expected to appear but does not, ensuring that appropriate exceptions are thrown to signal a test failure due to unmet conditions.
    """
    page.control_panel.remove_array_elements_button.click()
    time.sleep(
        4
    )  # and action is delayed for 3 seconds, sleeping 4 seconds to make sure action completed
    expect(page.elements_array.is_present).to_be(False)
    with pytest.raises(TimeoutException):
        page.elements_array.wait_until_found()


@pytest.mark.Wait
@pytest.mark.WaitUntilMissing
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_missing_for_arrays(page):
    """
    Test the ability to wait until an array of elements is no longer present on the page.

    Scenario:
    - Verify that an array of elements is present on the page initially.
    - Trigger an action that removes the array of elements from the page.
    - Wait until the array of elements is no longer present.
    - Assert that the array of elements is indeed not present after the action.

    This test verifies the functionality of dynamically removing arrays of elements from the page and ensuring that the test framework can properly wait for these elements to disappear as part of its assertions.
    """
    expect(page.elements_array.is_present).to_be(True)
    page.control_panel.remove_array_elements_button.click()
    page.elements_array.wait_until_missing()
    expect(page.elements_array.is_present).to_be(False)


@pytest.mark.Wait
@pytest.mark.WaitUntilMissing
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_missing_failure_for_arrays(page):
    """
    Test the handling of a timeout when waiting for an array of elements to no longer be present on the page, but they remain present within the specified time.

    Scenario:
    - Verify that an array of elements is present on the page initially.
    - Attempt to wait for the array of elements to no longer be present without triggering any action that would remove them.
    - Expect a TimeoutException to be raised, indicating that the array of elements remained present beyond the specified wait period.

    This test verifies the framework's ability to correctly handle cases where an array of elements is expected to disappear but does not, ensuring that appropriate exceptions are thrown to signal a test failure due to unmet conditions.
    """
    expect(page.elements_array.is_present).to_be(True)
    with pytest.raises(TimeoutException):
        page.elements_array.wait_until_missing()


@pytest.mark.Wait
@pytest.mark.WaitItemsCount
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_items_count(page):
    """
    Test the ability to wait until the items count in an array reaches a specified number on the page.

    Scenario:
    - Verify that the initial count of elements in the array is 2.
    - Trigger an action twice that adds an element to the array, with a brief wait between actions to ensure they are processed separately.
    - Wait until the count of elements in the array reaches 4, specifying a longer timeout to accommodate the addition process.
    - Assert that the count of elements in the array is indeed 4 after the actions.

    This test verifies the functionality of dynamically adding elements to an array on the page and ensuring that the test framework can properly wait for the count of these elements to reach a specified number as part of its assertions.
    """
    expect(len(page.elements_array)).to_be(2)
    page.control_panel.add_array_element_button.click()
    time.sleep(1.5)
    page.control_panel.add_array_element_button.click()
    page.elements_array.wait_until_items_count(4, timeout=10)
    expect(len(page.elements_array)).to_be(4)


@pytest.mark.Wait
@pytest.mark.WaitItemsCount
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_items_count_failure(page):
    """
    Test the handling of a timeout when waiting for the items count in an array to reach a specified number, but it does not within the default timeout.

    Scenario:
    - Verify that the initial count of elements in the array is 2.
    - Attempt to wait for the count of elements in the array to reach 4 without triggering any action that would actually add elements to the array.
    - Expect a TimeoutException to be raised, indicating that the count of elements did not reach the specified number within the default timeout period.

    This test verifies the framework's ability to correctly handle cases where the count of elements in an array is expected to reach a specified number but does not, ensuring that appropriate exceptions are thrown to signal a test failure due to unmet conditions.
    """
    expect(len(page.elements_array)).to_be(2)
    with pytest.raises(TimeoutException):
        page.elements_array.wait_until_items_count(4)


@pytest.mark.Wait
@pytest.mark.WaitUntilItemsDecrease
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_items_decreases_count(page):
    """
    Test the ability to wait until the count of items in an array decreases on the page.

    Scenario:
    - Verify that the initial count of elements in the array is 2.
    - Trigger an action that removes an element from the array.
    - Wait until the count of elements in the array decreases.
    - Assert that the count of elements in the array is 1 after the removal action.

    This test verifies the functionality of dynamically removing elements from an array on the page and ensuring that the test framework can properly wait for the count of these elements to decrease as part of its assertions.
    """
    expect(len(page.elements_array)).to_be(2)
    page.control_panel.remove_array_element_button.click()
    page.elements_array.wait_until_items_decrease()
    expect(len(page.elements_array)).to_be(1)


@pytest.mark.Wait
@pytest.mark.WaitUntilItemsDecrease
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_items_decrease_failure_on_increase(page):
    """
    Test the handling of a situation where waiting for the items count in an array to decrease fails because the count actually increases.

    Scenario:
    - Verify that the initial count of elements in the array is 2.
    - Trigger an action that adds an element to the array, thus increasing the count.
    - Attempt to wait for the count of elements in the array to decrease.
    - Expect a TimeoutException to be raised, indicating a failure as the count did not decrease but instead increased.

    This test verifies the framework's ability to detect and correctly handle cases where an expected decrease in the count of elements does not occur, ensuring that appropriate exceptions are thrown to signal a test failure.
    """
    expect(len(page.elements_array)).to_be(2)
    page.control_panel.add_array_element_button.click()
    with pytest.raises(TimeoutException):
        page.elements_array.wait_until_items_decrease()


@pytest.mark.Wait
@pytest.mark.WaitUntilItemsDecrease
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_items_decrease_failure(page):
    """
    Test the handling of a timeout when waiting for the items count in an array to decrease, but no change occurs within the specified timeout.

    Scenario:
    - Verify that the initial count of elements in the array is 2.
    - Without triggering any action that could potentially decrease the count of elements in the array, attempt to wait for the count to decrease.
    - Expect a TimeoutException to be raised, indicating that the count of elements did not decrease within the specified wait period.

    This test assesses the framework's capability to handle cases where an expected decrease in the count of elements in an array does not happen, ensuring that appropriate exceptions are thrown to indicate a test failure due to unmet conditions.
    """
    expect(len(page.elements_array)).to_be(2)
    with pytest.raises(TimeoutException):
        page.elements_array.wait_until_items_decrease()


@pytest.mark.Wait
@pytest.mark.WaitUntilItemsIncrease
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_items_increase(page):
    """
    Test the ability to wait until the count of items in an array increases on the page.

    Scenario:
    - Verify the initial count of elements in the array is 2.
    - Trigger an action that adds an element to the array.
    - Wait until the count of elements in the array increases.
    - Assert that the count of elements in the array is 3 after the addition action.

    This test verifies the functionality of dynamically adding elements to an array on the page and ensuring that the test framework can properly wait for the count of these elements to increase as part of its assertions.
    """
    expect(len(page.elements_array)).to_be(2)
    page.control_panel.add_array_element_button.click()
    page.elements_array.wait_until_items_increase()
    expect(len(page.elements_array)).to_be(3)


@pytest.mark.Wait
@pytest.mark.WaitUntilItemsIncrease
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_items_increase_failure_on_decrease(page):
    """
    Test the handling of a situation where waiting for the items count in an array to increase fails because the count actually decreases.

    Scenario:
    - Verify the initial count of elements in the array is 2.
    - Trigger an action that removes an element from the array, thus decreasing the count.
    - Attempt to wait for the count of elements in the array to increase.
    - Expect a TimeoutException to be raised, indicating a failure as the count did not increase but instead decreased.

    This test verifies the framework's ability to detect and correctly handle cases where an expected increase in the count of elements does not occur, ensuring that appropriate exceptions are thrown to signal a test failure.
    """
    expect(len(page.elements_array)).to_be(2)
    page.control_panel.remove_array_element_button.click()
    with pytest.raises(TimeoutException):
        page.elements_array.wait_until_items_increase()


@pytest.mark.Wait
@pytest.mark.WaitUntilItemsIncrease
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_items_increase_failure_without_action(page):
    """
    Test the handling of a timeout when waiting for the items count in an array to increase, but no change occurs within the specified timeout.

    Scenario:
    - Verify the initial count of elements in the array is 2.
    - Without triggering any action that could potentially increase the count of elements in the array, attempt to wait for the count to increase.
    - Expect a TimeoutException to be raised, indicating that the count of elements did not increase within the specified wait period.

    This test assesses the framework's capability to handle cases where an expected increase in the count of elements in an array does not happen, ensuring that appropriate exceptions are thrown to indicate a test failure due to unmet conditions.
    """
    expect(len(page.elements_array)).to_be(2)
    with pytest.raises(TimeoutException):
        page.elements_array.wait_until_items_increase()


@pytest.mark.Wait
@pytest.mark.WaitUntilItemsChange
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_items_change_on_decrease(page):
    """
    Test the ability to wait until the count of items in an array decreases on the page.

    Scenario:
    - Verify the initial count of elements in the array is 2.
    - Trigger an action that removes an element from the array.
    - Wait until the count of elements in the array changes.
    - Assert that the count of elements in the array is 1 after the removal action.

    This test verifies the functionality of dynamically removing elements from an array on the page and ensuring that the test framework can properly wait for any change in the count of these elements as part of its assertions.
    """
    expect(len(page.elements_array)).to_be(2)
    page.control_panel.remove_array_element_button.click()
    page.elements_array.wait_until_items_change()
    expect(len(page.elements_array)).to_be(1)


@pytest.mark.Wait
@pytest.mark.WaitUntilItemsChange
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_items_change_on_increase(page):
    """
    Test the ability to wait until the count of items in an array increases on the page.

    Scenario:
    - Verify the initial count of elements in the array is 2.
    - Trigger an action that adds an element to the array.
    - Wait until the count of elements in the array changes.
    - Assert that the count of elements in the array is 3 after the addition action.

    This test ensures the test framework can effectively wait for any change in the count of elements within an array, be it an increase or decrease, demonstrating the framework's flexibility in handling dynamic changes in the page's element count.
    """
    expect(len(page.elements_array)).to_be(2)
    page.control_panel.add_array_element_button.click()
    page.elements_array.wait_until_items_change()
    expect(len(page.elements_array)).to_be(3)


@pytest.mark.Wait
@pytest.mark.WaitUntilItemsChange
@pytest.mark.MultipleElement
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_wait_until_items_change_failure_without_action(page):
    """
    Test the handling of a timeout when waiting for the count of items in an array to change, but no change occurs within the specified timeout.

    Scenario:
    - Verify the initial count of elements in the array is 2.
    - Without triggering any action that could potentially change the count of elements in the array, attempt to wait for the count to change.
    - Expect a TimeoutException to be raised, indicating that the count of elements did not change within the specified wait period.

    This test assesses the framework's ability to handle cases where an expected change in the count of elements in an array does not occur, ensuring that appropriate exceptions are thrown to signal a test failure due to unmet conditions.
    """
    expect(len(page.elements_array)).to_be(2)
    with pytest.raises(TimeoutException):
        page.elements_array.wait_until_items_change()
