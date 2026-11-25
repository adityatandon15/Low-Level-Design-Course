# Static Polymorphism (Compile-time polymorphism) in real life says that
# the same action can behave differently depending on the input parameters.
# For example, a Manual car can accelerate by a fixed amount or by a
# specific amount you request. In programming, we achieve this via method
# overloading: multiple methods with the same name but different signatures.

class ManualCar:
    def __init__(self, brand, model):
        self._brand = brand
        self._model = model
        self._isEngineOn = False
        self._currentSpeed = 0
        self._currentGear = 0

    def startEngine(self):
        self._isEngineOn = True
        print(self._brand + " " + self._model + " : Engine started.")

    def stopEngine(self):
        self._isEngineOn = False
        self._currentSpeed = 0
        print(self._brand + " " + self._model + " : Engine turned off.")

    # Overloading accelerate - Static Polymorphism
    # accelerate() and accelerate(int speed) share one Python method.
    # speed is None for the no-argument overload.
    def accelerate(self, speed=None):
        if not self._isEngineOn:
            print(self._brand + " " + self._model + " : Cannot accelerate! Engine is off.")
            return
        if speed is None:
            self._currentSpeed += 20
        else:
            self._currentSpeed += speed
        print(self._brand + " " + self._model + " : Accelerating to " + str(self._currentSpeed) + " km/h")

    def brake(self):
        self._currentSpeed -= 20
        if self._currentSpeed < 0:
            self._currentSpeed = 0
        print(self._brand + " " + self._model + " : Braking! Speed is now "
              + str(self._currentSpeed) + " km/h")

    def shiftGear(self, gear):
        self._currentGear = gear
        print(self._brand + " " + self._model + " : Shifted to gear " + str(self._currentGear))


class StaticPolymorphism:
    @staticmethod
    def main(args):
        myManualCar = ManualCar("Suzuki", "WagonR")
        myManualCar.startEngine()
        myManualCar.accelerate()
        myManualCar.accelerate(40)
        myManualCar.brake()
        myManualCar.stopEngine()


if __name__ == "__main__":
    # call the same demo as Java main
    StaticPolymorphism.main(None)
