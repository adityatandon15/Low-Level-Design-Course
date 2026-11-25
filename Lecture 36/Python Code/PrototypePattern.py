from abc import ABC, abstractmethod


# Cloneable (aka Prototype) interface
class Cloneable(ABC):
    @abstractmethod
    def clone(self):
        pass


class NPC(Cloneable):
    def __init__(self, name, health, attack, defense):
        # call database
        # complex calc
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        print("Setting up template NPC '" + name + "'")

    # the clone method required by Prototype
    # copy-ctor used by clone(): field-by-field copy, does not rerun the heavy constructor
    def clone(self):
        cloned = NPC.__new__(NPC)
        cloned.name = self.name
        cloned.health = self.health
        cloned.attack = self.attack
        cloned.defense = self.defense
        print("Cloning NPC '" + cloned.name + "'")
        return cloned

    def describe(self):
        print("NPC " + self.name + " [HP=" + str(self.health) + " ATK=" + str(self.attack)
              + " DEF=" + str(self.defense) + "]")

    # setters to tweak the clone…
    def setName(self, n):
        self.name = n

    def setHealth(self, h):
        self.health = h

    def setAttack(self, a):
        self.attack = a

    def setDefense(self, d):
        self.defense = d


class PrototypePattern:
    @staticmethod
    def main(args=None):
        # 1) build one "heavy" template
        alien = NPC("Alien", 30, 5, 2)

        # 2) quickly clone + tweak as many variants as you like:
        alienCopied1 = alien.clone()
        alienCopied1.describe()

        alienCopied2 = alien.clone()
        alienCopied2.setName("Powerful Alien")
        alienCopied2.setHealth(50)
        alienCopied2.describe()

        # cleanup
        alien = None
        alienCopied1 = None
        alienCopied2 = None


if __name__ == "__main__":
    PrototypePattern.main()
