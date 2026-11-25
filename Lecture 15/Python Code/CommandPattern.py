from abc import ABC, abstractmethod


# ----------------------------
# Command Interface
# ----------------------------
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


# ----------------------------
# Receivers
# ----------------------------
class Light:
    def on(self):
        print("Light is ON")

    def off(self):
        print("Light is OFF")


class Fan:
    def on(self):
        print("Fan is ON")

    def off(self):
        print("Fan is OFF")


# ----------------------------
# Concrete Command for Light
# ----------------------------
class LightCommand(Command):
    def __init__(self, l):
        self._light = l

    def execute(self):
        self._light.on()

    def undo(self):
        self._light.off()


# ----------------------------
# Concrete Command for Fan
# ----------------------------
class FanCommand(Command):
    def __init__(self, f):
        self._fan = f

    def execute(self):
        self._fan.on()

    def undo(self):
        self._fan.off()


# ----------------------------
# Invoker: Remote Controller with static array of 4 buttons
# ----------------------------
class RemoteController:
    _numButtons = 4

    def __init__(self):
        self._buttons = [None] * RemoteController._numButtons
        self._buttonPressed = [False] * RemoteController._numButtons
        for i in range(RemoteController._numButtons):
            self._buttons[i] = None
            self._buttonPressed[i] = False  # false = off, true = on

    def setCommand(self, idx, cmd):
        if idx >= 0 and idx < RemoteController._numButtons:
            self._buttons[idx] = cmd
            self._buttonPressed[idx] = False

    def pressButton(self, idx):
        if idx >= 0 and idx < RemoteController._numButtons and self._buttons[idx] is not None:
            if not self._buttonPressed[idx]:
                self._buttons[idx].execute()
            else:
                self._buttons[idx].undo()
            self._buttonPressed[idx] = not self._buttonPressed[idx]
        else:
            print("No command assigned at button " + str(idx))


# ----------------------------
# Main Application
# ----------------------------
class CommandPattern:
    @staticmethod
    def main(args=None):
        livingRoomLight = Light()
        ceilingFan = Fan()

        remote = RemoteController()

        remote.setCommand(0, LightCommand(livingRoomLight))
        remote.setCommand(1, FanCommand(ceilingFan))

        # Simulate button presses (toggle behavior)
        print("--- Toggling Light Button 0 ---")
        remote.pressButton(0)  # ON
        remote.pressButton(0)  # OFF

        print("--- Toggling Fan Button 1 ---")
        remote.pressButton(1)  # ON
        remote.pressButton(1)  # OFF

        # Press unassigned button to show default message
        print("--- Pressing Unassigned Button 2 ---")
        remote.pressButton(2)


if __name__ == "__main__":
    CommandPattern.main()
