import threading

from ..enums.DeviceType import DeviceType
from ..factories.DeviceFactory import DeviceFactory


class DeviceManager:
    instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.currentOutputDevice = None

    @staticmethod
    def getInstance():
        with DeviceManager._lock:
            if DeviceManager.instance is None:
                DeviceManager.instance = DeviceManager()
            return DeviceManager.instance

    def connect(self, deviceType):
        if self.currentOutputDevice is not None:
            # In C++: delete currentOutputDevice;
            # In Java, garbage collector handles it, so no explicit delete.
            pass

        self.currentOutputDevice = DeviceFactory.createDevice(deviceType)

        if deviceType == DeviceType.BLUETOOTH:
            print("Bluetooth device connected ")
        elif deviceType == DeviceType.WIRED:
            print("Wired device connected ")
        elif deviceType == DeviceType.HEADPHONES:
            print("Headphones connected ")

    def getOutputDevice(self):
        if self.currentOutputDevice is None:
            raise RuntimeError("No output device is connected.")
        return self.currentOutputDevice

    def hasOutputDevice(self):
        return self.currentOutputDevice is not None
