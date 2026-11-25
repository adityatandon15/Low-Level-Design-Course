from abc import ABC, abstractmethod

# Dynamic Polymorphism in real life says that 2 Objects coming from same
# family will respond to same stimulus differently. Like in real world Manual
# car and Electric car will respond to accelerate() differently.
#
# To represent this in programming, we create a parent class that defines all
# characters and behaviours that are generic to all child classes and are also same in
# all child classes but make those methods abstract that are generic to all
# child classes but all child class will behave differently. Then those child class
# will provide implementation details of these abstract methods the way they want.
class Car(ABC):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.isEngineOn = False
        self.currentSpeed = 0

    # Common methods for all cars.
    def startEngine(self):
        self.isEngineOn = True
        print(self.brand + " " + self.model + " : Engine started.")

    def stopEngine(self):
        self.isEngineOn = False
        self.currentSpeed = 0
        print(self.brand + " " + self.model + " : Engine turned off.")

    # Abstract methods for dynamic polymorphism
    @abstractmethod
    def accelerate(self):
        pass

    @abstractmethod
    def brake(self):
        pass


class ManualCar(Car):
    def __init__(self, brand, model):
        super().__init__(brand, model)
        self._currentGear = 0

    # Specialized method for Manual Car
    def shiftGear(self, gear):
        self._currentGear = gear
        print(self.brand + " " + self.model + " : Shifted to gear " + str(self._currentGear))

    # Overriding accelerate - Dynamic Polymorphism
    def accelerate(self):
        if not self.isEngineOn:
            print(self.brand + " " + self.model + " : Cannot accelerate! Engine is off.")
            return
        self.currentSpeed += 20
        print(self.brand + " " + self.model + " : Accelerating to " + str(self.currentSpeed) + " km/h")

    # Overriding brake - Dynamic Polymorphism
    def brake(self):
        self.currentSpeed -= 20
        if self.currentSpeed < 0:
            self.currentSpeed = 0
        print(self.brand + " " + self.model + " : Braking! Speed is now " + str(self.currentSpeed) + " km/h")


class ElectricCar(Car):
    def __init__(self, brand, model):
        super().__init__(brand, model)
        self._batteryLevel = 100

    # Specialized method for Electric Car
    def chargeBattery(self):
        self._batteryLevel = 100
        print(self.brand + " " + self.model + " : Battery fully charged!")

    # Overriding accelerate - Dynamic Polymorphism
    def accelerate(self):
        if not self.isEngineOn:
            print(self.brand + " " + self.model + " : Cannot accelerate! Engine is off.")
            return
        if self._batteryLevel <= 0:
            print(self.brand + " " + self.model + " : Battery dead! Cannot accelerate.")
            return
        self._batteryLevel -= 10
        self.currentSpeed += 15
        print(self.brand + " " + self.model + " : Accelerating to " + str(self.currentSpeed)
              + " km/h. Battery at " + str(self._batteryLevel) + "%.")

    # Overriding brake - Dynamic Polymorphism
    def brake(self):
        self.currentSpeed -= 15
        if self.currentSpeed < 0:
            self.currentSpeed = 0
        print(self.brand + " " + self.model
              + " : Regenerative braking! Speed is now " + str(self.currentSpeed)
              + " km/h. Battery at " + str(self._batteryLevel) + "%.")


class DynamicPolymorphism:
    @staticmethod
    def main(args):
        myManualCar = ManualCar("Suzuki", "WagonR")
        myManualCar.startEngine()
        myManualCar.accelerate()
        myManualCar.accelerate()
        myManualCar.brake()
        myManualCar.stopEngine()

        print("----------------------")

        myElectricCar = ElectricCar("Tesla", "Model S")
        myElectricCar.startEngine()
        myElectricCar.accelerate()
        myElectricCar.accelerate()
        myElectricCar.brake()
        myElectricCar.stopEngine()


if __name__ == "__main__":
    # call the same demo as Java main
    DynamicPolymorphism.main(None)
