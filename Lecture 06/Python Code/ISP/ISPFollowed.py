from abc import ABC, abstractmethod

# Separate interface for 2D shapes
class TwoDimensionalShape(ABC):
    @abstractmethod
    def area(self):
        pass


# Separate interface for 3D shapes
class ThreeDimensionalShape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def volume(self):
        pass


# Square implements only the 2D interface
class Square(TwoDimensionalShape):
    def __init__(self, s):
        self._side = float(s)

    def area(self):
        return self._side * self._side


# Rectangle implements only the 2D interface
class Rectangle(TwoDimensionalShape):
    def __init__(self, l, w):
        self._length = float(l)
        self._width = float(w)

    def area(self):
        return self._length * self._width


# Cube implements the 3D interface
class Cube(ThreeDimensionalShape):
    def __init__(self, s):
        self._side = float(s)

    def area(self):
        return 6 * self._side * self._side

    def volume(self):
        return self._side * self._side * self._side


class ISPFollowed:
    @staticmethod
    def main(args):
        square = Square(5)
        rectangle = Rectangle(4, 6)
        cube = Cube(3)

        print("Square Area: " + str(square.area()))
        print("Rectangle Area: " + str(rectangle.area()))
        print("Cube Area: " + str(cube.area()))
        print("Cube Volume: " + str(cube.volume()))


if __name__ == "__main__":
    # call the same demo as Java main
    ISPFollowed.main(None)
