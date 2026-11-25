import sys


class Cart:
    def __init__(self):
        self._restaurant = None
        self._items = []

    def addItem(self, item):
        if self._restaurant is None:
            print("Cart: Set a restaurant before adding items.", file=sys.stderr)
            return
        self._items.append(item)

    def getTotalCost(self):
        sum = 0.0
        for it in self._items:
            sum += it.getPrice()
        return sum

    def isEmpty(self):
        return self._restaurant is None or len(self._items) == 0

    def clear(self):
        self._items.clear()
        self._restaurant = None

    def setRestaurant(self, r):
        self._restaurant = r

    def getRestaurant(self):
        return self._restaurant

    def getItems(self):
        return self._items
