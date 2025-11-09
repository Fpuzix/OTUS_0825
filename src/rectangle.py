from .figure import Figure


class Rectangle(Figure):
    def __init__(self, side_a: float, side_b: float):
        if side_a <= 0 or side_b <= 0:
            raise ValueError("Стороны прямоугольника должны быть > 0")
        self.side_a = side_a
        self.side_b = side_b

    @property
    def perimeter(self) -> float:
        return (self.side_a + self.side_b) * 2

    @property
    def area(self) -> float:
        return self.side_a * self.side_b


# test
# from circle import Circle
# r = Rectangle(3,5)
# c = Circle(2)
# print(r.perimeter)
# print(r.area)
