from .IAudioOutputDevice import IAudioOutputDevice


class WiredSpeakerAdapter(IAudioOutputDevice):
    def __init__(self, api):
        self.wiredApi = api

    def playAudio(self, song):
        payload = song.getTitle() + " by " + song.getArtist()
        self.wiredApi.playSoundViaCable(payload)
