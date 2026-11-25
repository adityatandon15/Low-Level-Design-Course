from abc import ABC, abstractmethod


# Implementation Hierarchy: Engine interface (LLL)
class Engine(ABC):
    @abstractmethod
    def start(self):
        pass


# Concrete Implementors (LLL)
class PetrolEngine(Engine):
    def start(self):
        print("Petrol engine starting with ignition!")


class DieselEngine(Engine):
    def start(self):
        print("Diesel engine roaring to life!")


class ElectricEngine(Engine):
    def start(self):
        print("Electric engine powering up silently!")


# Abstraction Hierarchy: Car (HLL)
class Car(ABC):
    def __init__(self, e):
        self.engine = e

    @abstractmethod
    def drive(self):
        pass


# Refined Abstraction: Sedan
class Sedan(Car):
    def __init__(self, e):
        super().__init__(e)

    def drive(self):
        self.engine.start()
        print("Driving a Sedan on the highway.")


# Refined Abstraction: SUV
class SUV(Car):
    def __init__(self, e):
        super().__init__(e)

    def drive(self):
        self.engine.start()
        print("Driving an SUV off-road.")


class BridgePattern:
    @staticmethod
    def main(args):
        # Create Engine implementations
        petrolEng = PetrolEngine()
        dieselEng = DieselEngine()
        electricEng = ElectricEngine()

        # Create Car abstractions, injecting Engine implementations
        mySedan = Sedan(petrolEng)
        mySUV = SUV(electricEng)
        yourSUV = SUV(dieselEng)

        # Use the cars
        mySedan.drive()   # Petrol engine + Sedan
        mySUV.drive()     # Electric engine + SUV
        yourSUV.drive()   # Diesel engine + SUV

        # No explicit cleanup needed in Java


if __name__ == "__main__":
    BridgePattern.main([])
