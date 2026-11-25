from .Order import Order


class PickupOrder(Order):
    def __init__(self):
        super().__init__()
        self._restaurantAddress = ""

    def getType(self):
        return "Pickup"

    def setRestaurantAddress(self, addr):
        self._restaurantAddress = addr

    def getRestaurantAddress(self):
        return self._restaurantAddress

    # Implement remaining Order methods with actual fields
