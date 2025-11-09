import pytest

from src.rectangle import Rectangle
from src.square import Square
from src.triangle import Triangle
from src.circle import Circle


@pytest.mark.parametrize(
    ("radius", "expected_area", "expected_perimeter"),
    [
        (5, 78.53981633974483, 31.41592653589793),
        (5.5, 95.03317777109125, 34.55751918948772),
    ],
    ids=["int value", "float value"],
)
def test_circle(radius, expected_area, expected_perimeter):
    c = Circle(radius)
    assert c.area == expected_area, f"Wrong result for area with {radius} in Circle"
    assert c.perimeter == expected_perimeter, (
        f"Wrong result for perimeter with {radius} in Circle"
    )


@pytest.mark.parametrize(
    ("side_a", "side_b", "expected_area", "expected_perimeter"),
    [(2, 4, 8, 12), (2.5, 3.5, 8.75, 12)],
    ids=["int value", "float value"],
)
def test_rectangle(side_a, side_b, expected_area, expected_perimeter):
    r = Rectangle(side_a, side_b)
    assert r.area == expected_area, (
        f"Wrong result for area with {side_a}, {side_b} in Rectangle"
    )
    assert r.perimeter == expected_perimeter, (
        f"Wrong result for perimeter with {side_a}, {side_b} in Rectangle"
    )


def test_triangle(triangle_case):
    a, b, c, expected_per, expected_area = triangle_case
    t = Triangle(a, b, c)
    assert t.perimeter == expected_per
    assert t.area == expected_area


@pytest.mark.parametrize(
    ("side_a", "expected_area", "expected_perimeter"),
    [(2, 4, 8), (2.5, 6.25, 10)],
    ids=["int value", "float value"],
)
def test_square(side_a, expected_area, expected_perimeter):
    s = Square(side_a)
    assert isinstance(s, Rectangle)
    assert s.area == expected_area, f"Wrong result for area with {side_a} in Square"
    assert s.perimeter == expected_perimeter, (
        f"Wrong result for perimetr with {side_a} in Square"
    )


@pytest.mark.parametrize(
    ("side_a", "side_b", "radius", "expected_area_sum"),
    [(2, 4, 5, 86.53981633974483), (2.5, 2.7, 6.25, 129.4684630308513)],
    ids=["int value", "float value"],
)
def test_add_area_sum_and_type(side_a, side_b, radius, expected_area_sum):
    r = Rectangle(side_a, side_b)
    c = Circle(radius)
    assert c.add_area(r) == expected_area_sum, (
        f"Wrong sum area for Circle and Rectangle"
    )


@pytest.mark.parametrize(
    ("side_a", "side_b", "radius"),
    [(2, 4, 5), (2.5, 2.7, 6.25)],
    ids=["int value", "float value"],
)
def test_add_area_sum_and_type_error(side_a, side_b, radius):
    r = Rectangle(side_a, side_b)
    c = Circle(radius)
    with pytest.raises(TypeError):
        r.add_area("not a figure")
