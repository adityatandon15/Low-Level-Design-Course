# Class Invariant of a parent class Object should not be broken by child class Object.
# Hence child class can either maintain or strengthen the invariant but never narrows it down.

class IllegalArgumentException(Exception):
    pass


class RuntimeException(Exception):
    pass


# Invariant: Balance cannot be negative
class BankAccount:
    def __init__(self, b):
        if b < 0:
            raise IllegalArgumentException("Balance can't be negative")
        self.balance = float(b)

    def withdraw(self, amount):
        amount = float(amount)
        if self.balance - amount < 0:
            raise RuntimeException("Insufficient funds")
        self.balance -= amount
        print("Amount withdrawn. Remaining balance is " + str(self.balance))


# Breaks invariant: Should not be allowed.
class CheatAccount(BankAccount):
    def __init__(self, b):
        super().__init__(b)

    def withdraw(self, amount):
        amount = float(amount)
        self.balance -= amount  # LSP break! Negative balance allowed
        print("Amount withdrawn. Remaining balance is " + str(self.balance))


class ClassInvariants:
    @staticmethod
    def main(args):
        bankAccount = BankAccount(100)
        bankAccount.withdraw(100)


if __name__ == "__main__":
    # call the same demo as Java main
    ClassInvariants.main(None)
