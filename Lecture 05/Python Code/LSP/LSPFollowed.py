from abc import ABC, abstractmethod

# 1. DepositOnlyAccount interface: only allows deposits
class DepositOnlyAccount(ABC):
    @abstractmethod
    def deposit(self, amount):
        pass


# 2. WithdrawableAccount interface: allows deposits and withdrawals
class WithdrawableAccount(DepositOnlyAccount):
    @abstractmethod
    def withdraw(self, amount):
        pass


class SavingAccount(WithdrawableAccount):
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


class CurrentAccount(WithdrawableAccount):
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


class FixedTermAccount(DepositOnlyAccount):
    def __init__(self):
        self._balance = 0.0

    def deposit(self, amount):
        amount = float(amount)
        self._balance += amount
        print("Deposited: " + str(amount) + " in Fixed Term Account. New Balance: " + str(self._balance))


class BankClient:
    def __init__(self, withdrawableAccounts, depositOnlyAccounts):
        self._withdrawableAccounts = withdrawableAccounts
        self._depositOnlyAccounts = depositOnlyAccounts

    def processTransactions(self):
        for acc in self._withdrawableAccounts:
            acc.deposit(1000)
            acc.withdraw(500)
        for acc in self._depositOnlyAccounts:
            acc.deposit(5000)


class LSPFollowed:
    @staticmethod
    def main(args):
        withdrawableAccounts = []
        withdrawableAccounts.append(SavingAccount())
        withdrawableAccounts.append(CurrentAccount())

        depositOnlyAccounts = []
        depositOnlyAccounts.append(FixedTermAccount())

        client = BankClient(withdrawableAccounts, depositOnlyAccounts)
        client.processTransactions()


if __name__ == "__main__":
    # call the same demo as Java main
    LSPFollowed.main(None)
