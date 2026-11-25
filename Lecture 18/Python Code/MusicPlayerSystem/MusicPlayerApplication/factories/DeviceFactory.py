from ..device.BluetoothSpeakerAdapter import BluetoothSpeakerAdapter
from ..device.HeadphonesAdapter import HeadphonesAdapter
from ..device.WiredSpeakerAdapter import WiredSpeakerAdapter
from ..external.BluetoothSpeakerAPI import BluetoothSpeakerAPI
from ..external.HeadphonesAPI import HeadphonesAPI
from ..external.WiredSpeakerAPI import WiredSpeakerAPI
from ..enums.DeviceType import DeviceType


class DeviceFactory:
    @staticmethod
    def createDevice(deviceType):
        if deviceType == DeviceType.BLUETOOTH:
            return BluetoothSpeakerAdapter(BluetoothSpeakerAPI())
        elif deviceType == DeviceType.WIRED:
            return WiredSpeakerAdapter(WiredSpeakerAPI())
        else:
            # HEADPHONES and default
            return HeadphonesAdapter(HeadphonesAPI())
