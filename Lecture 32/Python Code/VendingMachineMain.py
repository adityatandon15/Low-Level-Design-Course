from abc import ABC, abstractmethod


# Abstract State Interface
class VendingState(ABC):
    @abstractmethod
    def insertCoin(self, machine, coin):
        pass

    @abstractmethod
    def selectItem(self, machine):
        pass

    @abstractmethod
    def dispense(self, machine):
        pass

    @abstractmethod
    def returnCoin(self, machine):
        pass

    @abstractmethod
    def refill(self, machine, quantity):
        pass

    @abstractmethod
    def getStateName(self):
        pass


# Context Class - Vending Machine
class VendingMachine:
    def __init__(self, itemCount, itemPrice):
        self.itemCount = itemCount
        self.itemPrice = itemPrice
        self.insertedCoins = 0

        # Create state objects
        self.noCoinState = NoCoinState()
        self.hasCoinState = HasCoinState()
        self.dispenseState = DispenseState()
        self.soldOutState = SoldOutState()

        # Set initial state
        if itemCount > 0:
            self.currentState = self.noCoinState
        else:
            self.currentState = self.soldOutState

    # Delegate to current state and update state based on return value
    def insertCoin(self, coin):
        self.currentState = self.currentState.insertCoin(self, coin)

    def selectItem(self):
        self.currentState = self.currentState.selectItem(self)

    def dispense(self):
        self.currentState = self.currentState.dispense(self)

    def returnCoin(self):
        self.currentState = self.currentState.returnCoin(self)

    def refill(self, quantity):
        self.currentState = self.currentState.refill(self, quantity)

    # Print the status of Vending Machine
    def printStatus(self):
        print("\n--- Vending Machine Status ---")
        print("Items remaining: " + str(self.itemCount))
        print("Inserted coin: Rs " + str(self.insertedCoins))
        print("Current state: " + self.currentState.getStateName() + "\n")

    # Getters for states
    def getNoCoinState(self):
        return self.noCoinState

    def getHasCoinState(self):
        return self.hasCoinState

    def getDispenseState(self):
        return self.dispenseState

    def getSoldOutState(self):
        return self.soldOutState

    # Data access methods
    def getItemCount(self):
        return self.itemCount

    def decrementItemCount(self):
        self.itemCount -= 1

    def incrementItemCount(self, count=1):
        self.itemCount += count

    def getInsertedCoin(self):
        return self.insertedCoins

    def setInsertedCoin(self, coin):
        self.insertedCoins = coin

    def addCoin(self, coin):
        self.insertedCoins += coin

    def getPrice(self):
        return self.itemPrice

    def setPrice(self, itemPrice):
        self.itemPrice = itemPrice


# Concrete State: No Coin Inserted
class NoCoinState(VendingState):
    def insertCoin(self, machine, coin):
        machine.setInsertedCoin(coin)  # Rs 10
        print("Coin inserted. Current balance: Rs " + str(coin))
        return machine.getHasCoinState()  # Transition to HasCoinState

    def selectItem(self, machine):
        print("Please insert coin first!")
        return machine.getNoCoinState()  # Stay in same state

    def dispense(self, machine):
        print("Please insert coin and select item first!")
        return machine.getNoCoinState()  # Stay in same state

    def returnCoin(self, machine):
        print("No coin to return!")
        return machine.getNoCoinState()  # Stay in same state

    def refill(self, machine, quantity):
        print("Items refilling")
        machine.incrementItemCount(quantity)
        return machine.getNoCoinState()  # Stay in same state

    def getStateName(self):
        return "NO_COIN"


# Concrete State: Coin Inserted
class HasCoinState(VendingState):
    def insertCoin(self, machine, coin):
        machine.addCoin(coin)
        print("Additional coin inserted. Current balance: Rs " + str(machine.getInsertedCoin()))
        return machine.getHasCoinState()  # Stay in same state

    def selectItem(self, machine):
        if machine.getInsertedCoin() >= machine.getPrice():
            print("Item selected. Dispensing...")

            change = machine.getInsertedCoin() - machine.getPrice()
            if change > 0:
                print("Change returned: Rs " + str(change))
            machine.setInsertedCoin(0)

            return machine.getDispenseState()  # Transition to DispenseState
        else:
            needed = machine.getPrice() - machine.getInsertedCoin()
            print("Insufficient funds. Need Rs " + str(needed) + " more.")
            return machine.getHasCoinState()  # Stay in same state

    def dispense(self, machine):
        print("Please select an item first!")
        return machine.getHasCoinState()  # Stay in same state

    def returnCoin(self, machine):
        print("Coin returned: Rs " + str(machine.getInsertedCoin()))
        machine.setInsertedCoin(0)
        return machine.getNoCoinState()  # Transition to NoCoinState

    def refill(self, machine, quantity):
        print("Can't refil in this state")
        return machine.getHasCoinState()  # Stay in same state

    def getStateName(self):
        return "HAS_COIN"


# Concrete State: Item Sold
class DispenseState(VendingState):
    def insertCoin(self, machine, coin):
        print("Please wait, already dispensing item. Coin returned: Rs " + str(coin))
        return machine.getDispenseState()  # Stay in same state

    def selectItem(self, machine):
        print("Already dispensing item. Please wait.")
        return machine.getDispenseState()  # Stay in same state

    def dispense(self, machine):
        print("Item dispensed!")
        machine.decrementItemCount()

        if machine.getItemCount() > 0:
            return machine.getNoCoinState()  # Transition to NoCoinState
        else:
            print("Machine is now sold out!")
            return machine.getSoldOutState()  # Transition to SoldOutState

    def returnCoin(self, machine):
        print("Cannot return coin while dispensing item!")
        return machine.getDispenseState()  # Stay in same state

    def refill(self, machine, quantity):
        print("Can't refil in this state")
        return machine.getDispenseState()  # Stay in same state

    def getStateName(self):
        return "DISPENSING"


# Concrete State: Sold Out
class SoldOutState(VendingState):
    def insertCoin(self, machine, coin):
        print("Machine is sold out. Coin returned: Rs " + str(coin))
        return machine.getSoldOutState()  # Stay in same state

    def selectItem(self, machine):
        print("Machine is sold out!")
        return machine.getSoldOutState()  # Stay in same state

    def dispense(self, machine):
        print("Machine is sold out!")
        return machine.getSoldOutState()  # Stay in same state

    def returnCoin(self, machine):
        print("Machine is sold out. No coin inserted.")
        return machine.getSoldOutState()  # Stay in same state

    def refill(self, machine, quantity):
        print("Items refilling")
        machine.incrementItemCount(quantity)
        return machine.getNoCoinState()

    def getStateName(self):
        return "SOLD_OUT"


# Main class for Vending Machine
class VendingMachineMain:
    @staticmethod
    def main(args):
        print("=== Water Bottle VENDING MACHINE ===")

        itemCount = 2
        itemPrice = 20

        machine = VendingMachine(itemCount, itemPrice)
        machine.printStatus()

        # Test scenarios - each operation potentially changes state
        print("1. Trying to select item without coin:")
        machine.selectItem()  # Should ask for coin, no state change
        machine.printStatus()

        print("2. Inserting coin:")
        machine.insertCoin(10)  # State changes to HAS_COIN
        machine.printStatus()

        print("3. Selecting item with insufficient funds:")
        machine.selectItem()  # Insufficient funds, stays in HAS_COIN
        machine.printStatus()

        print("4. Adding more coins:")
        machine.insertCoin(10)  # Add more money, stays in HAS_COIN
        machine.printStatus()

        print("5. Selecting item Now")
        machine.selectItem()  # State changes to SOLD
        machine.printStatus()

        print("6. Dispensing item:")
        machine.dispense()  # State changes to NO_COIN (items remaining)
        machine.printStatus()

        print("7. Buying last item:")
        machine.insertCoin(20)  # State changes to HAS_COIN
        machine.selectItem()  # State changes to SOLD
        machine.dispense()  # State changes to SOLD_OUT (no items left)
        machine.printStatus()

        print("8. Trying to use sold out machine:")
        machine.insertCoin(5)  # Coin returned, stays in SOLD_OUT

        print("9. Trying to use sold out machine:")
        machine.refill(2)
        machine.printStatus()  # State changes NO_COIN


if __name__ == "__main__":
    import sys
    VendingMachineMain.main(sys.argv[1:])
