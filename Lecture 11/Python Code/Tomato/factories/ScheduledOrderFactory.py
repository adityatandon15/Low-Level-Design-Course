from ..models.DeliveryOrder import DeliveryOrder
from ..models.PickupOrder import PickupOrder
from .OrderFactory import OrderFactory


class ScheduledOrderFactory(OrderFactory):
    def __init__(self, scheduleTime):
        self._scheduleTime = scheduleTime

    def createOrder(self, user, cart, restaurant, menuItems,
                    paymentStrategy, totalCost, orderType):
        order = None

        if orderType == "Delivery":
            deliveryOrder = DeliveryOrder()
            deliveryOrder.setUserAddress(user.getAddress())
            order = deliveryOrder
        else:
            pickupOrder = PickupOrder()
            pickupOrder.setRestaurantAddress(restaurant.getLocation())
            order = pickupOrder

        order.setUser(user)
        order.setRestaurant(restaurant)
        order.setItems(menuItems)
        order.setPaymentStrategy(paymentStrategy)
        order.setScheduled(self._scheduleTime)
        order.setTotal(totalCost)
        return order
