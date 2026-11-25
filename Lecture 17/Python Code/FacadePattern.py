# Subsystems
class PowerSupply:
    def providePower(self):
        print("Power Supply: Providing power...")


class CoolingSystem:
    def startFans(self):
        print("Cooling System: Fans started...")


class CPU:
    def initialize(self):
        print("CPU: Initialization started...")


class Memory:
    def selfTest(self):
        print("Memory: Self-test passed...")


class HardDrive:
    def spinUp(self):
        print("Hard Drive: Spinning up...")


class BIOS:
    def boot(self, cpu, memory):
        print("BIOS: Booting CPU and Memory checks...")
        cpu.initialize()
        memory.selfTest()


class OperatingSystem:
    def load(self):
        print("Operating System: Loading into memory...")


# Facade
class ComputerFacade:
    def __init__(self):
        self._powerSupply = PowerSupply()
        self._coolingSystem = CoolingSystem()
        self._cpu = CPU()
        self._memory = Memory()
        self._hardDrive = HardDrive()
        self._bios = BIOS()
        self._os = OperatingSystem()

    def startComputer(self):
        print("----- Starting Computer -----")
        self._powerSupply.providePower()
        self._coolingSystem.startFans()
        self._bios.boot(self._cpu, self._memory)
        self._hardDrive.spinUp()
        self._os.load()
        print("Computer Booted Successfully!")


# Client
class FacadePattern:
    @staticmethod
    def main(args=None):
        computer = ComputerFacade()
        computer.startComputer()


if __name__ == "__main__":
    FacadePattern.main()
