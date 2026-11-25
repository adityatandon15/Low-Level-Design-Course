from random import Random

from .PlayStrategy import PlayStrategy


class RandomPlayStrategy(PlayStrategy):
    def __init__(self):
        self.currentPlaylist = None
        self.remainingSongs = None
        self.history = None
        self.random = Random()

    def setPlaylist(self, playlist):
        self.currentPlaylist = playlist
        if self.currentPlaylist is None or self.currentPlaylist.getSize() == 0:
            return

        self.remainingSongs = list(self.currentPlaylist.getSongs())
        self.history = []

    def hasNext(self):
        return self.currentPlaylist is not None and len(self.remainingSongs) != 0

    # Next in Loop
    def next(self):
        if self.currentPlaylist is None or self.currentPlaylist.getSize() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")
        if len(self.remainingSongs) == 0:
            raise RuntimeError("No songs left to play")

        idx = self.random.randrange(len(self.remainingSongs))
        selectedSong = self.remainingSongs[idx]

        # Remove the selectedSong from the list. (Swap and pop to remove in O(1))
        lastIndex = len(self.remainingSongs) - 1
        self.remainingSongs[idx] = self.remainingSongs[lastIndex]
        del self.remainingSongs[lastIndex]

        self.history.append(selectedSong)
        return selectedSong

    def hasPrevious(self):
        return len(self.history) > 0

    def previous(self):
        if len(self.history) == 0:
            raise RuntimeError("No previous song available.")

        song = self.history.pop()
        return song
