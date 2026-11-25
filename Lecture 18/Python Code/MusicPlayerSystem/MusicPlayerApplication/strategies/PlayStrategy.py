from abc import ABC, abstractmethod


class PlayStrategy(ABC):
    @abstractmethod
    def setPlaylist(self, playlist):
        pass

    @abstractmethod
    def next(self):
        pass

    @abstractmethod
    def hasNext(self):
        pass

    @abstractmethod
    def previous(self):
        pass

    @abstractmethod
    def hasPrevious(self):
        pass

    def addToNext(self, song):
        pass
