from abc import ABC, abstractmethod

# Product Interface and subclasses
class Burger(ABC):
    @abstractmethod
    def prepare(self):
        pass


class BasicBurger(Burger):
    def prepare(self):
        print("Preparing Basic Burger with bun, patty, and ketchup!")


class StandardBurger(Burger):
    def prepare(self):
        print("Preparing Standard Burger with bun, patty, cheese, and lettuce!")


class PremiumBurger(Burger):
    def prepare(self):
        print("Preparing Premium Burger with gourmet bun, premium patty, cheese, lettuce, and secret sauce!")


class BasicWheatBurger(Burger):
    def prepare(self):
        print("Preparing Basic Wheat Burger with bun, patty, and ketchup!")


class StandardWheatBurger(Burger):
    def prepare(self):
        print("Preparing Standard Wheat Burger with bun, patty, cheese, and lettuce!")


class PremiumWheatBurger(Burger):
    def prepare(self):
        print("Preparing Premium Wheat Burger with gourmet bun, premium patty, cheese, lettuce, and secret sauce!")


# Factory Interface and Concrete Factories
class BurgerFactory(ABC):
    @abstractmethod
    def createBurger(self, type):
        pass


class SinghBurger(BurgerFactory):
    def createBurger(self, type):
        if type.lower() == "basic":
            return BasicBurger()
        elif type.lower() == "standard":
            return StandardBurger()
        elif type.lower() == "premium":
            return PremiumBurger()
        else:
            print("Invalid burger type!")
            return None


class KingBurger(BurgerFactory):
    def createBurger(self, type):
        if type.lower() == "basic":
            return BasicWheatBurger()
        elif type.lower() == "standard":
            return StandardWheatBurger()
        elif type.lower() == "premium":
            return PremiumWheatBurger()
        else:
            print("Invalid burger type!")
            return None


# Main Class
class FactoryMethod:
    @staticmethod
    def main(args):
        type = "basic"

        myFactory = SinghBurger()
        burger = myFactory.createBurger(type)

        if burger is not None:
            burger.prepare()


if __name__ == "__main__":
    # call the same demo as Java main
    FactoryMethod.main(None)
