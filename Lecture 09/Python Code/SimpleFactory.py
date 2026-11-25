from abc import ABC, abstractmethod

# --- Burger Interface ---
class Burger(ABC):
    @abstractmethod
    def prepare(self):
        pass


# --- Concrete Burger Implementations ---
class BasicBurger(Burger):
    def prepare(self):
        print("Preparing Basic Burger with bun, patty, and ketchup!")


class StandardBurger(Burger):
    def prepare(self):
        print("Preparing Standard Burger with bun, patty, cheese, and lettuce!")


class PremiumBurger(Burger):
    def prepare(self):
        print("Preparing Premium Burger with gourmet bun, premium patty, cheese, lettuce, and secret sauce!")


# --- Burger Factory ---
class BurgerFactory:
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


# --- Main Class ---
class SimpleFactory:
    @staticmethod
    def main(args):
        type = "standard"

        myBurgerFactory = BurgerFactory()

        burger = myBurgerFactory.createBurger(type)

        if burger is not None:
            burger.prepare()


if __name__ == "__main__":
    # call the same demo as Java main
    SimpleFactory.main(None)
