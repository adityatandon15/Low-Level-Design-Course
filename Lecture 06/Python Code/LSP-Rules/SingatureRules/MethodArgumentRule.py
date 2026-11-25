# Method Argument Rule :
# Subtype method arguments can be identical or wider than the supertype
# Java enforces this by requiring the same method signature for overrides

class Parent:
    def print(self, msg):
        print("Parent: " + msg)


class Child(Parent):
    def print(self, msg):
        print("Child: " + msg)


# Client that passes a String msg as the client expects.
class Client:
    def __init__(self, p):
        self._p = p

    def printMsg(self):
        self._p.print("Hello")


class MethodArgumentRule:
    @staticmethod
    def main(args):
        parent = Parent()
        child = Child()

        client = Client(parent)
        # Client client = new Client(child);

        client.printMsg()


if __name__ == "__main__":
    # call the same demo as Java main
    MethodArgumentRule.main(None)
