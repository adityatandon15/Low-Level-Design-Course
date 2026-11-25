# A Postcondition must be satisfied after a method is executed.
# Subclasses can strengthen the Postcondition but cannot weaken it.

class Car:
    def __init__(self):
        self.speed = 0

    def accelerate(self):
        print("Accelerating")
        self.speed += 20

    # PostCondition: Speed must reduce after brake
    def brake(self):
        print("Applying brakes")
        self.speed -= 20


# Subclass can strengthen postcondition - Does not violate LSP
class HybridCar(Car):
    def __init__(self):
        super().__init__()
        self._charge = 0

    # PostCondition: Speed must reduce after brake
    # PostCondition: Charge must increase.
    def brake(self):
        print("Applying brakes")
        self.speed -= 20
        self._charge += 10


class PostConditions:
    @staticmethod
    def main(args):
        hybridCar = HybridCar()
        hybridCar.brake()  # Works fine: HybridCar reduces speed and also increases charge.

        # Client feels no difference in substituting Hybrid car in place of Car.


if __name__ == "__main__":
    # call the same demo as Java main
    PostConditions.main(None)
