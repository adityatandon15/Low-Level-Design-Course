# We know that real world Objects show inheritance relationship where we
# have parent object and child object. child object have all the characters
# or behaviours that parent have plus some additional characters/behaviours.
# Like all cars in real world have a brand, model etc and can start, stop,
# accelerate etc. But some specific cars like manual car have gear System
# while other specific cars like Electric cars have battery system.
#
# We represent this scenario of real world in programming by creating a parent class and
# defining all the characters(variables) or behaviours(methods) that all cars
# have in parent class. Then we create different child classes that inherits
# from this parent class and define only those characters and behaviours
# that are specific to them. Although objects of these child classes can
# access or call parent class characters(variables) and behaviours(methods).
# Hence providing code reusability.
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.isEngineOn = False
        self.currentSpeed = 0

    # Common methods for all cars
    def startEngine(self):
        self.isEngineOn = True
        print(self.brand + " " + self.model + " : Engine started.")

    def stopEngine(self):
        self.isEngineOn = False
        self.currentSpeed = 0
        print(self.brand + " " + self.model + " : Engine turned off.")

    def accelerate(self):
        if not self.isEngineOn:
            print(self.brand + " " + self.model + " : Cannot accelerate! Engine is off.")
            return
        self.currentSpeed += 20
        print(self.brand + " " + self.model + " : Accelerating to " + str(self.currentSpeed) + " km/h")

    def brake(self):
        self.currentSpeed -= 20
        if self.currentSpeed < 0:
            self.currentSpeed = 0
        print(self.brand + " " + self.model + " : Braking! Speed is now " + str(self.currentSpeed) + " km/h")


class ManualCar(Car):  # Inherits from Car
    def __init__(self, brand, model):
        super().__init__(brand, model)
        self._currentGear = 0  # spcific to Manual Car.

    # Specialized method for Manual Car
    def shiftGear(self, gear):
        self._currentGear = gear
        print(self.brand + " " + self.model + " : Shifted to gear " + str(self._currentGear))


class ElectricCar(Car):  # Inherits from Car
    def __init__(self, brand, model):
        super().__init__(brand, model)
        self._batteryLevel = 100  # spcific to Electric Car.

    # Specialized method for Electric Car
    def chargeBattery(self):
        self._batteryLevel = 100
        print(self.brand + " " + self.model + " : Battery fully charged!")


# Main Class
class Inheritance:
    @staticmethod
    def main(args):
        myManualCar = ManualCar("Suzuki", "WagonR")
        myManualCar.startEngine()
        myManualCar.shiftGear(1)  # Specific to Manual Car
        myManualCar.accelerate()
        myManualCar.brake()
        myManualCar.stopEngine()

        print("----------------------")

        myElectricCar = ElectricCar("Tesla", "Model S")
        myElectricCar.chargeBattery()  # Specific to Electric Car
        myElectricCar.startEngine()
        myElectricCar.accelerate()
        myElectricCar.brake()
        myElectricCar.stopEngine()


if __name__ == "__main__":
    # call the same demo as Java main
    Inheritance.main(None)
