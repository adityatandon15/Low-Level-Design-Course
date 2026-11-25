from abc import ABC, abstractmethod


# Component Interface: defines a common interface for Mario and all power-up decorators.
class Character(ABC):
    @abstractmethod
    def getAbilities(self):
        pass


# Concrete Component: Basic Mario character with no power-ups.
class Mario(Character):
    def getAbilities(self):
        return "Mario"


# Abstract Decorator: CharacterDecorator "is-a" Character and "has-a" Character.
class CharacterDecorator(Character):
    def __init__(self, c):
        self.character = c  # Wrapped component


# Concrete Decorator: Height-Increasing Power-Up.
class HeightUp(CharacterDecorator):
    def __init__(self, c):
        super().__init__(c)

    def getAbilities(self):
        return self.character.getAbilities() + " with HeightUp"


# Concrete Decorator: Gun Shooting Power-Up.
class GunPowerUp(CharacterDecorator):
    def __init__(self, c):
        super().__init__(c)

    def getAbilities(self):
        return self.character.getAbilities() + " with Gun"


# Concrete Decorator: Star Power-Up (temporary ability).
class StarPowerUp(CharacterDecorator):
    def __init__(self, c):
        super().__init__(c)

    def getAbilities(self):
        return self.character.getAbilities() + " with Star Power (Limited Time)"


class DecoratorPattern:
    @staticmethod
    def main(args=None):
        # Create a basic Mario character.
        mario = Mario()
        print("Basic Character: " + mario.getAbilities())

        # Decorate Mario with a HeightUp power-up.
        mario = HeightUp(mario)
        print("After HeightUp: " + mario.getAbilities())

        # Decorate Mario further with a GunPowerUp.
        mario = GunPowerUp(mario)
        print("After GunPowerUp: " + mario.getAbilities())

        # Finally, add a StarPowerUp decoration.
        mario = StarPowerUp(mario)
        print("After StarPowerUp: " + mario.getAbilities())


if __name__ == "__main__":
    DecoratorPattern.main()
