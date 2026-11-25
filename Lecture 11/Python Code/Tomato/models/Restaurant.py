class Restaurant:
    _nextRestaurantId = 0

    def __init__(self, name, location):
        self._name = name
        self._location = location
        Restaurant._nextRestaurantId += 1
        self._restaurantId = Restaurant._nextRestaurantId
        self._menu = []

    def getName(self):
        return self._name

    def setName(self, n):
        self._name = n

    def getLocation(self):
        return self._location

    def setLocation(self, loc):
        self._location = loc

    def addMenuItem(self, item):
        self._menu.append(item)

    def getMenu(self):
        return self._menu
