class Playlist:
    def __init__(self, name):
        self.playlistName = name
        self.songList = []

    def getPlaylistName(self):
        return self.playlistName

    def getSongs(self):
        return self.songList

    def getSize(self):
        return len(self.songList)

    def addSongToPlaylist(self, song):
        if song is None:
            raise RuntimeError("Cannot add null song to playlist.")
        self.songList.append(song)
