from abc import ABC, abstractmethod


class UnsupportedOperationException(Exception):
    def getMessage(self):
        return self.args[0] if self.args else None


# Account interface
class Account(ABC):
    @abstractmethod
    def deposit(self, amount):
        pass

    @abstractmethod
    def withdraw(self, amount):
        pass


class SavingAccount(Account):
    def __init__(self):
        self._balance = 0.0

    def deposit(self, amount):
        amount = float(amount)
        self._balance += amount
        print("Deposited: " + str(amount) + " in Savings Account. New Balance: " + str(self._balance))

    def withdraw(self, amount):
        amount = float(amount)
        if self._balance >= amount:
            self._balance -= amount
            print("Withdrawn: " + str(amount) + " from Savings Account. New Balance: " + str(self._balance))
        else:
            print("Insufficient funds in Savings Account!")


class CurrentAccount(Account):
    def __init__(self):
        self._balance = 0.0

    def deposit(self, amount):
        amount = float(amount)
        self._balance += amount
        print("Deposited: " + str(amount) + " in Current Account. New Balance: " + str(self._balance))

    def withdraw(self, amount):
        amount = float(amount)
        if self._balance >= amount:
            self._balance -= amount
            print("Withdrawn: " + str(amount) + " from Current Account. New Balance: " + str(self._balance))
        else:
            print("Insufficient funds in Current Account!")


class FixedTermAccount(Account):
    def __init__(self):
        self._balance = 0.0

    def deposit(self, amount):
        amount = float(amount)
        self._balance += amount
        print("Deposited: " + str(amount) + " in Fixed Term Account. New Balance: " + str(self._balance))

    def withdraw(self, amount):
        raise UnsupportedOperationException("Withdrawal not allowed in Fixed Term Account!")


class BankClient:
    def __init__(self, accounts):
        self._accounts = accounts

    def processTransactions(self):
        for acc in self._accounts:
            acc.deposit(1000)

            # Checking account type explicitly
            if isinstance(acc, FixedTermAccount):
                print("Skipping withdrawal for Fixed Term Account.")
            else:
                try:
                    acc.withdraw(500)
                except UnsupportedOperationException as e:
                    print("Exception: " + e.getMessage())


class LSPFollowedWrongly:
    @staticmethod
    def main(args):
        accounts = []
        accounts.append(SavingAccount())
        accounts.append(CurrentAccount())
        accounts.append(FixedTermAccount())

        client = BankClient(accounts)
        client.processTransactions()


if __name__ == "__main__":
    # call the same demo as Java main
    LSPFollowedWrongly.main(None)
