from abc import ABC, abstractmethod


class IAudioOutputDevice(ABC):
    @abstractmethod
    def playAudio(self, song):
        pass
