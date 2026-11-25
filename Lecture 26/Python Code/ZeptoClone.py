import math
from abc import ABC, abstractmethod


# Python dict preserves insertion order. java.util.HashMap iterates buckets
# (hash & (capacity - 1)), so the demo's product listing follows that order.
class HashMap(dict):
    def __init__(self):
        super().__init__()
        self._capacity = 0

    def __setitem__(self, key, value):
        isNew = key not in self
        super().__setitem__(key, value)
        if isNew:
            if self._capacity == 0:
                self._capacity = 16
            threshold = int(self._capacity * 0.75)
            if len(self) > threshold:
                self._capacity *= 2

    def _bucket(self, key):
        h = key & 0xFFFFFFFF
        h ^= (h >> 16)
        return h & (self._capacity - 1)

    def entrySet(self):
        if self._capacity == 0 or len(self) == 0:
            return []
        buckets = [[] for _ in range(self._capacity)]
        for key, value in dict.items(self):
            buckets[self._bucket(key)].append((key, value))
        ordered = []
        for bucket in buckets:
            ordered.extend(bucket)
        return ordered


# /////////////////////////////////////////////
# Product & Factory
# /////////////////////////////////////////////

class Product:
    def __init__(self, id, nm, pr):
        self.sku = id
        self.name = nm
        self.price = float(pr)

    # Getters & Setters
    def getSku(self):
        return self.sku

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price


class ProductFactory:
    @staticmethod
    def createProduct(sku):
        # In reality product comes from DB
        if sku == 101:
            name = "Apple"
            price = 20
        elif sku == 102:
            name = "Banana"
            price = 10
        elif sku == 103:
            name = "Chocolate"
            price = 50
        elif sku == 201:
            name = "T-Shirt"
            price = 500
        elif sku == 202:
            name = "Jeans"
            price = 1000
        else:
            name = "Item" + str(sku)
            price = 100
        return Product(sku, name, price)


# /////////////////////////////////////////////
# InventoryStore (Interface) & DbInventoryStore
# /////////////////////////////////////////////

class InventoryStore(ABC):
    @abstractmethod
    def addProduct(self, prod, qty):
        pass

    @abstractmethod
    def removeProduct(self, sku, qty):
        pass

    @abstractmethod
    def checkStock(self, sku):
        pass

    @abstractmethod
    def listAvailableProducts(self):
        pass


class DbInventoryStore(InventoryStore):
    def __init__(self):
        self.stock = HashMap()       # SKU -> quantity
        self.products = HashMap()    # SKU -> Product

    def addProduct(self, prod, qty):
        sku = prod.getSku()
        if sku not in self.products:
            self.products[sku] = prod
        # else drop the extra prod instance
        self.stock[sku] = self.stock.get(sku, 0) + qty

    def removeProduct(self, sku, qty):
        if sku not in self.stock:
            return

        currentQuantity = self.stock[sku]
        remainingQuantity = currentQuantity - qty
        if remainingQuantity > 0:
            self.stock[sku] = remainingQuantity
        else:
            self.stock.pop(sku, None)
            self.products.pop(sku, None)

    def checkStock(self, sku):
        return self.stock.get(sku, 0)

    def listAvailableProducts(self):
        available = []
        for sku, qty in self.stock.entrySet():
            if qty > 0 and sku in self.products:
                available.append(self.products[sku])
        return available


# /////////////////////////////////////////////
# InventoryManager
# /////////////////////////////////////////////

class InventoryManager:
    def __init__(self, store):
        self.store = store

    def addStock(self, sku, qty):
        prod = ProductFactory.createProduct(sku)
        self.store.addProduct(prod, qty)
        print("[InventoryManager] Added SKU " + str(sku) + " Qty " + str(qty))

    def removeStock(self, sku, qty):
        self.store.removeProduct(sku, qty)

    def checkStock(self, sku):
        return self.store.checkStock(sku)

    def getAvailableProducts(self):
        return self.store.listAvailableProducts()


# /////////////////////////////////////////////
# Replenishment Strategy (Strategy Pattern)
# /////////////////////////////////////////////

class ReplenishStrategy(ABC):
    @abstractmethod
    def replenish(self, manager, itemsToReplenish):
        pass


class ThresholdReplenishStrategy(ReplenishStrategy):
    def __init__(self, threshold):
        self.threshold = threshold

    def replenish(self, manager, itemsToReplenish):
        print("[ThresholdReplenish] Checking threshold...")
        entries = itemsToReplenish.entrySet() if isinstance(itemsToReplenish, HashMap) else list(itemsToReplenish.items())
        for sku, qtyToAdd in entries:
            current = manager.checkStock(sku)
            if current < self.threshold:
                manager.addStock(sku, qtyToAdd)
                print("  -> SKU " + str(sku) + " was " + str(current)
                      + ", replenished by " + str(qtyToAdd))


class WeeklyReplenishStrategy(ReplenishStrategy):
    def __init__(self):
        pass

    def replenish(self, manager, itemsToReplenish):
        print("[WeeklyReplenish] Weekly replenishment triggered for inventory.")


# /////////////////////////////////////////////
# DarkStore (formerly Warehouse)
# /////////////////////////////////////////////

class DarkStore:
    def __init__(self, n, x_coord, y_coord):
        self.name = n
        self.x = x_coord
        self.y = y_coord
        self.replenishStrategy = None

        # We could have made another factory called InventoryStoreFactory to get
        # DbInventoryStore by enum and hence make it loosely coupled.
        self.inventoryManager = InventoryManager(DbInventoryStore())

    def distanceTo(self, ux, uy):
        return math.sqrt((self.x - ux) * (self.x - ux) + (self.y - uy) * (self.y - uy))

    def runReplenishment(self, itemsToReplenish):
        if self.replenishStrategy is not None:
            self.replenishStrategy.replenish(self.inventoryManager, itemsToReplenish)

    # Delegation Methods
    def getAllProducts(self):
        return self.inventoryManager.getAvailableProducts()

    def checkStock(self, sku):
        return self.inventoryManager.checkStock(sku)

    def removeStock(self, sku, qty):
        self.inventoryManager.removeStock(sku, qty)

    def addStock(self, sku, qty):
        self.inventoryManager.addStock(sku, qty)

    # Getters & Setters
    def setReplenishStrategy(self, strategy):
        self.replenishStrategy = strategy

    def getName(self):
        return self.name

    def getXCoordinate(self):
        return self.x

    def getYCoordinate(self):
        return self.y

    def getInventoryManager(self):
        return self.inventoryManager


# /////////////////////////////////////////////
# DarkStoreManager (Singleton)
# /////////////////////////////////////////////

class DarkStoreManager:
    _instance = None

    def __init__(self):
        self.darkStores = []

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def registerDarkStore(self, ds):
        self.darkStores.append(ds)

    def getNearbyDarkStores(self, ux, uy, maxDistance):
        distList = []
        for ds in self.darkStores:
            d = ds.distanceTo(ux, uy)
            if d <= maxDistance:
                distList.append(Pair(d, ds))
        distList.sort(key=lambda p: p.getKey())
        result = []
        for p in distList:
            result.append(p.getValue())
        return result


# Simple helper Pair class (since JavaFX/Android Pair might not be available)
class Pair:
    def __init__(self, k, v):
        self.key = k
        self.value = v

    def getKey(self):
        return self.key

    def getValue(self):
        return self.value


# /////////////////////////////////////////////
# User & Cart
# /////////////////////////////////////////////

class Cart:
    def __init__(self):
        self.items = []

    def addItem(self, sku, qty):
        prod = ProductFactory.createProduct(sku)
        self.items.append(Pair(prod, qty))
        print("[Cart] Added SKU " + str(sku) + " (" + prod.getName()
              + ") x" + str(qty))

    def getTotal(self):
        total = 0.0
        for it in self.items:
            total += (it.getKey().getPrice() * it.getValue())
        return total

    def getItems(self):
        return self.items


class User:
    def __init__(self, n, x_coord, y_coord):
        self.name = n
        self.x = x_coord
        self.y = y_coord
        self.cart = Cart()  # User owns a cart

    def getCart(self):
        return self.cart


# /////////////////////////////////////////////
# DeliveryPartner
# /////////////////////////////////////////////

class DeliveryPartner:
    def __init__(self, n):
        self.name = n


# /////////////////////////////////////////////
# Order & OrderManager (Singleton)
# /////////////////////////////////////////////

class Order:
    nextId = 1

    def __init__(self, u):
        self.orderId = Order.nextId
        Order.nextId += 1
        self.user = u
        self.items = []
        self.partners = []
        self.totalAmount = 0.0


class OrderManager:
    _instance = None

    def __init__(self):
        self.orders = []

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def placeOrder(self, user, cart):
        print("\n[OrderManager] Placing Order for: " + user.name)

        requestedItems = cart.getItems()

        # 1) Find nearby dark stores within 5 KM
        maxDist = 5.0
        nearbyDarkStores = DarkStoreManager.getInstance().getNearbyDarkStores(user.x, user.y, maxDist)

        if len(nearbyDarkStores) == 0:
            print("  No dark stores within 5 KM. Cannot fulfill order.")
            return

        # 2) Check if closest store has all items
        firstStore = nearbyDarkStores[0]
        allInFirst = True
        for item in requestedItems:
            sku = item.getKey().getSku()
            qty = item.getValue()
            if firstStore.checkStock(sku) < qty:
                allInFirst = False
                break

        order = Order(user)

        # One delivery partner required...
        if allInFirst:
            print("  All items at: " + firstStore.getName())

            for item in requestedItems:
                sku = item.getKey().getSku()
                qty = item.getValue()
                firstStore.removeStock(sku, qty)
                order.items.append(Pair(item.getKey(), qty))

            order.totalAmount = cart.getTotal()
            order.partners.append(DeliveryPartner("Partner1"))
            print("  Assigned Delivery Partner: Partner1")

        # Multiple delivery partners required
        else:
            print("  Splitting order across stores...")
            allItems = HashMap()
            for item in requestedItems:
                allItems[item.getKey().getSku()] = item.getValue()

            partnerId = 1
            for store in nearbyDarkStores:
                if len(allItems) == 0:
                    break
                print("   Checking: " + store.getName())
                toErase = []
                for sku, qtyNeeded in allItems.entrySet():
                    availableQty = store.checkStock(sku)
                    if availableQty <= 0:
                        continue
                    takenQty = min(availableQty, qtyNeeded)
                    store.removeStock(sku, takenQty)
                    print("     " + store.getName() + " supplies SKU " + str(sku)
                          + " x" + str(takenQty))
                    order.items.append(Pair(ProductFactory.createProduct(sku), takenQty))
                    if qtyNeeded > takenQty:
                        allItems[sku] = qtyNeeded - takenQty
                    else:
                        toErase.append(sku)
                for sku in toErase:
                    allItems.pop(sku, None)
                if len(toErase) > 0:
                    pname = "Partner" + str(partnerId)
                    partnerId += 1
                    order.partners.append(DeliveryPartner(pname))
                    print("     Assigned: " + pname + " for " + store.getName())

            if len(allItems) > 0:
                print("  Could not fulfill:")
                for sku, qty in allItems.entrySet():
                    print("    SKU " + str(sku)
                          + " x" + str(qty))

            totalSum = 0.0
            for it in order.items:
                totalSum += it.getKey().getPrice() * it.getValue()
            order.totalAmount = totalSum

        # Printing Order Summary
        print("\n[OrderManager] Order #" + str(order.orderId) + " Summary:")
        print("  User: " + user.name + "\n  Items:")
        for item in order.items:
            print("    SKU " + str(item.getKey().getSku())
                  + " (" + item.getKey().getName() + ") x" + str(item.getValue())
                  + " @ ₹" + str(item.getKey().getPrice()))
        print("  Total: ₹" + str(order.totalAmount) + "\n  Partners:")
        for dp in order.partners:
            print("    " + dp.name)
        print()

        self.orders.append(order)

    def getAllOrders(self):
        return self.orders


# /////////////////////////////////////////////
# Zepto Initialization & Main
# /////////////////////////////////////////////

class ZeptoHelper:
    @staticmethod
    def showAllItems(user):
        print("\n[Zepto] All Available products within 5 KM for " + user.name + ":")
        dsManager = DarkStoreManager.getInstance()
        nearbyStores = dsManager.getNearbyDarkStores(user.x, user.y, 5.0)
        skuToPrice = HashMap()
        skuToName = HashMap()

        for ds in nearbyStores:
            for product in ds.getAllProducts():
                sku = product.getSku()
                if sku not in skuToPrice:
                    skuToPrice[sku] = product.getPrice()
                    skuToName[sku] = product.getName()

        for sku, price in skuToPrice.entrySet():
            print("  SKU " + str(sku) + " - "
                  + skuToName[sku]
                  + " @ ₹" + str(price))

    @staticmethod
    def initialize():
        dsManager = DarkStoreManager.getInstance()

        # DarkStore A.......
        darkStoreA = DarkStore("DarkStoreA", 0.0, 0.0)
        darkStoreA.setReplenishStrategy(ThresholdReplenishStrategy(3))
        print("\nAdding stocks in DarkStoreA....")
        darkStoreA.addStock(101, 5)
        darkStoreA.addStock(102, 2)

        # DarkStore B.......
        darkStoreB = DarkStore("DarkStoreB", 4.0, 1.0)
        darkStoreB.setReplenishStrategy(ThresholdReplenishStrategy(3))
        print("\nAdding stocks in DarkStoreB....")
        darkStoreB.addStock(101, 3)
        darkStoreB.addStock(103, 10)

        # DarkStore C.......
        darkStoreC = DarkStore("DarkStoreC", 2.0, 3.0)
        darkStoreC.setReplenishStrategy(ThresholdReplenishStrategy(3))
        print("\nAdding stocks in DarkStoreC....")
        darkStoreC.addStock(102, 5)
        darkStoreC.addStock(201, 7)

        dsManager.registerDarkStore(darkStoreA)
        dsManager.registerDarkStore(darkStoreB)
        dsManager.registerDarkStore(darkStoreC)


class ZeptoClone:
    @staticmethod
    def main(args):
        # 1) Initialize.
        ZeptoHelper.initialize()

        # 2) A User comes on Platform
        user = User("Aditya", 1.0, 1.0)
        print("\nUser with name " + user.name + " comes on platform")

        # 3) Show all available items via Zepto
        ZeptoHelper.showAllItems(user)

        # 4) User adds items to cart
        print("\nAdding items to cart")
        cart = user.getCart()
        cart.addItem(101, 4)
        cart.addItem(102, 3)
        cart.addItem(103, 2)

        # 5) Place Order
        OrderManager.getInstance().placeOrder(user, cart)

        print("\n=== Demo Complete ===")


if __name__ == "__main__":
    ZeptoClone.main([])
