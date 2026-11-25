# Return Type Rule :
# Subtype overridden method return type should be either identical
# or narrower than the parent method's return type.
# This is also called return type covariance.
# Java supports this out of the box.

class Animal:
    # some common Animal methods
    pass


class Dog(Animal):
    # Additional Dog methods specific to Dogs.
    pass


class Parent:
    def getAnimal(self):
        print("Parent : Returning Animal instance")
        return Animal()


class Child(Parent):
    def getAnimal(self):
        print("Child : Returning Dog instance")
        return Dog()


class Client:
    def __init__(self, p):
        self._p = p

    def takeAnimal(self):
        self._p.getAnimal()


class ReturnTypeRule:
    @staticmethod
    def main(args):
        parent = Parent()
        child = Child()

        client = Client(child)
        # Client client = new Client(parent);
        client.takeAnimal()


if __name__ == "__main__":
    # call the same demo as Java main
    ReturnTypeRule.main(None)
