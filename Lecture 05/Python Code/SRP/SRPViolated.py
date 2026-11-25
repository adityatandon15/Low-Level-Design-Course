# Product class representing any item of any ECommerce.
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = float(price)


# Violating SRP: ShoppingCart is handling multiple responsibilities
class ShoppingCart:
    def __init__(self):
        self._products = []

    def addProduct(self, p):
        self._products.append(p)

    def getProducts(self):
        return self._products

    # 1. Calculates total price in cart.
    def calculateTotal(self):
        total = 0.0
        for p in self._products:
            total += p.price
        return total

    # 2. Violating SRP - Prints invoice (Should be in a separate class)
    def printInvoice(self):
        print("Shopping Cart Invoice:")
        for p in self._products:
            print(p.name + " - Rs " + str(p.price))
        print("Total: Rs " + str(self.calculateTotal()))

    # 3. Violating SRP - Saves to DB (Should be in a separate class)
    def saveToDatabase(self):
        print("Saving shopping cart to database...")


class SRPViolated:
    @staticmethod
    def main(args):
        cart = ShoppingCart()

        cart.addProduct(Product("Laptop", 50000))
        cart.addProduct(Product("Mouse", 2000))

        cart.printInvoice()
        cart.saveToDatabase()


if __name__ == "__main__":
    # call the same demo as Java main
    SRPViolated.main(None)
