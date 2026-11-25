# A Precondition must be statisfied before a method can be executed.
# Sub classes can weaken the precondition but cannot strengthen it.

class IllegalArgumentException(Exception):
    pass


class User:
    # Precondition: Password must be at least 8 characters long
    def setPassword(self, password):
        if len(password) < 8:
            raise IllegalArgumentException("Password must be at least 8 characters long!")
        print("Password set successfully")


class AdminUser(User):
    # Precondition: Password must be at least 6 characters
    def setPassword(self, password):
        if len(password) < 6:
            raise IllegalArgumentException("Password must be at least 6 characters long!")
        print("Password set successfully")


class PreConditions:
    @staticmethod
    def main(args):
        user = AdminUser()
        user.setPassword("Admin1")  # Works fine: AdminUser allows shorter passwords


if __name__ == "__main__":
    # call the same demo as Java main
    PreConditions.main(None)
