import threading

from ..models.Playlist import Playlist


class PlaylistManager:
    instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.playlists = {}

    @staticmethod
    def getInstance():
        with PlaylistManager._lock:
            if PlaylistManager.instance is None:
                PlaylistManager.instance = PlaylistManager()
            return PlaylistManager.instance

    def createPlaylist(self, name):
        if name in self.playlists:
            raise RuntimeError("Playlist \"" + name + "\" already exists.")
        self.playlists[name] = Playlist(name)

    def addSongToPlaylist(self, playlistName, song):
        if playlistName not in self.playlists:
            raise RuntimeError("Playlist \"" + playlistName + "\" not found.")
        self.playlists[playlistName].addSongToPlaylist(song)

    def getPlaylist(self, name):
        if name not in self.playlists:
            raise RuntimeError("Playlist \"" + name + "\" not found.")
        return self.playlists[name]
