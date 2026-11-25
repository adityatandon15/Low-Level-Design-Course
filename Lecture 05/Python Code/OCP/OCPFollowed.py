from abc import ABC, abstractmethod

# Product class representing any item in eCommerce.
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = float(price)


# 1. ShoppingCart: Only responsible for Cart related business logic.
class ShoppingCart:
    def __init__(self):
        self._products = []

    def addProduct(self, p):
        self._products.append(p)

    def getProducts(self):
        return self._products

    # Calculates total price in cart.
    def calculateTotal(self):
        total = 0.0
        for p in self._products:
            total += p.price
        return total


# 2. ShoppingCartPrinter: Only responsible for printing invoices
class ShoppingCartPrinter:
    def __init__(self, cart):
        self._cart = cart

    def printInvoice(self):
        print("Shopping Cart Invoice:")
        for p in self._cart.getProducts():
            print(p.name + " - Rs " + str(p.price))
        print("Total: Rs " + str(self._cart.calculateTotal()))


class Persistence(ABC):
    @abstractmethod
    def save(self, cart):
        pass


class SQLPersistence(Persistence):
    def save(self, cart):
        print("Saving shopping cart to SQL DB...")


class MongoPersistence(Persistence):
    def save(self, cart):
        print("Saving shopping cart to MongoDB...")


class FilePersistence(Persistence):
    def save(self, cart):
        print("Saving shopping cart to a file...")


class OCPFollowed:
    @staticmethod
    def main(args):
        cart = ShoppingCart()
        cart.addProduct(Product("Laptop", 50000))
        cart.addProduct(Product("Mouse", 2000))

        printer = ShoppingCartPrinter(cart)
        printer.printInvoice()

        db = SQLPersistence()
        mongo = MongoPersistence()
        file = FilePersistence()

        db.save(cart)     # Save to SQL database
        mongo.save(cart)  # Save to MongoDB
        file.save(cart)   # Save to File


if __name__ == "__main__":
    # call the same demo as Java main
    OCPFollowed.main(None)
