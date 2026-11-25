from .Cart import Cart


class User:
    def __init__(self, userId, name, address):
        self._userId = userId
        self._name = name
        self._address = address
        self._cart = Cart()

    def getName(self):
        return self._name

    def setName(self, n):
        self._name = n

    def getAddress(self):
        return self._address

    def setAddress(self, a):
        self._address = a

    def getCart(self):
        return self._cart
