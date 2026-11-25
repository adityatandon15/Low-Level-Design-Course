from abc import ABC, abstractmethod

# Base Car class
class Car(ABC):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.isEngineOn = False
        self.currentSpeed = 0

    # Common methods for All cars.
    def startEngine(self):
        self.isEngineOn = True
        print(self.brand + " " + self.model + " : Engine started.")

    def stopEngine(self):
        self.isEngineOn = False
        self.currentSpeed = 0
        print(self.brand + " " + self.model + " : Engine turned off.")

    # Abstract method for Dynamic Polymorphism
    # Abstract method for Static Polymorphism
    # accelerate() and accelerate(int speed). speed is None for the no-argument overload.
    @abstractmethod
    def accelerate(self, speed=None):
        pass

    # Abstract method for Dynamic Polymorphism
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
    # overriding and overloading accelerate at the same time.
    def accelerate(self, speed=None):
        if not self.isEngineOn:
            print(self.brand + " " + self.model + " : Cannot accelerate! Engine is off.")
            return
        if speed is None:
            self.currentSpeed += 20
        else:
            self.currentSpeed += speed
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

    # specialized method for Electric Car
    def chargeBattery(self):
        self._batteryLevel = 100
        print(self.brand + " " + self.model + " : Battery fully charged!")

    # Overriding accelerate - Dynamic Polymorphism
    def accelerate(self, speed=None):
        if not self.isEngineOn:
            print(self.brand + " " + self.model + " : Cannot accelerate! Engine is off.")
            return
        if self._batteryLevel <= 0:
            print(self.brand + " " + self.model + " : Battery dead! Cannot accelerate.")
            return
        if speed is None:
            self._batteryLevel -= 10
            self.currentSpeed += 15
        else:
            self._batteryLevel -= 10 + speed
            self.currentSpeed += speed
        print(self.brand + " " + self.model + " : Accelerating to " + str(self.currentSpeed) +
              " km/h. Battery at " + str(self._batteryLevel) + "%.")

    # Overriding brake - Dynamic Polymorphism
    def brake(self):
        self.currentSpeed -= 15
        if self.currentSpeed < 0:
            self.currentSpeed = 0
        print(self.brand + " " + self.model +
              " : Regenerative braking! Speed is now " + str(self.currentSpeed) +
              " km/h. Battery at " + str(self._batteryLevel) + "%.")


# Main function
class StaticAndDynamicPolymorphism:
    @staticmethod
    def main(args):
        myManualCar = ManualCar("Ford", "Mustang")
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
    StaticAndDynamicPolymorphism.main(None)
