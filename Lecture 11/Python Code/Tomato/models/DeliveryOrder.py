from .Order import Order


class DeliveryOrder(Order):
    def __init__(self):
        super().__init__()
        self._userAddress = ""

    def getType(self):
        return "Delivery"

    def setUserAddress(self, addr):
        self._userAddress = addr

    def getUserAddress(self):
        return self._userAddress

    # Implement remaining Order methods with actual fields
