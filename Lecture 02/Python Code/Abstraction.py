from abc import ABC, abstractmethod

# Car Interface --> Act as an interface for Outsiude world to operate the car.
# This interface tells 'WHAT' all it can do rather then 'HOW' it does that.
# Since this is an interface we cannot directly create Objects of this. We
# need to implement it first and then that child class will have the responsibility to
# provide implementation details of all the methods in the interface.
#
# In our real world example of Car, imagine you sitting in the car and able to operate
# the car (startEngine, accelerate, brake, turn) just by pressing or moving some
# pedals/buttons/stearing wheel etc. You dont need to know how these things work, and
# also they are hidden under thre hood.
# This Interface 'Car' denotes that (pedals/buttons/stearing wheel etc).

class Car(ABC):
    @abstractmethod
    def startEngine(self):
        pass

    @abstractmethod
    def shiftGear(self, gear):
        pass

    @abstractmethod
    def accelerate(self):
        pass

    @abstractmethod
    def brake(self):
        pass

    @abstractmethod
    def stopEngine(self):
        pass


# This is a Concrete class (A class that provide implementation details of an interface/abstract class).
# Now anyone can make an Object of 'SportsCar' and can assign it to 'Car' reference.
# (See main method for this)
#
# In our real world example of Car, as you cannot have a real car by just having its body only
# (all these buttons or pedals). You need to have the actual implementation of 'What' happens
# when we press these buttons. 'SportsCar' class denotes that actual implementation.
#
# Hence we can concude, to denote a real world car in programming we created 2 classes.
# One to deonte all the user-interface like pedals, buttons, stearing wheels etc ('Car' interface).
# And another one to denote the actual car with all the implementations of these buttons (SportsCar' class).
class SportsCar(Car):
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model
        self.isEngineOn = False
        self.currentSpeed = 0
        self.currentGear = 0

    def startEngine(self):
        self.isEngineOn = True
        print(self.brand + " " + self.model + " : Engine starts with a roar!")

    def shiftGear(self, gear):
        if not self.isEngineOn:
            print(self.brand + " " + self.model + " : Engine is off! Cannot Cannot Shift Gear.")
            return
        self.currentGear = gear
        print(self.brand + " " + self.model + " : Shifted to gear " + str(self.currentGear))

    def accelerate(self):
        if not self.isEngineOn:
            print(self.brand + " " + self.model + " : Engine is off! Cannot accelerate.")
            return
        self.currentSpeed += 20
        print(self.brand + " " + self.model + " : Accelerating to " + str(self.currentSpeed) + " km/h")

    def brake(self):
        self.currentSpeed -= 20
        if self.currentSpeed < 0:
            self.currentSpeed = 0
        print(self.brand + " " + self.model + " : Braking! Speed is now " + str(self.currentSpeed) + " km/h")

    def stopEngine(self):
        self.isEngineOn = False
        self.currentGear = 0
        self.currentSpeed = 0
        print(self.brand + " " + self.model + " : Engine turned off.")


# Main Method
class Abstraction:
    @staticmethod
    def main(args):
        myCar = SportsCar("Ford", "Mustang")

        myCar.startEngine()
        myCar.shiftGear(1)
        myCar.accelerate()
        myCar.shiftGear(2)
        myCar.accelerate()
        myCar.brake()
        myCar.stopEngine()


if __name__ == "__main__":
    # call the same demo as Java main
    Abstraction.main(None)
