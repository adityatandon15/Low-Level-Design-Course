from .factories.NowOrderFactory import NowOrderFactory
from .factories.ScheduledOrderFactory import ScheduledOrderFactory
from .managers.OrderManager import OrderManager
from .managers.RestaurantManager import RestaurantManager
from .models.MenuItem import MenuItem
from .models.Restaurant import Restaurant
from .services.NotificationService import NotificationService


class TomatoApp:

    def __init__(self):
        self.initializeRestaurants()

    def initializeRestaurants(self):
        restaurant1 = Restaurant("Bikaner", "Delhi")
        restaurant1.addMenuItem(MenuItem("P1", "Chole Bhature", 120))
        restaurant1.addMenuItem(MenuItem("P2", "Samosa", 15))

        restaurant2 = Restaurant("Haldiram", "Kolkata")
        restaurant2.addMenuItem(MenuItem("P1", "Raj Kachori", 80))
        restaurant2.addMenuItem(MenuItem("P2", "Pav Bhaji", 100))
        restaurant2.addMenuItem(MenuItem("P3", "Dhokla", 50))

        restaurant3 = Restaurant("Saravana Bhavan", "Chennai")
        restaurant3.addMenuItem(MenuItem("P1", "Masala Dosa", 90))
        restaurant3.addMenuItem(MenuItem("P2", "Idli Vada", 60))
        restaurant3.addMenuItem(MenuItem("P3", "Filter Coffee", 30))

        restaurantManager = RestaurantManager.getInstance()
        restaurantManager.addRestaurant(restaurant1)
        restaurantManager.addRestaurant(restaurant2)
        restaurantManager.addRestaurant(restaurant3)

    def searchRestaurants(self, location):
        return RestaurantManager.getInstance().searchByLocation(location)

    def selectRestaurant(self, user, restaurant):
        cart = user.getCart()
        cart.setRestaurant(restaurant)

    def addToCart(self, user, itemCode):
        restaurant = user.getCart().getRestaurant()
        if restaurant is None:
            print("Please select a restaurant first.")
            return
        for item in restaurant.getMenu():
            if item.getCode() == itemCode:
                user.getCart().addItem(item)
                break

    def checkoutNow(self, user, orderType, paymentStrategy):
        return self.checkout(user, orderType, paymentStrategy, NowOrderFactory())

    def checkoutScheduled(self, user, orderType, paymentStrategy, scheduleTime):
        return self.checkout(user, orderType, paymentStrategy, ScheduledOrderFactory(scheduleTime))

    def checkout(self, user, orderType, paymentStrategy, orderFactory):
        if user.getCart().isEmpty():
            return None

        userCart = user.getCart()
        orderedRestaurant = userCart.getRestaurant()
        itemsOrdered = userCart.getItems()
        totalCost = userCart.getTotalCost()

        order = orderFactory.createOrder(user, userCart, orderedRestaurant, itemsOrdered, paymentStrategy, totalCost, orderType)
        OrderManager.getInstance().addOrder(order)
        return order

    def payForOrder(self, user, order):
        isPaymentSuccess = order.processPayment()

        if isPaymentSuccess:
            NotificationService.notify(order)
            user.getCart().clear()

    def printUserCart(self, user):
        print("Items in cart:")
        print("------------------------------------")
        for item in user.getCart().getItems():
            print(item.getCode() + " : " + item.getName() + " : ₹" + str(item.getPrice()))
        print("------------------------------------")
        print("Grand total : ₹" + str(user.getCart().getTotalCost()))
