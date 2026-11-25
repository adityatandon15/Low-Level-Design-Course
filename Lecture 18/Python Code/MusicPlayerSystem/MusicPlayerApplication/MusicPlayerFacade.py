import threading

from .core.AudioEngine import AudioEngine
from .managers.DeviceManager import DeviceManager
from .managers.PlaylistManager import PlaylistManager
from .managers.StrategyManager import StrategyManager


class MusicPlayerFacade:
    instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.loadedPlaylist = None
        self.playStrategy = None
        self.audioEngine = AudioEngine()

    @staticmethod
    def getInstance():
        with MusicPlayerFacade._lock:
            if MusicPlayerFacade.instance is None:
                MusicPlayerFacade.instance = MusicPlayerFacade()
            return MusicPlayerFacade.instance

    def connectDevice(self, deviceType):
        DeviceManager.getInstance().connect(deviceType)

    def setPlayStrategy(self, strategyType):
        self.playStrategy = StrategyManager.getInstance().getStrategy(strategyType)

    def loadPlaylist(self, name):
        self.loadedPlaylist = PlaylistManager.getInstance().getPlaylist(name)
        if self.playStrategy is None:
            raise RuntimeError("Play strategy not set before loading.")
        self.playStrategy.setPlaylist(self.loadedPlaylist)

    def playSong(self, song):
        if not DeviceManager.getInstance().hasOutputDevice():
            raise RuntimeError("No audio device connected.")
        device = DeviceManager.getInstance().getOutputDevice()
        self.audioEngine.play(device, song)

    def pauseSong(self, song):
        if self.audioEngine.getCurrentSongTitle() != song.getTitle():
            raise RuntimeError("Cannot pause \"" + song.getTitle() + "\"; not currently playing.")
        self.audioEngine.pause()

    def playAllTracks(self):
        if self.loadedPlaylist is None:
            raise RuntimeError("No playlist loaded.")
        while self.playStrategy.hasNext():
            nextSong = self.playStrategy.next()
            device = DeviceManager.getInstance().getOutputDevice()
            self.audioEngine.play(device, nextSong)
        print("Completed playlist: " + self.loadedPlaylist.getPlaylistName())

    def playNextTrack(self):
        if self.loadedPlaylist is None:
            raise RuntimeError("No playlist loaded.")
        if self.playStrategy.hasNext():
            nextSong = self.playStrategy.next()
            device = DeviceManager.getInstance().getOutputDevice()
            self.audioEngine.play(device, nextSong)
        else:
            print("Completed playlist: " + self.loadedPlaylist.getPlaylistName())

    def playPreviousTrack(self):
        if self.loadedPlaylist is None:
            raise RuntimeError("No playlist loaded.")
        if self.playStrategy.hasPrevious():
            prevSong = self.playStrategy.previous()
            device = DeviceManager.getInstance().getOutputDevice()
            self.audioEngine.play(device, prevSong)
        else:
            print("Completed playlist: " + self.loadedPlaylist.getPlaylistName())

    def enqueueNext(self, song):
        self.playStrategy.addToNext(song)
