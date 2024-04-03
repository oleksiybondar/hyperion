import pytest
from hyperiontf.executors.pytest import automatic_log_setup, fixture  # noqa: F401
from .caps_variants import caps_variants
from ..page_objects.visual import VisualPage
from hyperiontf import expect, Image
from hyperiontf.typing import VisualMode
import os

dirname = os.path.dirname(__file__)
test_page_path = os.path.join(dirname, "../resources/test_pages/visual_testing.html")
page_url = f"file://{test_page_path}"

base_image_path = os.path.join(dirname, "../resources/images")
full_page_img = os.path.abspath(os.path.join(base_image_path, "full_page.png"))
dice_img = os.path.abspath(os.path.join(base_image_path, "dice.png"))
collect_page_img = os.path.abspath(os.path.join(base_image_path, "collected_page.png"))
collect_dice_img = os.path.abspath(os.path.join(base_image_path, "collected_dice.png"))


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = VisualPage.start_browser(caps)
    page.open(page_url)
    yield page


@pytest.mark.visual
@pytest.mark.collect_code
@pytest.mark.page
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_collect_mode_for_whole_page(page):
    """
    Tests the collect mode for visual verification of the whole page.

    In this mode, the test ensures that the expected visual representation of the entire page
    is collected for future comparisons. This test first verifies that the expected image does not
    exist, performs visual match collection, and then confirms the image's existence post-operation.

    Parameters:
    - page: An instance of VisualPage provided by the `page` fixture.
    """
    page_img = Image(collect_page_img)
    expect(page_img).not_to_exist()
    page.verify_visual_match(page_img, mode=VisualMode.COLLECT)
    expect(page_img).to_exist()
    page_img.remove()
    expect(page_img).not_to_exist()


@pytest.mark.visual
@pytest.mark.collect_code
@pytest.mark.element
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_collect_mode_for_element_only(page):
    """
    Tests the collect mode specifically for an individual page element.

    This test verifies the functionality of collecting visual verification data for a specific
    element on the page, not the whole page. It ensures that the image representing the element does not
    exist before the collection, performs the collection, and then checks that the image exists after
    the collection process. Finally, it cleans up by removing the collected image.

    Parameters:
    - page: An instance of VisualPage provided by the `page` fixture, which includes the specific element to test.
    """
    dice = Image(collect_dice_img)
    expect(dice).not_to_exist()
    page.dice.verify_visual_match(dice, mode=VisualMode.COLLECT)
    expect(dice).to_exist()
    dice.remove()
    expect(dice).not_to_exist()


@pytest.mark.visual
@pytest.mark.compare_code
@pytest.mark.threshold
@pytest.mark.page
@pytest.mark.change_viewport
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_compare_mode_for_whole_page(page):
    """
    Tests visual comparison for the whole page in a specific viewport size with a defined mismatch threshold.

    This test sets the viewport to medium size, performs a visual comparison of the current page against a baseline image,
    and expects a specific result based on the mismatch threshold. It asserts the outcome of the visual comparison,
    indicating whether the current page's visual representation matches the expected baseline within the allowed threshold.

    Parameters:
    - page: An instance of VisualPage provided by the `page` fixture.
    """
    page.viewport = "md"
    result = page.verify_visual_match(
        full_page_img, mode=VisualMode.COMPARE, mismatch_threshold=1
    )
    assert result == 1, f"Expected True, but got {result.result}"  # type: ignore


@pytest.mark.visual
@pytest.mark.compare_code
@pytest.mark.threshold
@pytest.mark.page
@pytest.mark.change_viewport
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_compare_mode_for_whole_page_with_interferences(page):
    """
    Tests the compare mode for the whole page while simulating visual interferences on the page.

    This test involves adjusting the viewport, toggling a control panel option to introduce visual
    interferences, and then performing a visual comparison against a baseline image. It verifies that
    the comparison accounts for the specified mismatch threshold and that interferences affect the
    outcome as expected. The result of the visual comparison should align with the anticipated test conditions.

    Parameters:
    - page: An instance of VisualPage provided by the `page` fixture, with methods to manipulate and test visual interferences.
    """
    page.viewport = "md"
    page.control_panel.toggle_interference.click()
    result = page.verify_visual_match(
        full_page_img, mode=VisualMode.COMPARE, mismatch_threshold=1
    )
    assert result == 0, f"Expected False, but got {result.result}"  # type: ignore


@pytest.mark.visual
@pytest.mark.compare_code
@pytest.mark.threshold
@pytest.mark.page
@pytest.mark.change_viewport
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_compare_mode_for_element(page):
    """
    Tests the compare mode for a specific element on the page, considering changes in the page layout and element attributes.

    This test sets the viewport size and manipulates the page layout by resizing and splitting elements
    before conducting a visual comparison of both the whole page and a specific element against their
    respective baseline images. It assesses the impact of these manipulations on the visual comparison
    outcome, expecting specific results based on a defined mismatch threshold.

    Parameters:
    - page: An instance of VisualPage provided by the `page` fixture, capable of element manipulation and visual comparison.
    """
    page.viewport = "md"

    page.control_panel.resize_blue.click()
    page.control_panel.split_purple.click()

    result = page.verify_visual_match(
        full_page_img, mode=VisualMode.COMPARE, mismatch_threshold=1
    )
    assert result == 0, f"Expected False, but got {result.result}"  # type: ignore

    result = page.dice.verify_visual_match(
        dice_img, mode=VisualMode.COMPARE, mismatch_threshold=1
    )
    assert result == 1, f"Expected True, but got {result.result}"  # type: ignore
