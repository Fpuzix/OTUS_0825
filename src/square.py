
from rectangle import Rectangle



class Square(Rectangle):
    def __init__(self, side_a: float):
        super().__init__(side_a, side_a)




#test
#from circle import Circle
#s = Square(2)
#c = Circle(3)
#print(s.perimeter)
#print(s.area)
#print(s.add_area(c))
