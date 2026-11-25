import threading
from abc import ABC, abstractmethod
from enum import Enum


# ----------------------------
# Discount Strategy (Strategy Pattern)
# ----------------------------
class DiscountStrategy(ABC):
    @abstractmethod
    def calculate(self, baseAmount):
        pass


class FlatDiscountStrategy(DiscountStrategy):
    def __init__(self, amt):
        self.amount = float(amt)

    def calculate(self, baseAmount):
        return min(self.amount, baseAmount)


class PercentageDiscountStrategy(DiscountStrategy):
    def __init__(self, pct):
        self.percent = float(pct)

    def calculate(self, baseAmount):
        return (self.percent / 100.0) * baseAmount


class PercentageWithCapStrategy(DiscountStrategy):
    def __init__(self, pct, capVal):
        self.percent = float(pct)
        self.cap = float(capVal)

    def calculate(self, baseAmount):
        disc = (self.percent / 100.0) * baseAmount
        return self.cap if disc > self.cap else disc


class StrategyType(Enum):
    FLAT = 1
    PERCENT = 2
    PERCENT_WITH_CAP = 3


# ----------------------------
# DiscountStrategyManager (Singleton)
# ----------------------------
class DiscountStrategyManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        pass

    @classmethod
    def getInstance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def getStrategy(self, type, param1, param2):
        if type == StrategyType.FLAT:
            return FlatDiscountStrategy(param1)
        elif type == StrategyType.PERCENT:
            return PercentageDiscountStrategy(param1)
        elif type == StrategyType.PERCENT_WITH_CAP:
            return PercentageWithCapStrategy(param1, param2)
        else:
            return None


# ----------------------------
# Assume existing Cart and Product classes
# ----------------------------
class Product:
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = float(price)

    def getName(self):
        return self.name

    def getCategory(self):
        return self.category

    def getPrice(self):
        return self.price


class CartItem:
    def __init__(self, prod, qty):
        self.product = prod
        self.quantity = qty

    def itemTotal(self):
        return self.product.getPrice() * self.quantity

    def getProduct(self):
        return self.product


class Cart:
    def __init__(self):
        self.items = []
        self.originalTotal = 0.0
        self.currentTotal = 0.0
        self.loyaltyMember = False
        self.paymentBank = ""

    def addProduct(self, prod, qty):
        item = CartItem(prod, qty)
        self.items.append(item)
        self.originalTotal += item.itemTotal()
        self.currentTotal += item.itemTotal()

    def getOriginalTotal(self):
        return self.originalTotal

    def getCurrentTotal(self):
        return self.currentTotal

    def applyDiscount(self, d):
        self.currentTotal -= d
        if self.currentTotal < 0:
            self.currentTotal = 0.0

    def setLoyaltyMember(self, member):
        self.loyaltyMember = member

    def isLoyaltyMember(self):
        return self.loyaltyMember

    def setPaymentBank(self, bank):
        self.paymentBank = bank

    def getPaymentBank(self):
        return self.paymentBank

    def getItems(self):
        return self.items


# ----------------------------
# Coupon base class (Chain of Responsibility)
# ----------------------------
class Coupon(ABC):
    def __init__(self):
        self.next = None

    def setNext(self, nxt):
        self.next = nxt

    def getNext(self):
        return self.next

    def applyDiscount(self, cart):
        if self.isApplicable(cart):
            discount = self.getDiscount(cart)
            cart.applyDiscount(discount)
            print(self.name() + " applied: " + str(discount))
            if not self.isCombinable():
                return
        if self.next is not None:
            self.next.applyDiscount(cart)

    @abstractmethod
    def isApplicable(self, cart):
        pass

    @abstractmethod
    def getDiscount(self, cart):
        pass

    def isCombinable(self):
        return True

    @abstractmethod
    def name(self):
        pass


# ----------------------------
# Concrete Coupons
# ----------------------------
class SeasonalOffer(Coupon):
    def __init__(self, pct, cat):
        super().__init__()
        self.percent = pct
        self.category = cat
        self.strat = DiscountStrategyManager.getInstance().getStrategy(StrategyType.PERCENT, self.percent, 0.0)

    def isApplicable(self, cart):
        for item in cart.getItems():
            if item.getProduct().getCategory() == self.category:
                return True
        return False

    def getDiscount(self, cart):
        subtotal = 0.0
        for item in cart.getItems():
            if item.getProduct().getCategory() == self.category:
                subtotal += item.itemTotal()
        return self.strat.calculate(subtotal)

    def name(self):
        return "Seasonal Offer " + str(int(self.percent)) + "% off " + self.category


class LoyaltyDiscount(Coupon):
    def __init__(self, pct):
        super().__init__()
        self.percent = pct
        self.strat = DiscountStrategyManager.getInstance().getStrategy(StrategyType.PERCENT, self.percent, 0.0)

    def isApplicable(self, cart):
        return cart.isLoyaltyMember()

    def getDiscount(self, cart):
        return self.strat.calculate(cart.getCurrentTotal())

    def name(self):
        return "Loyalty Discount " + str(int(self.percent)) + "% off"


class BulkPurchaseDiscount(Coupon):
    def __init__(self, thr, off):
        super().__init__()
        self.threshold = thr
        self.flatOff = off
        self.strat = DiscountStrategyManager.getInstance().getStrategy(StrategyType.FLAT, self.flatOff, 0.0)

    def isApplicable(self, cart):
        return cart.getOriginalTotal() >= self.threshold

    def getDiscount(self, cart):
        return self.strat.calculate(cart.getCurrentTotal())

    def name(self):
        return "Bulk Purchase Rs " + str(int(self.flatOff)) + " off over " + str(int(self.threshold))


class BankingCoupon(Coupon):
    def __init__(self, b, ms, percent, offCap):
        super().__init__()
        self.bank = b
        self.minSpend = ms
        self.percent = percent
        self.offCap = offCap
        self.strat = DiscountStrategyManager.getInstance().getStrategy(
            StrategyType.PERCENT_WITH_CAP, self.percent, self.offCap)

    def isApplicable(self, cart):
        return cart.getPaymentBank() == self.bank and cart.getOriginalTotal() >= self.minSpend

    def getDiscount(self, cart):
        return self.strat.calculate(cart.getCurrentTotal())

    def name(self):
        return self.bank + " Bank Rs " + str(int(self.percent)) + " off upto " + str(int(self.offCap))


# ----------------------------
# CouponManager (Singleton)
# ----------------------------
class CouponManager:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.head = None
        # java.util.concurrent.locks.ReentrantLock
        self.lock = threading.RLock()

    @classmethod
    def getInstance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def registerCoupon(self, coupon):
        self.lock.acquire()
        try:
            if self.head is None:
                self.head = coupon
            else:
                cur = self.head
                while cur.getNext() is not None:
                    cur = cur.getNext()
                cur.setNext(coupon)
        finally:
            self.lock.release()

    def getApplicable(self, cart):
        self.lock.acquire()
        try:
            res = []
            cur = self.head
            while cur is not None:
                if cur.isApplicable(cart):
                    res.append(cur.name())
                cur = cur.getNext()
            return res
        finally:
            self.lock.release()

    def applyAll(self, cart):
        self.lock.acquire()
        try:
            if self.head is not None:
                self.head.applyDiscount(cart)
            return cart.getCurrentTotal()
        finally:
            self.lock.release()


# ----------------------------
# Main: Client code
# ----------------------------
class DiscountCoupon:
    @staticmethod
    def main(args):
        mgr = CouponManager.getInstance()
        mgr.registerCoupon(SeasonalOffer(10, "Clothing"))
        mgr.registerCoupon(LoyaltyDiscount(5))
        mgr.registerCoupon(BulkPurchaseDiscount(1000, 100))
        mgr.registerCoupon(BankingCoupon("ABC", 2000, 15, 500))

        p1 = Product("Winter Jacket", "Clothing", 1000)
        p2 = Product("Smartphone", "Electronics", 20000)
        p3 = Product("Jeans", "Clothing", 1000)
        p4 = Product("Headphones", "Electronics", 2000)

        cart = Cart()
        cart.addProduct(p1, 1)
        cart.addProduct(p2, 1)
        cart.addProduct(p3, 2)
        cart.addProduct(p4, 1)
        cart.setLoyaltyMember(True)
        cart.setPaymentBank("ABC")

        print("Original Cart Total: " + str(cart.getOriginalTotal()) + " Rs")

        applicable = mgr.getApplicable(cart)
        print("Applicable Coupons:")
        for name in applicable:
            print(" - " + name)

        finalTotal = mgr.applyAll(cart)
        print("Final Cart Total after discounts: " + str(finalTotal) + " Rs")


if __name__ == "__main__":
    DiscountCoupon.main([])
