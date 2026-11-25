from abc import ABC, abstractmethod

# Interface for document elements
class DocumentElement(ABC):
    @abstractmethod
    def render(self):
        pass


# Concrete implementation for text elements
class TextElement(DocumentElement):
    def __init__(self, text):
        self._text = text

    def render(self):
        return self._text


# Concrete implementation for image elements
class ImageElement(DocumentElement):
    def __init__(self, imagePath):
        self._imagePath = imagePath

    def render(self):
        return "[Image: " + self._imagePath + "]"


# NewLineElement represents a line break in the document.
class NewLineElement(DocumentElement):
    def render(self):
        return "\n"


# TabSpaceElement represents a tab space in the document.
class TabSpaceElement(DocumentElement):
    def render(self):
        return "\t"


# Document class responsible for holding a collection of elements
class Document:
    def __init__(self):
        self._documentElements = []

    def addElement(self, element):
        self._documentElements.append(element)

    # Renders the document by concatenating the render output of all elements.
    def render(self):
        result = ""
        for element in self._documentElements:
            result += element.render()
        return result


# Persistence Interface
class Persistence(ABC):
    @abstractmethod
    def save(self, data):
        pass


# FileStorage implementation of Persistence
class FileStorage(Persistence):
    def save(self, data):
        try:
            outFile = open("document.txt", "w")
            outFile.write(data)
            outFile.close()
            print("Document saved to document.txt")
        except OSError:
            print("Error: Unable to open file for writing.")


# Placeholder DBStorage implementation
class DBStorage(Persistence):
    def save(self, data):
        # Save to DB
        pass


# DocumentEditor class managing client interactions
class DocumentEditor:
    def __init__(self, document, storage):
        self._document = document
        self._storage = storage
        self._renderedDocument = ""

    def addText(self, text):
        self._document.addElement(TextElement(text))

    def addImage(self, imagePath):
        self._document.addElement(ImageElement(imagePath))

    # Adds a new line to the document.
    def addNewLine(self):
        self._document.addElement(NewLineElement())

    # Adds a tab space to the document.
    def addTabSpace(self):
        self._document.addElement(TabSpaceElement())

    def renderDocument(self):
        if self._renderedDocument == "":
            self._renderedDocument = self._document.render()
        return self._renderedDocument

    def saveDocument(self):
        self._storage.save(self.renderDocument())


# Client usage example
class DocumentEditorClient:
    @staticmethod
    def main(args):
        document = Document()
        persistence = FileStorage()

        editor = DocumentEditor(document, persistence)

        # Simulate a client using the editor with common text formatting features.
        editor.addText("Hello, world!")
        editor.addNewLine()
        editor.addText("This is a real-world document editor example.")
        editor.addNewLine()
        editor.addTabSpace()
        editor.addText("Indented text after a tab space.")
        editor.addNewLine()
        editor.addImage("picture.jpg")

        # Render and display the final document.
        print(editor.renderDocument())

        editor.saveDocument()


if __name__ == "__main__":
    # call the same demo as Java main
    DocumentEditorClient.main(None)
