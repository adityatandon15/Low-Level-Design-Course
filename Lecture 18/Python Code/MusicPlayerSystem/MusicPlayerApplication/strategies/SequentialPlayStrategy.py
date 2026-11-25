from .PlayStrategy import PlayStrategy


class SequentialPlayStrategy(PlayStrategy):
    def __init__(self):
        self.currentPlaylist = None
        self.currentIndex = -1

    def setPlaylist(self, playlist):
        self.currentPlaylist = playlist
        self.currentIndex = -1

    def hasNext(self):
        return (self.currentIndex + 1) < self.currentPlaylist.getSize()

    # Next in Loop
    def next(self):
        if self.currentPlaylist is None or self.currentPlaylist.getSize() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")
        self.currentIndex = self.currentIndex + 1
        return self.currentPlaylist.getSongs()[self.currentIndex]

    def hasPrevious(self):
        return (self.currentIndex - 1) > 0

    # previous in Loop
    def previous(self):
        if self.currentPlaylist is None or self.currentPlaylist.getSize() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")
        self.currentIndex = self.currentIndex - 1
        return self.currentPlaylist.getSongs()[self.currentIndex]
