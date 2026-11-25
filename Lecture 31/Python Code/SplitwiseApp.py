from abc import ABC, abstractmethod
from decimal import Decimal, ROUND_HALF_EVEN
from enum import Enum


def _formatDecimal(value):
    # java.text.DecimalFormat("#.##"): at most 2 fraction digits, HALF_EVEN, no trailing zeros
    quantized = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_EVEN)
    text = format(quantized, "f")
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    if text in ("", "-0"):
        return "0"
    return text


# Forward declarations equivalent - not needed in Java due to automatic resolution

class SplitType(Enum):
    EQUAL = 1
    EXACT = 2
    PERCENTAGE = 3


class Split:
    def __init__(self, userId, amount):
        self.userId = userId
        self.amount = amount


# Observer Pattern - Notification interface
class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass


# Strategy Pattern - Split strategies
class SplitStrategy(ABC):
    @abstractmethod
    def calculateSplit(self, totalAmount, userIds, values):
        pass


class EqualSplit(SplitStrategy):
    def calculateSplit(self, totalAmount, userIds, values):
        splits = []
        amountPerUser = totalAmount / len(userIds)

        for userId in userIds:
            splits.append(Split(userId, amountPerUser))
        return splits


class ExactSplit(SplitStrategy):
    def calculateSplit(self, totalAmount, userIds, values):
        splits = []

        # validations

        for i in range(len(userIds)):
            splits.append(Split(userIds[i], values[i]))
        return splits


class PercentageSplit(SplitStrategy):
    def calculateSplit(self, totalAmount, userIds, values):
        splits = []

        # validations

        for i in range(len(userIds)):
            amount = (totalAmount * values[i]) / 100.0
            splits.append(Split(userIds[i], amount))
        return splits


# Factory for split strategies
class SplitFactory:
    @staticmethod
    def getSplitStrategy(type):
        if type == SplitType.EQUAL:
            return EqualSplit()
        elif type == SplitType.EXACT:
            return ExactSplit()
        elif type == SplitType.PERCENTAGE:
            return PercentageSplit()
        else:
            return EqualSplit()


# User class --> Concrete Observer
class User(Observer):
    nextUserId = 0

    def __init__(self, name, email):
        User.nextUserId += 1
        self.userId = "user" + str(User.nextUserId)
        self.name = name
        self.email = email
        self.balances = {}  # userId -> amount (positive = they owe you, negative = you owe them)

    def update(self, message):
        print("[NOTIFICATION to " + self.name + "]: " + message)

    def updateBalance(self, otherUserId, amount):
        self.balances[otherUserId] = self.balances.get(otherUserId, 0.0) + amount

        # Remove if balance becomes zero
        if abs(self.balances[otherUserId]) < 0.01:
            del self.balances[otherUserId]

    def getTotalOwed(self):
        total = 0.0
        for balance in self.balances.values():
            if balance < 0:
                total += abs(balance)
        return total

    def getTotalOwing(self):
        total = 0.0
        for balance in self.balances.values():
            if balance > 0:
                total += balance
        return total


# Expense Model class
class Expense:
    nextExpenseId = 0

    def __init__(self, desc, amount, paidBy, splits, group=""):
        Expense.nextExpenseId += 1
        self.expenseId = "expense" + str(Expense.nextExpenseId)
        self.description = desc
        self.totalAmount = amount
        self.paidByUserId = paidBy
        self.splits = splits
        self.groupId = group


class _MutableEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value


class DebtSimplifier:
    @staticmethod
    def simplifyDebts(groupBalances):
        # Calculate net amount for each person
        netAmounts = {}

        # Initialize all users with 0
        for userId in groupBalances:
            netAmounts[userId] = 0.0

        # Calculate net amounts
        # We only need to process each balance once (not twice)
        # If groupBalances[A][B] = 200, it means B owes A 200
        # So A should receive 200 (positive) and B should pay 200 (negative)
        for creditorId, userBalance in groupBalances.items():
            for debtorId, amount in userBalance.items():
                # Only process positive amounts to avoid double counting
                if amount > 0:
                    netAmounts[creditorId] = netAmounts[creditorId] + amount  # creditor receives
                    netAmounts[debtorId] = netAmounts[debtorId] - amount      # debtor pays

        # Divide users into creditors and debtors
        creditors = []  # those who should receive money
        debtors = []    # those who should pay money

        for userId, net in netAmounts.items():
            if net > 0.01:  # creditor
                creditors.append(_MutableEntry(userId, net))
            elif net < -0.01:  # debtor
                debtors.append(_MutableEntry(userId, -net))  # store positive amount

        # Sort for better optimization (largest amounts first)
        creditors.sort(key=lambda entry: entry.value, reverse=True)
        debtors.sort(key=lambda entry: entry.value, reverse=True)

        # Create new simplified balance map
        simplifiedBalances = {}

        # Initialize empty maps for all users
        for userId in groupBalances:
            simplifiedBalances[userId] = {}

        # Use greedy algorithm to minimize transactions
        i = 0
        j = 0
        while i < len(creditors) and j < len(debtors):
            creditorId = creditors[i].key
            debtorId = debtors[j].key
            creditorAmount = creditors[i].value
            debtorAmount = debtors[j].value

            # Find the minimum amount to settle
            settleAmount = min(creditorAmount, debtorAmount)

            # Update simplified balances
            # debtorId owes creditorId the settleAmount
            simplifiedBalances[creditorId][debtorId] = settleAmount
            simplifiedBalances[debtorId][creditorId] = -settleAmount

            # Update remaining amounts
            creditors[i].value = creditors[i].value - settleAmount
            debtors[j].value = debtors[j].value - settleAmount

            # Move to next creditor or debtor if current one is settled
            if creditors[i].value < 0.01:
                i += 1
            if debtors[j].value < 0.01:
                j += 1

        return simplifiedBalances


# Group class --> Concrete Observable
class Group:
    def getUserByuserId(self, userId):
        user = None

        for member in self.members:
            if member.userId == userId:
                user = member
        return user

    nextGroupId = 0

    def __init__(self, name):
        Group.nextGroupId += 1
        self.groupId = "group" + str(Group.nextGroupId)
        self.name = name
        self.members = []  # observers
        self.groupExpenses = {}  # Group's own expense book
        self.groupBalances = {}  # memberId -> {otherMemberId -> balance}

    def addMember(self, user):
        self.members.append(user)

        # Initialize balance map for new member
        self.groupBalances[user.userId] = {}
        print(user.name + " added to group " + self.name)

    def removeMember(self, userId):
        # Check if user can be removed or not
        if not self.canUserLeaveGroup(userId):
            print("\nUser not allowed to leave group without clearing expenses")
            return False

        # Remove from observers
        self.members = [user for user in self.members if user.userId != userId]

        # Remove from group balances
        del self.groupBalances[userId]

        # Remove this user from other members' balance maps
        for memberBalance in self.groupBalances.values():
            memberBalance.pop(userId, None)
        return True

    def notifyMembers(self, message):
        for observer in self.members:
            observer.update(message)

    def isMember(self, userId):
        return userId in self.groupBalances

    # Update balance within group
    def updateGroupBalance(self, fromUserId, toUserId, amount):
        fromBalances = self.groupBalances[fromUserId]
        toBalances = self.groupBalances[toUserId]
        fromBalances[toUserId] = fromBalances.get(toUserId, 0.0) + amount
        toBalances[fromUserId] = toBalances.get(fromUserId, 0.0) - amount

        # Remove if balance becomes zero
        if abs(fromBalances[toUserId]) < 0.01:
            del fromBalances[toUserId]
        if abs(toBalances[fromUserId]) < 0.01:
            del toBalances[fromUserId]

    # Check if user can leave group.
    def canUserLeaveGroup(self, userId):
        if not self.isMember(userId):
            raise RuntimeError("user is not a part of this group")

        # Check if user has any outstanding balance with other group members
        userBalanceSheet = self.groupBalances[userId]
        for balance in userBalanceSheet.values():
            if abs(balance) > 0.01:
                return False  # Has outstanding balance
        return True

    # Get user's balance within this group
    def getUserGroupBalances(self, userId):
        if not self.isMember(userId):
            raise RuntimeError("user is not a part of this group")
        return self.groupBalances[userId]

    # Add expense to this group
    def addExpense(self, description, amount, paidByUserId, involvedUsers, splitType, splitValues=None):
        if splitValues is None:
            splitValues = []

        if not self.isMember(paidByUserId):
            raise RuntimeError("user is not a part of this group")

        # Validate that all involved users are group members
        for userId in involvedUsers:
            if not self.isMember(userId):
                raise RuntimeError("involvedUsers are not a part of this group")

        # Generate splits using strategy pattern
        splits = SplitFactory.getSplitStrategy(splitType).calculateSplit(
            amount, involvedUsers, splitValues)

        # Create expense in group's own expense book
        expense = Expense(description, amount, paidByUserId, splits, self.groupId)
        self.groupExpenses[expense.expenseId] = expense

        # Update group balances
        for split in splits:
            if split.userId != paidByUserId:
                # Person who paid gets positive balance, person who owes gets negative
                self.updateGroupBalance(paidByUserId, split.userId, split.amount)

        print("\n=========== Sending Notifications ====================")
        paidByName = self.getUserByuserId(paidByUserId).name
        self.notifyMembers("New expense added: " + description + " (Rs " + str(amount) + ")")

        # Printing console message-------
        print("\n=========== Expense Message ====================")
        print("Expense added to " + self.name + ": " + description + " (Rs " + str(amount)
              + ") paid by " + paidByName + " and involved people are : ")
        if splitValues:
            for i in range(len(splitValues)):
                print(self.getUserByuserId(involvedUsers[i]).name + " : " + str(splitValues[i]))
        else:
            for user in involvedUsers:
                print(self.getUserByuserId(user).name + ", ", end="")
            print("\nWill be Paid Equally")
        #-----------------------------------

        return True

    def settlePayment(self, fromUserId, toUserId, amount):
        # Validate that both users are group members
        if (not self.isMember(fromUserId)) or (not self.isMember(toUserId)):
            print("user is not a part of this group")
            return False

        # Update group balances
        self.updateGroupBalance(fromUserId, toUserId, amount)

        # Get user names for display
        fromName = self.getUserByuserId(fromUserId).name
        toName = self.getUserByuserId(toUserId).name

        # Notify group members
        self.notifyMembers("Settlement: " + fromName + " paid " + toName + " Rs " + str(amount))

        print("Settlement in " + self.name + ": " + fromName + " settled Rs "
              + str(amount) + " with " + toName)

        return True

    def showGroupBalances(self):
        print("\n=== Group Balances for " + self.name + " ===")

        for memberId, userBalances in self.groupBalances.items():
            memberName = self.getUserByuserId(memberId).name

            print(memberName + "'s balances in group:")

            if not userBalances:
                print("  No outstanding balances")
            else:
                for otherMemberUserId, balance in userBalances.items():
                    otherName = self.getUserByuserId(otherMemberUserId).name

                    if balance > 0:
                        print("  " + otherName + " owes: Rs " + _formatDecimal(balance))
                    else:
                        print("  Owes " + otherName + ": Rs " + _formatDecimal(abs(balance)))

    def simplifyGroupDebts(self):
        simplifiedBalances = DebtSimplifier.simplifyDebts(self.groupBalances)
        self.groupBalances = simplifiedBalances

        print("\nDebts have been simplified for group: " + self.name)


# Main ExpenseManager class (Singleton - Facade)
class Splitwise:
    instance = None

    def __init__(self):
        self.users = {}
        self.groups = {}
        self.expenses = {}

    @staticmethod
    def getInstance():
        if Splitwise.instance is None:
            Splitwise.instance = Splitwise()
        return Splitwise.instance

    # User management
    def createUser(self, name, email):
        user = User(name, email)
        self.users[user.userId] = user
        print("User created: " + name + " (ID: " + user.userId + ")")
        return user

    def getUser(self, userId):
        return self.users.get(userId)

    # Group management
    def createGroup(self, name):
        group = Group(name)
        self.groups[group.groupId] = group
        print("Group created: " + name + " (ID: " + group.groupId + ")")
        return group

    def getGroup(self, groupId):
        return self.groups.get(groupId)

    def addUserToGroup(self, userId, groupId):
        user = self.getUser(userId)
        group = self.getGroup(groupId)

        if user is not None and group is not None:
            group.addMember(user)

    # Try to remove user from group - just delegates to group
    def removeUserFromGroup(self, userId, groupId):
        group = self.getGroup(groupId)

        if group is None:
            print("Group not found!")
            return False

        user = self.getUser(userId)
        if user is None:
            print("User not found!")
            return False

        userRemoved = group.removeMember(userId)

        if userRemoved:
            print(user.name + " successfully left " + group.name)
        return userRemoved

    # Expense management - delegate to group
    def addExpenseToGroup(self, groupId, description, amount, paidByUserId,
                          involvedUsers, splitType, splitValues=None):
        if splitValues is None:
            splitValues = []

        group = self.getGroup(groupId)
        if group is None:
            print("Group not found!")
            return

        group.addExpense(description, amount, paidByUserId, involvedUsers, splitType, splitValues)

    # Settlement - delegate to group
    def settlePaymentInGroup(self, groupId, fromUserId, toUserId, amount):
        group = self.getGroup(groupId)
        if group is None:
            print("Group not found!")
            return

        group.settlePayment(fromUserId, toUserId, amount)

    # Settlement
    def settleIndividualPayment(self, fromUserId, toUserId, amount):
        fromUser = self.getUser(fromUserId)
        toUser = self.getUser(toUserId)

        if fromUser is not None and toUser is not None:
            fromUser.updateBalance(toUserId, amount)
            toUser.updateBalance(fromUserId, -amount)

            print(fromUser.name + " settled Rs" + str(amount) + " with " + toUser.name)

    def addIndividualExpense(self, description, amount, paidByUserId, toUserId,
                             splitType, splitValues=None):
        if splitValues is None:
            splitValues = []

        strategy = SplitFactory.getSplitStrategy(splitType)
        splits = strategy.calculateSplit(amount, [paidByUserId, toUserId], splitValues)

        expense = Expense(description, amount, paidByUserId, splits)
        self.expenses[expense.expenseId] = expense

        paidByUser = self.getUser(paidByUserId)
        toUser = self.getUser(toUserId)

        paidByUser.updateBalance(toUserId, amount)
        toUser.updateBalance(paidByUserId, -amount)

        print("Individual expense added: " + description + " (Rs " + str(amount)
              + ") paid by " + paidByUser.name + " for " + toUser.name)

    # Display Method
    def showUserBalance(self, userId):
        user = self.getUser(userId)
        if user is None:
            return

        print("\n=========== Balance for " + user.name + " ====================")
        print("Total you owe: Rs " + _formatDecimal(user.getTotalOwed()))
        print("Total others owe you: Rs " + _formatDecimal(user.getTotalOwing()))

        print("Detailed balances:")
        for otherUserId, balance in user.balances.items():
            otherUser = self.getUser(otherUserId)
            if otherUser is not None:
                if balance > 0:
                    print("  " + otherUser.name + " owes you: Rs" + str(balance))
                else:
                    print("  You owe " + otherUser.name + ": Rs" + str(abs(balance)))

    def showGroupBalances(self, groupId):
        group = self.getGroup(groupId)
        if group is None:
            return

        group.showGroupBalances()

    def simplifyGroupDebts(self, groupId):
        group = self.getGroup(groupId)
        if group is None:
            return

        # Use group's balance data for debt simplification
        group.simplifyGroupDebts()


class SplitwiseApp:
    @staticmethod
    def main(args):
        manager = Splitwise.getInstance()

        print("\n=========== Creating Users ====================")
        user1 = manager.createUser("Aditya", "aditya@gmail.com")
        user2 = manager.createUser("Rohit", "rohit@gmail.com")
        user3 = manager.createUser("Manish", "manish@gmail.com")
        user4 = manager.createUser("Saurav", "saurav@gmail.com")

        print("\n=========== Creating Group and Adding Members ====================")
        hostelGroup = manager.createGroup("Hostel Expenses")
        manager.addUserToGroup(user1.userId, hostelGroup.groupId)
        manager.addUserToGroup(user2.userId, hostelGroup.groupId)
        manager.addUserToGroup(user3.userId, hostelGroup.groupId)
        manager.addUserToGroup(user4.userId, hostelGroup.groupId)

        print("\n=========== Adding Expenses in group ====================")
        groupMembers = [user1.userId, user2.userId, user3.userId, user4.userId]
        manager.addExpenseToGroup(hostelGroup.groupId, "Lunch", 800.0, user1.userId, groupMembers, SplitType.EQUAL)

        dinnerMembers = [user1.userId, user3.userId, user4.userId]
        dinnerAmounts = [200.0, 300.0, 200.0]
        manager.addExpenseToGroup(hostelGroup.groupId, "Dinner", 700.0, user3.userId, dinnerMembers,
                                 SplitType.EXACT, dinnerAmounts)

        print("\n=========== printing Group-Specific Balances ====================")
        manager.showGroupBalances(hostelGroup.groupId)

        print("\n=========== Debt Simplification ====================")
        manager.simplifyGroupDebts(hostelGroup.groupId)

        print("\n=========== printing Group-Specific Balances ====================")
        manager.showGroupBalances(hostelGroup.groupId)

        print("\n=========== Adding Individual Expense ====================")
        manager.addIndividualExpense("Coffee", 40.0, user2.userId, user4.userId, SplitType.EQUAL)

        print("\n=========== printing User Balances ====================")
        manager.showUserBalance(user1.userId)
        manager.showUserBalance(user2.userId)
        manager.showUserBalance(user3.userId)
        manager.showUserBalance(user4.userId)

        print("\n==========Attempting to remove Rohit from group==========")
        manager.removeUserFromGroup(user2.userId, hostelGroup.groupId)

        print("\n======== Making Settlement to Clear Rohit's Debt ==========")
        manager.settlePaymentInGroup(hostelGroup.groupId, user2.userId, user3.userId, 200.0)

        print("\n======== Attempting to Remove Rohit Again ==========")
        manager.removeUserFromGroup(user2.userId, hostelGroup.groupId)

        print("\n=========== Updated Group Balances ====================")
        manager.showGroupBalances(hostelGroup.groupId)


if __name__ == "__main__":
    import sys
    SplitwiseApp.main(sys.argv[1:])
