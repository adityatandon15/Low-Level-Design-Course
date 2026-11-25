from abc import ABC, abstractmethod


# Base interface for files and folders
class FileSystemItem(ABC):
    @abstractmethod
    def ls(self, indent):
        pass

    @abstractmethod
    def openAll(self, indent):
        pass

    @abstractmethod
    def getSize(self):
        pass

    @abstractmethod
    def cd(self, name):
        pass

    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def isFolder(self):
        pass


# Leaf: File
class File(FileSystemItem):
    def __init__(self, n, s):
        self.name = n
        self.size = s

    def ls(self, indent):
        indentSpaces = " " * indent
        print(indentSpaces + self.name)

    def openAll(self, indent):
        indentSpaces = " " * indent
        print(indentSpaces + self.name)

    def getSize(self):
        return self.size

    def cd(self, name):
        return None

    def getName(self):
        return self.name

    def isFolder(self):
        return False


class Folder(FileSystemItem):
    def __init__(self, n):
        self.name = n
        self.children = []

    def add(self, item):
        self.children.append(item)

    def ls(self, indent):
        indentSpaces = " " * indent
        for child in self.children:
            if child.isFolder():
                print(indentSpaces + "+ " + child.getName())
            else:
                print(indentSpaces + child.getName())

    def openAll(self, indent):
        indentSpaces = " " * indent
        print(indentSpaces + "+ " + self.name)
        for child in self.children:
            child.openAll(indent + 4)

    def getSize(self):
        total = 0
        for child in self.children:
            total += child.getSize()
        return total

    def cd(self, target):
        for child in self.children:
            if child.isFolder() and child.getName() == target:
                return child
        # not found or not a folder
        return None

    def getName(self):
        return self.name

    def isFolder(self):
        return True


class CompositePattern:
    @staticmethod
    def main(args):
        # Build file system
        root = Folder("root")
        root.add(File("file1.txt", 1))
        root.add(File("file2.txt", 1))

        docs = Folder("docs")
        docs.add(File("resume.pdf", 1))
        docs.add(File("notes.txt", 1))
        root.add(docs)

        images = Folder("images")
        images.add(File("photo.jpg", 1))
        root.add(images)

        root.ls(0)

        docs.ls(0)

        root.openAll(0)

        cwd = root.cd("docs")
        if cwd is not None:
            cwd.ls(0)
        else:
            print("\nCould not cd into docs\n")

        print(root.getSize())


if __name__ == "__main__":
    CompositePattern.main([])
