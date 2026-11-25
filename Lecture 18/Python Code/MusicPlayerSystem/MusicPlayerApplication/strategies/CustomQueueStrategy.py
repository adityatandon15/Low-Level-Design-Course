from collections import deque

from .PlayStrategy import PlayStrategy


class CustomQueueStrategy(PlayStrategy):
    def __init__(self):
        self.currentPlaylist = None
        self.currentIndex = -1
        self.nextQueue = deque()
        self.prevStack = []

    def nextSequential(self):
        if self.currentPlaylist.getSize() == 0:
            raise RuntimeError("Playlist is empty.")
        self.currentIndex = self.currentIndex + 1
        return self.currentPlaylist.getSongs()[self.currentIndex]

    def previousSequential(self):
        if self.currentPlaylist.getSize() == 0:
            raise RuntimeError("Playlist is empty.")
        self.currentIndex = self.currentIndex - 1
        return self.currentPlaylist.getSongs()[self.currentIndex]

    def setPlaylist(self, playlist):
        self.currentPlaylist = playlist
        self.currentIndex = -1
        self.nextQueue.clear()
        self.prevStack.clear()

    def hasNext(self):
        return (self.currentIndex + 1) < self.currentPlaylist.getSize()

    def next(self):
        if self.currentPlaylist is None or self.currentPlaylist.getSize() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")

        if len(self.nextQueue) != 0:
            s = self.nextQueue.popleft()
            self.prevStack.append(s)

            # update index to match queued song
            songs = self.currentPlaylist.getSongs()
            for i in range(len(songs)):
                if songs[i] is s:
                    self.currentIndex = i
                    break
            return s

        # Otherwise sequential
        return self.nextSequential()

    def hasPrevious(self):
        return (self.currentIndex - 1) > 0

    def previous(self):
        if self.currentPlaylist is None or self.currentPlaylist.getSize() == 0:
            raise RuntimeError("No playlist loaded or playlist is empty.")

        if len(self.prevStack) != 0:
            s = self.prevStack.pop()

            # update index to match stacked song
            songs = self.currentPlaylist.getSongs()
            for i in range(len(songs)):
                if songs[i] is s:
                    self.currentIndex = i
                    break
            return s

        # Otherwise sequential
        return self.previousSequential()

    def addToNext(self, song):
        if song is None:
            raise RuntimeError("Cannot enqueue null song.")
        self.nextQueue.append(song)
