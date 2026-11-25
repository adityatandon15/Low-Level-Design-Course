class NotificationService:
    @staticmethod
    def notify(order):
        print("\nNotification: New " + order.getType() + " order placed!")
        print("---------------------------------------------")
        print("Order ID: " + str(order.getOrderId()))
        print("Customer: " + order.getUser().getName())
        print("Restaurant: " + order.getRestaurant().getName())
        print("Items Ordered:")

        items = order.getItems()
        for item in items:
            print("   - " + item.getName() + " (₹" + str(item.getPrice()) + ")")

        print("Total: ₹" + str(order.getTotal()))
        print("Scheduled For: " + order.getScheduled())
        print("Payment: Done")
        print("---------------------------------------------")
