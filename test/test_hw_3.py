import math
import pytest

from src.rectangle import Rectangle
from src.square import Square
from src.triangle import Triangle
from src.circle import Circle


def test_circle():
    c = Circle(9)
    assert c.area == 254.46900494077323
    assert c.perimeter == 56.548667764616276


def test_rectangle():
    r = Rectangle(3, 5)
    assert r.area == 15
    assert r.perimeter == 16


def test_triangle(triangle_case):
    a, b, c, expected_per, expected_area = triangle_case
    t = Triangle(a, b, c)
    assert t.perimeter == expected_per
    assert t.area == expected_area


def test_square():
    s = Square(4)
    assert isinstance(s, Rectangle)
    assert s.area == 16
    assert s.perimeter == 16


def test_add_area_sum_and_type_error():
    # from src.circle import Circle
    r = Rectangle(1, 2)
    c = Circle(1)
    assert c.add_area(r) == pytest.approx(math.pi + 2)
    with pytest.raises(TypeError):
        c.add_area("not a figure")
