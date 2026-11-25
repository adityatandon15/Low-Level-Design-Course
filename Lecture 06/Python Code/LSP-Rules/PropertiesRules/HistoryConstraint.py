# Subclass methods should not be allowed state changes that
# the base class never allowed.

class IllegalArgumentException(Exception):
    pass


class RuntimeException(Exception):
    pass


class BankAccount:
    def __init__(self, b):
        if b < 0:
            raise IllegalArgumentException("Balance can't be negative")
        self.balance = float(b)

    # History Constraint: withdraw should be allowed
    def withdraw(self, amount):
        amount = float(amount)
        if self.balance - amount < 0:
            raise RuntimeException("Insufficient funds")
        self.balance -= amount
        print("Amount withdrawn. Remaining balance is " + str(self.balance))


class FixedDepositAccount(BankAccount):
    def __init__(self, b):
        super().__init__(b)

    # LSP break! History constraint broken!
    # Parent class behavior changed: Now withdraw is not allowed.
    # This class will break client code that relies on withdraw.
    def withdraw(self, amount):
        raise RuntimeException("Withdraw not allowed in Fixed Deposit")


class HistoryConstraint:
    @staticmethod
    def main(args):
        bankAccount = BankAccount(100)
        bankAccount.withdraw(100)


if __name__ == "__main__":
    # call the same demo as Java main
    HistoryConstraint.main(None)
