class MySQLDatabase:  # Low-level module
    def saveToSQL(self, data):
        print(
            "Executing SQL Query: INSERT INTO users VALUES('"
            + data + "');"
        )


class MongoDBDatabase:  # Low-level module
    def saveToMongo(self, data):
        print(
            "Executing MongoDB Function: db.users.insert({name: '"
            + data + "'})"
        )


class UserService:  # High-level module (Tightly coupled)
    def __init__(self):
        self._sqlDb = MySQLDatabase()
        self._mongoDb = MongoDBDatabase()

    def storeUserToSQL(self, user):
        # MySQL-specific code
        self._sqlDb.saveToSQL(user)

    def storeUserToMongo(self, user):
        # MongoDB-specific code
        self._mongoDb.saveToMongo(user)


class DIPViolated:
    @staticmethod
    def main(args):
        service = UserService()
        service.storeUserToSQL("Aditya")
        service.storeUserToMongo("Rohit")


if __name__ == "__main__":
    # call the same demo as Java main
    DIPViolated.main(None)
