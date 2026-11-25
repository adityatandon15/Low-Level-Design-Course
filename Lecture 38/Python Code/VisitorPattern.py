from abc import ABC, abstractmethod


# Visitor Interface
class FileSystemVisitor(ABC):
    @abstractmethod
    def visit(self, file):
        pass


class FileSystemItem(ABC):
    def __init__(self, itemName):
        self.name = itemName

    def getName(self):
        return self.name

    @abstractmethod
    def accept(self, visitor):
        pass


class TextFile(FileSystemItem):
    def __init__(self, fileName, fileContent):
        super().__init__(fileName)
        self.content = fileContent

    def getContent(self):
        return self.content

    def accept(self, visitor):
        visitor.visit(self)


class ImageFile(FileSystemItem):
    def __init__(self, fileName):
        super().__init__(fileName)

    def accept(self, visitor):
        visitor.visit(self)


class VideoFile(FileSystemItem):
    def __init__(self, fileName):
        super().__init__(fileName)

    def accept(self, visitor):
        visitor.visit(self)


# 1. Size calculation visitor
class SizeCalculationVisitor(FileSystemVisitor):
    # Java overloads visit(TextFile), visit(ImageFile), visit(VideoFile).
    def visit(self, file):
        if isinstance(file, TextFile):
            print("Calculating size for TEXT file: " + file.getName())
        elif isinstance(file, ImageFile):
            print("Calculating size for IMAGE file: " + file.getName())
        elif isinstance(file, VideoFile):
            print("Calculating size for VIDEO file: " + file.getName())


# 2. Compression Visitor
class CompressionVisitor(FileSystemVisitor):
    def visit(self, file):
        if isinstance(file, TextFile):
            print("Compressing TEXT file: " + file.getName())
        elif isinstance(file, ImageFile):
            print("Compressing IMAGE file: " + file.getName())
        elif isinstance(file, VideoFile):
            print("Compressing VIDEO file: " + file.getName())


# 3. Virus Scanning Visitor
class VirusScanningVisitor(FileSystemVisitor):
    def visit(self, file):
        if isinstance(file, TextFile):
            print("Scanning TEXT file: " + file.getName())
        elif isinstance(file, ImageFile):
            print("Scanning IMAGE file: " + file.getName())
        elif isinstance(file, VideoFile):
            print("Scanning VIDEO file: " + file.getName())


class VisitorPattern:
    @staticmethod
    def main(args=None):
        img1 = ImageFile("sample.jpg")

        img1.accept(SizeCalculationVisitor())
        img1.accept(CompressionVisitor())
        img1.accept(VirusScanningVisitor())

        vid1 = VideoFile("test.mp4")
        vid1.accept(CompressionVisitor())


if __name__ == "__main__":
    VisitorPattern.main()
