class DocumentEditor:
    def __init__(self):
        self._documentElements = []
        self._renderedDocument = ""

    # Adds text as a plain string
    def addText(self, text):
        self._documentElements.append(text)

    # Adds an image represented by its file path
    def addImage(self, imagePath):
        self._documentElements.append(imagePath)

    # Renders the document by checking the type of each element at runtime
    def renderDocument(self):
        if self._renderedDocument == "":
            result = ""
            for element in self._documentElements:
                if len(element) > 4 and (element.endswith(".jpg") or element.endswith(".png")):
                    result += "[Image: " + element + "]\n"
                else:
                    result += element + "\n"
            self._renderedDocument = result
        return self._renderedDocument

    def saveToFile(self):
        try:
            writer = open("document.txt", "w")
            writer.write(self.renderDocument())
            writer.close()
            print("Document saved to document.txt")
        except OSError:
            print("Error: Unable to open file for writing.")


class DocumentEditorClient:
    @staticmethod
    def main(args):
        editor = DocumentEditor()
        editor.addText("Hello, world!")
        editor.addImage("picture.jpg")
        editor.addText("This is a document editor.")

        print(editor.renderDocument())

        editor.saveToFile()


if __name__ == "__main__":
    # call the same demo as Java main
    DocumentEditorClient.main(None)
