import random
from abc import ABC, abstractmethod
from enum import Enum


# ----------------------------
# Data structure for payment details
# ----------------------------
class PaymentRequest:
    def __init__(self, sender, reciever, amt, curr):
        self.sender = sender
        self.reciever = reciever
        self.amount = amt
        self.currency = curr


# ----------------------------
# Banking System interface and implementations (Strategy for actual payment logic)
# ----------------------------
class BankingSystem(ABC):
    @abstractmethod
    def processPayment(self, amount):
        pass


class PaytmBankingSystem(BankingSystem):
    def __init__(self):
        self.rand = random.Random()

    def processPayment(self, amount):
        # Simulate 20% success
        r = self.rand.randrange(100)
        return r < 80


class RazorpayBankingSystem(BankingSystem):
    def __init__(self):
        self.rand = random.Random()

    def processPayment(self, amount):
        print("[BankingSystem-Razorpay] Processing payment of " + str(amount) + "...")
        # Simulate 90% success
        r = self.rand.randrange(100)
        return r < 90


# ----------------------------
# Abstract base class for Payment Gateway (Template Method Pattern)
# ----------------------------
class PaymentGateway(ABC):
    def __init__(self):
        self.bankingSystem = None

    # Template method defining the standard payment flow
    def processPayment(self, request):
        if not self.validatePayment(request):
            print("[PaymentGateway] Validation failed for " + request.sender + ".")
            return False
        if not self.initiatePayment(request):
            print("[PaymentGateway] Initiation failed for " + request.sender + ".")
            return False
        if not self.confirmPayment(request):
            print("[PaymentGateway] Confirmation failed for " + request.sender + ".")
            return False
        return True

    # Steps to be implemented by concrete gateways
    @abstractmethod
    def validatePayment(self, request):
        pass

    @abstractmethod
    def initiatePayment(self, request):
        pass

    @abstractmethod
    def confirmPayment(self, request):
        pass


# ----------------------------
# Concrete Payment Gateway for Paytm
# ----------------------------
class PaytmGateway(PaymentGateway):
    def __init__(self):
        super().__init__()
        self.bankingSystem = PaytmBankingSystem()

    def validatePayment(self, request):
        print("[Paytm] Validating payment for " + request.sender + ".")
        if request.amount <= 0 or request.currency != "INR":
            return False
        return True

    def initiatePayment(self, request):
        print("[Paytm] Initiating payment of " + str(request.amount)
              + " " + request.currency + " for " + request.sender + ".")
        return self.bankingSystem.processPayment(request.amount)

    def confirmPayment(self, request):
        print("[Paytm] Confirming payment for " + request.sender + ".")
        # Confirmation always succeeds in this simulation
        return True


# ----------------------------
# Concrete Payment Gateway for Razorpay
# ----------------------------
class RazorpayGateway(PaymentGateway):
    def __init__(self):
        super().__init__()
        self.bankingSystem = RazorpayBankingSystem()

    def validatePayment(self, request):
        print("[Razorpay] Validating payment for " + request.sender + ".")
        if request.amount <= 0:
            return False
        return True

    def initiatePayment(self, request):
        print("[Razorpay] Initiating payment of " + str(request.amount)
              + " " + request.currency + " for " + request.sender + ".")
        return self.bankingSystem.processPayment(request.amount)

    def confirmPayment(self, request):
        print("[Razorpay] Confirming payment for " + request.sender + ".")
        # Confirmation always succeeds in this simulation
        return True


# ----------------------------
# Proxy class that wraps a PaymentGateway to add retries (Proxy Pattern)
# ----------------------------
class PaymentGatewayProxy(PaymentGateway):
    def __init__(self, gateway, maxRetries):
        super().__init__()
        self.realGateway = gateway
        self.retries = maxRetries

    def processPayment(self, request):
        result = False
        for attempt in range(self.retries):
            if attempt > 0:
                print("[Proxy] Retrying payment (attempt " + str(attempt + 1)
                      + ") for " + request.sender + ".")
            result = self.realGateway.processPayment(request)
            if result:
                break
        if not result:
            print("[Proxy] Payment failed after " + str(self.retries)
                  + " attempts for " + request.sender + ".")
        return result

    def validatePayment(self, request):
        return self.realGateway.validatePayment(request)

    def initiatePayment(self, request):
        return self.realGateway.initiatePayment(request)

    def confirmPayment(self, request):
        return self.realGateway.confirmPayment(request)


# ----------------------------
# Gateway Factory for creating gateway (Singleton)
# ----------------------------
class GatewayType(Enum):
    PAYTM = 1
    RAZORPAY = 2


class GatewayFactory:
    _instance = None

    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def getGateway(self, type):
        if type == GatewayType.PAYTM:
            paymentGateway = PaytmGateway()
            return PaymentGatewayProxy(paymentGateway, 3)
        else:
            paymentGateway = RazorpayGateway()
            return PaymentGatewayProxy(paymentGateway, 1)


# ----------------------------
# Unified API service (Singleton)
# ----------------------------
class PaymentService:
    _instance = None

    def __init__(self):
        self.gateway = None

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def setGateway(self, g):
        self.gateway = g

    def processPayment(self, request):
        if self.gateway is None:
            print("[PaymentService] No payment gateway selected.")
            return False
        return self.gateway.processPayment(request)


# ----------------------------
# Controller class for all client requests (Singleton)
# ----------------------------
class PaymentController:
    _instance = None

    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def handlePayment(self, type, req):
        paymentGateway = GatewayFactory.getInstance().getGateway(type)
        PaymentService.getInstance().setGateway(paymentGateway)
        return PaymentService.getInstance().processPayment(req)


# ----------------------------
# Main: Client code now goes through controller
# ----------------------------
class PaymentGatewayApplication:
    @staticmethod
    def main(args):
        req1 = PaymentRequest("Aditya", "Shubham", 1000.0, "INR")

        print("Processing via Paytm")
        print("------------------------------")
        res1 = PaymentController.getInstance().handlePayment(GatewayType.PAYTM, req1)
        print("Result: " + ("SUCCESS" if res1 else "FAIL"))
        print("------------------------------\n")

        req2 = PaymentRequest("Shubham", "Aditya", 500.0, "USD")

        print("Processing via Razorpay")
        print("------------------------------")
        res2 = PaymentController.getInstance().handlePayment(GatewayType.RAZORPAY, req2)
        print("Result: " + ("SUCCESS" if res2 else "FAIL"))
        print("------------------------------")


if __name__ == "__main__":
    PaymentGatewayApplication.main([])
