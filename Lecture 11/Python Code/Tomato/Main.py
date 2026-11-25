from .TomatoApp import TomatoApp
from .models.User import User
from .strategies.UpiPaymentStrategy import UpiPaymentStrategy


class Main:
    @staticmethod
    def main(args=None):
        # Simulating a happy flow
        # Create TomatoApp Object
        tomato = TomatoApp()

        # Simulate a user coming in (Happy Flow)
        user = User(101, "Aditya", "Delhi")
        print("User: " + user.getName() + " is active.")

        # User searches for restaurants by location
        restaurantList = tomato.searchRestaurants("Delhi")

        if len(restaurantList) == 0:
            print("No restaurants found!")
            return

        print("Found Restaurants:")
        for restaurant in restaurantList:
            print(" - " + restaurant.getName())

        # User selects a restaurant
        tomato.selectRestaurant(user, restaurantList[0])
        print("Selected restaurant: " + restaurantList[0].getName())

        # User adds items to the cart
        tomato.addToCart(user, "P1")
        tomato.addToCart(user, "P2")

        tomato.printUserCart(user)

        # User checkout the cart
        order = tomato.checkoutNow(user, "Delivery", UpiPaymentStrategy("1234567890"))

        # User pays for the cart. If payment is successful, notification is sent.
        tomato.payForOrder(user, order)


if __name__ == "__main__":
    Main.main()
