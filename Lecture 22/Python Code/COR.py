from abc import ABC, abstractmethod


class MoneyHandler(ABC):
    def __init__(self):
        self.nextHandler = None

    def setNextHandler(self, next):
        self.nextHandler = next

    @abstractmethod
    def dispense(self, amount):
        pass


class ThousandHandler(MoneyHandler):
    def __init__(self, numNotes):
        super().__init__()
        self.numNotes = numNotes

    def dispense(self, amount):
        notesNeeded = amount // 1000

        if notesNeeded > self.numNotes:
            notesNeeded = self.numNotes
            self.numNotes = 0
        else:
            self.numNotes -= notesNeeded

        if notesNeeded > 0:
            print("Dispensing " + str(notesNeeded) + " x ₹1000 notes.")

        remainingAmount = amount - (notesNeeded * 1000)
        if remainingAmount > 0:
            if self.nextHandler is not None:
                self.nextHandler.dispense(remainingAmount)
            else:
                print("Remaining amount of " + str(remainingAmount) + " cannot be fulfilled (Insufficinet fund in ATM)")


class FiveHundredHandler(MoneyHandler):
    def __init__(self, numNotes):
        super().__init__()
        self.numNotes = numNotes

    def dispense(self, amount):
        notesNeeded = amount // 500

        if notesNeeded > self.numNotes:
            notesNeeded = self.numNotes
            self.numNotes = 0
        else:
            self.numNotes -= notesNeeded

        if notesNeeded > 0:
            print("Dispensing " + str(notesNeeded) + " x ₹500 notes.")

        remainingAmount = amount - (notesNeeded * 500)
        if remainingAmount > 0:
            if self.nextHandler is not None:
                self.nextHandler.dispense(remainingAmount)
            else:
                print("Remaining amount of " + str(remainingAmount) + " cannot be fulfilled (Insufficinet fund in ATM)")


class TwoHundredHandler(MoneyHandler):
    def __init__(self, numNotes):
        super().__init__()
        self.numNotes = numNotes

    def dispense(self, amount):
        notesNeeded = amount // 200

        if notesNeeded > self.numNotes:
            notesNeeded = self.numNotes
            self.numNotes = 0
        else:
            self.numNotes -= notesNeeded

        if notesNeeded > 0:
            print("Dispensing " + str(notesNeeded) + " x ₹200 notes.")

        remainingAmount = amount - (notesNeeded * 200)
        if remainingAmount > 0:
            if self.nextHandler is not None:
                self.nextHandler.dispense(remainingAmount)
            else:
                print("Remaining amount of " + str(remainingAmount) + " cannot be fulfilled (Insufficinet fund in ATM)")


class HundredHandler(MoneyHandler):
    def __init__(self, numNotes):
        super().__init__()
        self.numNotes = numNotes

    def dispense(self, amount):
        notesNeeded = amount // 100

        if notesNeeded > self.numNotes:
            notesNeeded = self.numNotes
            self.numNotes = 0
        else:
            self.numNotes -= notesNeeded

        if notesNeeded > 0:
            print("Dispensing " + str(notesNeeded) + " x ₹100 notes.")

        remainingAmount = amount - (notesNeeded * 100)
        if remainingAmount > 0:
            if self.nextHandler is not None:
                self.nextHandler.dispense(remainingAmount)
            else:
                print("Remaining amount of " + str(remainingAmount) + " cannot be fulfilled (Insufficinet fund in ATM)")


class COR:
    @staticmethod
    def main(args):
        thousandHandler = ThousandHandler(3)
        fiveHundredHandler = FiveHundredHandler(5)
        twoHundredHandler = TwoHundredHandler(10)
        hundredHandler = HundredHandler(20)

        thousandHandler.setNextHandler(fiveHundredHandler)
        fiveHundredHandler.setNextHandler(twoHundredHandler)
        twoHundredHandler.setNextHandler(hundredHandler)

        amountToWithdraw = 4000

        print("\nDispensing amount: ₹" + str(amountToWithdraw))
        thousandHandler.dispense(amountToWithdraw)


if __name__ == "__main__":
    COR.main([])
