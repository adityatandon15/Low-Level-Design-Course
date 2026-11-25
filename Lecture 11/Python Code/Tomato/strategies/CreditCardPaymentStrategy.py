from .PaymentStrategy import PaymentStrategy


class CreditCardPaymentStrategy(PaymentStrategy):
    def __init__(self, card):
        self._cardNumber = card

    def pay(self, amount):
        print("Paid ₹" + str(amount) + " using Credit Card (" + self._cardNumber + ")")
