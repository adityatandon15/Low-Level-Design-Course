from .IAudioOutputDevice import IAudioOutputDevice


class BluetoothSpeakerAdapter(IAudioOutputDevice):
    def __init__(self, api):
        self.bluetoothApi = api

    def playAudio(self, song):
        payload = song.getTitle() + " by " + song.getArtist()
        self.bluetoothApi.playSoundViaBluetooth(payload)
