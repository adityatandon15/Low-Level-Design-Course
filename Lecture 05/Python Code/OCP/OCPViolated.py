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


# 3. ShoppingCartStorage: Only responsible for saving cart to DB
class ShoppingCartStorage:
    def __init__(self, cart):
        self._cart = cart

    def saveToSQLDatabase(self):
        print("Saving shopping cart to SQL DB...")

    def saveToMongoDatabase(self):
        print("Saving shopping cart to Mongo DB...")

    def saveToFile(self):
        print("Saving shopping cart to File...")


class OCPViolated:
    @staticmethod
    def main(args):
        cart = ShoppingCart()

        cart.addProduct(Product("Laptop", 50000))
        cart.addProduct(Product("Mouse", 2000))

        printer = ShoppingCartPrinter(cart)
        printer.printInvoice()

        db = ShoppingCartStorage(cart)
        db.saveToSQLDatabase()


if __name__ == "__main__":
    # call the same demo as Java main
    OCPViolated.main(None)
