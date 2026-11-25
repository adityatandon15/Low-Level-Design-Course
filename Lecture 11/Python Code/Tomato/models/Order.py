from abc import ABC, abstractmethod


class Order(ABC):
    _nextOrderId = 0

    def __init__(self):
        self.user = None
        self.restaurant = None
        self.paymentStrategy = None
        self.total = 0.0
        self.scheduled = ""
        self.items = None
        Order._nextOrderId += 1
        self.orderId = Order._nextOrderId

    def processPayment(self):
        if self.paymentStrategy is not None:
            self.paymentStrategy.pay(self.total)
            return True
        else:
            print("Please choose a payment mode first")
            return False

    @abstractmethod
    def getType(self):
        pass

    # Getters and Setters
    def getOrderId(self):
        return self.orderId

    def setUser(self, u):
        self.user = u

    def getUser(self):
        return self.user

    def setRestaurant(self, r):
        self.restaurant = r

    def getRestaurant(self):
        return self.restaurant

    def setItems(self, its):
        self.items = its
        self.total = 0.0
        for i in self.items:
            self.total += i.getPrice()

    def getItems(self):
        return self.items

    def setPaymentStrategy(self, p):
        self.paymentStrategy = p

    def setScheduled(self, s):
        self.scheduled = s

    def getScheduled(self):
        return self.scheduled

    def getTotal(self):
        return self.total

    def setTotal(self, total):
        self.total = total
