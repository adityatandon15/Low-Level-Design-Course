from abc import ABC, abstractmethod


class OrderFactory(ABC):
    @abstractmethod
    def createOrder(self, user, cart, restaurant, menuItems,
                    paymentStrategy, totalCost, orderType):
        pass
