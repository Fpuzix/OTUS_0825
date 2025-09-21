
import math
from figure import Figure


class Triangle(Figure):
    def __init__(self, side_a: float, side_b: float, side_c: float):
        if side_a <= 0 or side_b <= 0 or side_c <= 0:
            raise ValueError("Стороны треугольника должны быть > 0")
        if side_a + side_b <= side_c or side_b + side_c <= side_a or side_a + side_c <= side_b:
            raise ValueError("Треугольник с такими сторонами не существует")
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c

    @property
    def perimeter(self) -> float:
        return self.side_a + self.side_b + self.side_c

    @property
    def area(self) -> float:
        p = (self.side_a + self.side_b + self.side_c) / 2
        return math.sqrt(p * (p - self.side_a) * (p - self.side_b) * (p - self.side_c))




#test
#from circle import Circle
#t = Triangle(3,4,5 )
#c = Circle(5)

#print(t.perimeter)
#print(t.area)
#print(t.add_area(c))
