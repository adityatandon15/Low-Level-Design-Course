from .IAudioOutputDevice import IAudioOutputDevice


class HeadphonesAdapter(IAudioOutputDevice):
    def __init__(self, api):
        self.headphonesApi = api

    def playAudio(self, song):
        payload = song.getTitle() + " by " + song.getArtist()
        self.headphonesApi.playSoundViaJack(payload)
