from abc import ABC, abstractmethod


class IImage(ABC):
    @abstractmethod
    def display(self):
        pass


class RealImage(IImage):
    def __init__(self, file):
        self.filename = file
        print("[RealImage] Loading image from disk: " + self.filename)

    def display(self):
        print("[RealImage] Displaying " + self.filename)


class ImageProxy(IImage):
    def __init__(self, file):
        self.filename = file
        self.realImage = None

    def display(self):
        if self.realImage is None:
            self.realImage = RealImage(self.filename)
        self.realImage.display()


class VirtualProxy:
    @staticmethod
    def main(args):
        image1 = ImageProxy("sample.jpg")
        image1.display()


if __name__ == "__main__":
    VirtualProxy.main([])
