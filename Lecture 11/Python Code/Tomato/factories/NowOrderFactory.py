from ..models.DeliveryOrder import DeliveryOrder
from ..models.PickupOrder import PickupOrder
from ..utils.TimeUtils import TimeUtils
from .OrderFactory import OrderFactory


class NowOrderFactory(OrderFactory):
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
        order.setScheduled(TimeUtils.getCurrentTime())
        order.setTotal(totalCost)
        return order
