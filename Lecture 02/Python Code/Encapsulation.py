# Encapsulation says 2 things:
# 1. An Object's Characteristics and its behaviour are encapsulated together
# within that Object.
# 2. All the characteristics or behaviours are not for everyone to access.
# Object should provide data security.
#
# We follow above 2 pointers about Object of real world in programming by:
# 1. Creating a class that act as a blueprint for Object creation. Class contain
# all the characteristics (class variable) and behaviour (class methods) in one block,
# encapsulating it together.
# 2. We introduce access modifiers (public, private, protected, default) etc to provide data
# security to the class members.

class SportsCar:
    def __init__(self, brand, model):
        self._brand = brand
        self._model = model
        self._isEngineOn = False
        self._currentSpeed = 0
        self._currentGear = 0

        # Introduce new variable to exaplain setters
        self._tyreCompany = None

    def getSpeed(self):
        return self._currentSpeed

    def getTyreCompany(self):
        return self._tyreCompany

    def setTyreCompany(self, tyreCompany):
        self._tyreCompany = tyreCompany

    def startEngine(self):
        self._isEngineOn = True
        print(self._brand + " " + self._model + " : Engine starts with a roar!")

    def shiftGear(self, gear):
        self._currentGear = gear
        print(self._brand + " " + self._model + " : Shifted to gear " + str(self._currentGear))

    def accelerate(self):
        if not self._isEngineOn:
            print(self._brand + " " + self._model + " : Engine is off! Cannot accelerate.")
            return
        self._currentSpeed += 20
        print(self._brand + " " + self._model + " : Accelerating to " + str(self._currentSpeed) + " km/h")

    def brake(self):
        self._currentSpeed -= 20
        if self._currentSpeed < 0:
            self._currentSpeed = 0
        print(self._brand + " " + self._model + " : Braking! Speed is now " + str(self._currentSpeed) + " km/h")

    def stopEngine(self):
        self._isEngineOn = False
        self._currentGear = 0
        self._currentSpeed = 0
        print(self._brand + " " + self._model + " : Engine turned off.")


# Main Method
class Encapsulation:
    @staticmethod
    def main(args):
        mySportsCar = SportsCar("Ford", "Mustang")

        mySportsCar.startEngine()
        mySportsCar.shiftGear(1)
        mySportsCar.accelerate()
        mySportsCar.shiftGear(2)
        mySportsCar.accelerate()
        mySportsCar.brake()
        mySportsCar.stopEngine()

        # Setting arbitrary value to speed.
        # mySportsCar.currentSpeed = 500;

        # System.out.println("Current Speed of My Sports Car is set to " + mySportsCar.currentSpeed);

        print("Current Speed of My Sports Car is " + str(mySportsCar.getSpeed()))


if __name__ == "__main__":
    # call the same demo as Java main
    Encapsulation.main(None)
