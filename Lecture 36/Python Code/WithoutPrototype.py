# Simple NPC class — no Prototype
class NPC:
    def __init__(self, name, health, attack, defense):
        # call database
        # complex calc
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        print("Creating NPC '" + name + "' [HP:" + str(health) + ", ATK:"
              + str(attack) + ", DEF:" + str(defense) + "]")

    def describe(self):
        print("  NPC: " + self.name + " | HP=" + str(self.health) + " ATK=" + str(self.attack)
              + " DEF=" + str(self.defense))


class WithoutPrototype:
    @staticmethod
    def main(args=None):
        # Base Alien
        alien = NPC("Alien", 30, 5, 2)
        alien.describe()

        # Powerful Alien — must re-pass all stats, easy to make mistakes
        alien2 = NPC("Powerful Alien", 30, 5, 5)
        alien2.describe()

        # If you want 100 aliens, you'd repeat this 100 times…


if __name__ == "__main__":
    WithoutPrototype.main()
