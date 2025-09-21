from abc import ABC, abstractmethod

class Figure(ABC):

    @property
    @abstractmethod
    def area(self) -> float:
        pass

    @property
    @abstractmethod
    def perimeter(self) -> float:
        pass

    def add_area(self, figure) -> float:
        if not isinstance(figure, Figure):
            raise TypeError("Нужно чтобы значение было класса Figure")
        return self.area + figure.area
