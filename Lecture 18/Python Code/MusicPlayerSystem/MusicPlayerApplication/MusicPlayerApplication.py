import threading

from .managers.PlaylistManager import PlaylistManager
from .models.Song import Song
from .MusicPlayerFacade import MusicPlayerFacade


class MusicPlayerApplication:
    instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.songLibrary = []

    @staticmethod
    def getInstance():
        with MusicPlayerApplication._lock:
            if MusicPlayerApplication.instance is None:
                MusicPlayerApplication.instance = MusicPlayerApplication()
            return MusicPlayerApplication.instance

    def createSongInLibrary(self, title, artist, path):
        newSong = Song(title, artist, path)
        self.songLibrary.append(newSong)

    def findSongByTitle(self, title):
        for s in self.songLibrary:
            if s.getTitle() == title:
                return s
        return None

    def createPlaylist(self, playlistName):
        PlaylistManager.getInstance().createPlaylist(playlistName)

    def addSongToPlaylist(self, playlistName, songTitle):
        song = self.findSongByTitle(songTitle)
        if song is None:
            raise RuntimeError("Song \"" + songTitle + "\" not found in library.")
        PlaylistManager.getInstance().addSongToPlaylist(playlistName, song)

    def connectAudioDevice(self, deviceType):
        MusicPlayerFacade.getInstance().connectDevice(deviceType)

    def selectPlayStrategy(self, strategyType):
        MusicPlayerFacade.getInstance().setPlayStrategy(strategyType)

    def loadPlaylist(self, playlistName):
        MusicPlayerFacade.getInstance().loadPlaylist(playlistName)

    def playSingleSong(self, songTitle):
        song = self.findSongByTitle(songTitle)
        if song is None:
            raise RuntimeError("Song \"" + songTitle + "\" not found.")
        MusicPlayerFacade.getInstance().playSong(song)

    def pauseCurrentSong(self, songTitle):
        song = self.findSongByTitle(songTitle)
        if song is None:
            raise RuntimeError("Song \"" + songTitle + "\" not found.")
        MusicPlayerFacade.getInstance().pauseSong(song)

    def playAllTracksInPlaylist(self):
        MusicPlayerFacade.getInstance().playAllTracks()

    def playPreviousTrackInPlaylist(self):
        MusicPlayerFacade.getInstance().playPreviousTrack()

    def queueSongNext(self, songTitle):
        song = self.findSongByTitle(songTitle)
        if song is None:
            raise RuntimeError("Song \"" + songTitle + "\" not found.")
        MusicPlayerFacade.getInstance().enqueueNext(song)
