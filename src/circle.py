import math
from .figure import Figure


class Circle(Figure):
    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("Радиус должен быть > 0")
        self.radius = radius

    @property
    def area(self) -> float:
        return math.pi * self.radius**2

    @property
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


# test
# from rectangle import Rectangle
# c = Circle(4)
# r = Rectangle(4, 5)
# print(c.perimeter)
# print(c.area)
# print(c.add_area(r))
