import pytest
from hyperiontf.ui.color import Color


@pytest.mark.color
def test_clamping():
    assert Color(300, 300, 300) == Color(255, 255, 255)
    assert Color(-20, -20, -20) == Color(0, 0, 0)
    assert Color(150, 200, 250, 1.2) == Color(150, 200, 250, 1.0)
    assert Color(150, 200, 250, -0.2) == Color(150, 200, 250, 0.0)


@pytest.mark.color
def test_from_string():
    assert Color.from_string("rgb(255,255,255)") == Color(255, 255, 255)
    assert Color.from_string("rgba(255,255,255,0.5)") == Color(255, 255, 255, 0.5)
    assert Color.from_string("#FFF") == Color(255, 255, 255)
    assert Color.from_string("#FFFFFF") == Color(255, 255, 255)

    with pytest.raises(ValueError):
        Color.from_string("invalid_string")


@pytest.mark.color
def test_grayscale():
    assert Color(255, 0, 0).grayscale() == pytest.approx(0.299 * 255)
    assert Color(0, 255, 0).grayscale() == pytest.approx(0.587 * 255)
    assert Color(0, 0, 255).grayscale() == pytest.approx(0.114 * 255)


@pytest.mark.color
def test_approx_eq():
    col1 = Color(255, 0, 0)
    col2 = Color(250, 10, 0)
    assert col1.approx_eq(
        col2
    )  # should be approximately equal based on default thresholds
    assert not col1.approx_eq(
        col2, 1
    )  # should not be approximately equal with stricter threshold


@pytest.mark.color
def test_equality():
    assert Color(255, 0, 0) == Color(255, 0, 0)
    assert Color(255, 0, 0) != Color(254, 0, 0)


@pytest.mark.color
def test_ordering():
    assert Color(255, 0, 0) < Color(0, 255, 0)
    assert Color(0, 0, 255) <= Color(255, 0, 0)
    assert Color(0, 255, 0) > Color(255, 0, 0)
    assert Color(255, 0, 0) >= Color(0, 0, 255)


@pytest.mark.color
def test_math_operations_1():
    col1 = Color(255, 0, 0)
    col2 = Color(0, 255, 0)

    assert col1 + col2 == Color(255, 255, 0)
    assert col1 - col2 == Color(255, 0, 0, 0)

    col1 += col2
    assert col1 == Color(255, 255, 0)

    col1 -= col2
    assert col1 == Color(255, 0, 0, 0)


@pytest.mark.color
def test_math_operations_2():
    col1 = Color(255, 0, 0)
    col2 = Color(0, 255, 0)
    assert col1 * col2 == Color(0, 0, 0, 0)
    assert col1 * 0.5 == Color(127, 0, 0, 0)

    col1 *= col2
    assert col1 == Color(0, 0, 0, 0)

    col1 *= 2
    assert col1 == Color(0, 0, 0, 0)


@pytest.mark.color
def test_string_representation():
    assert str(Color(255, 255, 255)) == "rgba(255, 255, 255 ,1.00)"
    assert str(Color(150, 150, 150, 0.5)) == "rgba(150, 150, 150 ,0.50)"
