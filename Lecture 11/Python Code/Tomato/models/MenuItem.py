class MenuItem:
    def __init__(self, code, name, price):
        self._code = code
        self._name = name
        self._price = price

    def getCode(self):
        return self._code

    def setCode(self, c):
        self._code = c

    def getName(self):
        return self._name

    def setName(self, n):
        self._name = n

    def getPrice(self):
        return self._price

    def setPrice(self, p):
        self._price = p
