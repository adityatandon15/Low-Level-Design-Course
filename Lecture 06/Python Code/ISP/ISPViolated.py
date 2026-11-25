from abc import ABC, abstractmethod


class UnsupportedOperationException(Exception):
    def getMessage(self):
        return self.args[0] if self.args else None


# Single interface for all shapes (Violates ISP)
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def volume(self):  # 2D shapes don't have volume!
        pass


# Square is a 2D shape but is forced to implement volume()
class Square(Shape):
    def __init__(self, s):
        self._side = float(s)

    def area(self):
        return self._side * self._side

    def volume(self):
        raise UnsupportedOperationException("Volume not applicable for Square")  # Unnecessary method


# Rectangle is also a 2D shape but is forced to implement volume()
class Rectangle(Shape):
    def __init__(self, l, w):
        self._length = float(l)
        self._width = float(w)

    def area(self):
        return self._length * self._width

    def volume(self):
        raise UnsupportedOperationException("Volume not applicable for Rectangle")  # Unnecessary method


# Cube is a 3D shape, so it actually has a volume
class Cube(Shape):
    def __init__(self, s):
        self._side = float(s)

    def area(self):
        return 6 * self._side * self._side

    def volume(self):
        return self._side * self._side * self._side


class ISPViolated:
    @staticmethod
    def main(args):
        square = Square(5)
        rectangle = Rectangle(4, 6)
        cube = Cube(3)

        print("Square Area: " + str(square.area()))
        print("Rectangle Area: " + str(rectangle.area()))
        print("Cube Area: " + str(cube.area()))
        print("Cube Volume: " + str(cube.volume()))

        try:
            print("Square Volume: " + str(square.volume()))  # Will throw an exception
        except UnsupportedOperationException as e:
            print("Exception: " + e.getMessage())


if __name__ == "__main__":
    # call the same demo as Java main
    ISPViolated.main(None)
