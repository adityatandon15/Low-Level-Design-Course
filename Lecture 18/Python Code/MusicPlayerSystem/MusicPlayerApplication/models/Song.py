class Song:
    def __init__(self, title, artist, filePath):
        self.title = title
        self.artist = artist
        self.filePath = filePath

    def getTitle(self):
        return self.title

    def getArtist(self):
        return self.artist

    def getFilePath(self):
        return self.filePath
