class AudioEngine:
    def __init__(self):
        self.currentSong = None
        self.songIsPaused = False

    def getCurrentSongTitle(self):
        if self.currentSong is not None:
            return self.currentSong.getTitle()
        return ""

    def isPaused(self):
        return self.songIsPaused

    def play(self, aod, song):
        if song is None:
            raise RuntimeError("Cannot play a null song.")
        # Resume if same song was paused
        if self.songIsPaused and song is self.currentSong:
            self.songIsPaused = False
            print("Resuming song: " + song.getTitle())
            aod.playAudio(song)
            return

        self.currentSong = song
        self.songIsPaused = False
        print("Playing song: " + song.getTitle())
        aod.playAudio(song)

    def pause(self):
        if self.currentSong is None:
            raise RuntimeError("No song is currently playing to pause.")
        if self.songIsPaused:
            raise RuntimeError("Song is already paused.")
        self.songIsPaused = True
        print("Pausing song: " + self.currentSong.getTitle())
