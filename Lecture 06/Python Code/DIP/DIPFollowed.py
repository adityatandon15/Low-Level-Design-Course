from abc import ABC, abstractmethod

# Abstraction (Interface)
class Database(ABC):
    @abstractmethod
    def save(self, data):
        pass


# MySQL implementation (Low-level module)
class MySQLDatabase(Database):
    def save(self, data):
        print(
            "Executing SQL Query: INSERT INTO users VALUES('"
            + data + "');"
        )


# MongoDB implementation (Low-level module)
class MongoDBDatabase(Database):
    def save(self, data):
        print(
            "Executing MongoDB Function: db.users.insert({name: '"
            + data + "'})"
        )


# High-level module (Now loosely coupled via Dependency Injection)
class UserService:
    def __init__(self, database):
        self._db = database

    def storeUser(self, user):
        self._db.save(user)


class DIPFollowed:
    @staticmethod
    def main(args):
        mysql = MySQLDatabase()
        mongodb = MongoDBDatabase()

        service1 = UserService(mysql)
        service1.storeUser("Aditya")

        service2 = UserService(mongodb)
        service2.storeUser("Rohit")


if __name__ == "__main__":
    # call the same demo as Java main
    DIPFollowed.main(None)
