from .PaymentStrategy import PaymentStrategy


class UpiPaymentStrategy(PaymentStrategy):
    def __init__(self, mob):
        self._mobile = mob

    def pay(self, amount):
        print("Paid ₹" + str(amount) + " using UPI (" + self._mobile + ")")
