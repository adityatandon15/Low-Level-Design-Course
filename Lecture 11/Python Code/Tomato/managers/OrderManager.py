class OrderManager:
    _instance = None

    def __init__(self):
        # Private Constructor
        self._orders = []

    @staticmethod
    def getInstance():
        if OrderManager._instance is None:
            OrderManager._instance = OrderManager()
        return OrderManager._instance

    def addOrder(self, order):
        self._orders.append(order)

    def listOrders(self):
        print("\n--- All Orders ---")
        for order in self._orders:
            print(order.getType() + " order for " + order.getUser().getName()
                  + " | Total: ₹" + str(order.getTotal())
                  + " | At: " + order.getScheduled())
