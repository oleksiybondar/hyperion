import pytest
from hyperiontf.executors.pytest import hyperion_test_case_setup, fixture  # noqa: F401
from ..page_objects.action_builder_page import ActionBuilderPage
from .caps_variants import caps_variants
from hyperiontf import Image
from hyperiontf.typing import VisualMode
import math
import os

dirname = os.path.dirname(__file__)
test_page_path = os.path.join(dirname, "../resources/test_pages/action_builder.html")
page_url = f"file://{test_page_path}"


@fixture(scope="function", log=False)
def page(request):
    caps = request.param
    page = ActionBuilderPage.start_browser(caps)
    page.open(page_url)
    yield page


def calculate_star_points(rect, outer_radius, inner_radius, points=5):
    """Calculate the coordinates for a star."""
    center_x = rect["x"] + rect["width"] / 2
    center_y = rect["y"] + rect["height"] / 2
    star_points = []
    angle = math.pi / points  # 36 degrees between points

    for i in range(2 * points):
        radius = outer_radius if i % 2 == 0 else inner_radius
        theta = i * angle - math.pi / 2  # Start at the top
        x = center_x + radius * math.cos(theta)
        y = center_y + radius * math.sin(theta)
        star_points.append((x, y))

    return star_points


def draw_star(builder, star_points):
    """Draw a star using the provided action builder and star coordinates."""
    # Move to the first point and press mouse down
    builder.mouse_move_to(star_points[0][0], star_points[0][1]).mouse_down("left")

    # Move through the points
    for x, y in star_points[1:]:
        builder.mouse_move_to(x, y)

    # Complete the star by connecting back to the first point
    builder.mouse_move_to(star_points[0][0], star_points[0][1])

    # Release the mouse to finish the drawing
    builder.mouse_up("left").perform()


def draw_multiple_stars(builder, rect, num_stars=5):
    """Draw multiple stars inside each other with slight offset."""
    # Define the outer and inner radii for the largest star
    max_outer_radius = min(rect["width"], rect["height"]) * 0.4
    max_inner_radius = max_outer_radius * 0.5

    # Draw multiple stars, each slightly smaller and offset
    for i in range(num_stars):
        outer_radius = max_outer_radius - i * 10  # Reduce radius for each star
        inner_radius = max_inner_radius - i * 5
        offset_rect = {
            "x": rect["x"] + i * 5,  # Offset x for each star
            "y": rect["y"] + i * 5,  # Offset y for each star
            "width": rect["width"],
            "height": rect["height"],
        }

        star_points = calculate_star_points(offset_rect, outer_radius, inner_radius)
        draw_star(builder, star_points)


@pytest.mark.SingleElement
@pytest.mark.ActionBuilder
@pytest.mark.Visual
@pytest.mark.ElementVisual
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_mouse_down_and_move(page):
    """
    Test drawing multiple stars with slight offset to ensure visual match.
    """
    rect = page.canvas.rect
    builder = page.action_builder
    star_image = Image(os.path.join(dirname, "../resources/images/star.png"))

    # Draw 5 stars with offsets
    draw_multiple_stars(builder, rect, num_stars=5)

    # Assert the visual match for the final drawing
    page.canvas.assert_visual_match(star_image, mode=VisualMode.COMPARE)


@pytest.mark.SingleElement
@pytest.mark.ActionBuilder
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_right_click(page):
    """
    Test drawing multiple stars with slight offset to ensure visual match.
    """

    # Assert the visual match for the final drawing
    page.popup_menu.assert_hidden()

    page.action_builder.right_click_by(400, 100).perform()

    page.popup_menu.assert_visible()


@pytest.mark.MultipleElement
@pytest.mark.ActionBuilder
@pytest.mark.parametrize("page", caps_variants, indirect=True)
def test_drag_and_drop(page):
    """
    Test drawing multiple stars with slight offset to ensure visual match.
    """

    # Assert the visual match for the final drawing
    page.rows[0].assert_text("Row 1: Item A")
    page.rows[1].assert_text("Row 2: Item B")
    page.rows[2].assert_text("Row 3: Item C")

    page.rows[2].drag_and_drop(page.rows[0])

    page.rows.force_refresh()

    page.rows[0].assert_text("Row 3: Item C")
    page.rows[1].assert_text("Row 1: Item A")
    page.rows[2].assert_text("Row 2: Item B")
