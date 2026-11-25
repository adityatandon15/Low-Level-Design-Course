# Memento - Stores database state snapshot
class DatabaseMemento:
    def __init__(self, dbData):
        self.data = dict(dbData)

    def getState(self):
        return self.data


# Originator - The database whose state we want to save/restore
class Database:
    def __init__(self):
        self.records = {}

    # Insert a record
    def insert(self, key, value):
        self.records[key] = value
        print("Inserted: " + key + " = " + value)

    # Update a record
    def update(self, key, value):
        if key in self.records:
            self.records[key] = value
            print("Updated: " + key + " = " + value)
        else:
            print("Key not found for update: " + key)

    # Delete a record
    def remove(self, key):
        if key in self.records:
            del self.records[key]
            print("Deleted: " + key)
        else:
            print("Key not found for deletion: " + key)

    # Create memento - Save current state
    def createMemento(self):
        print("Creating database backup...")
        return DatabaseMemento(self.records)

    # Restore from memento - Rollback to saved state
    def restoreFromMemento(self, memento):
        self.records = dict(memento.getState())
        print("Database restored from backup!")

    # Display current database state
    def displayRecords(self):
        print("\n--- Current Database State ---")
        if len(self.records) == 0:
            print("Database is empty")
        else:
            for key, value in self.records.items():
                print(key + " = " + value)
        print("-----------------------------\n")


# Caretaker - Manages the memento (transaction manager)
class TransactionManager:
    def __init__(self):
        self.backup = None

    # Begin transaction - create backup
    def beginTransaction(self, db):
        print("=== BEGIN TRANSACTION ===")
        self.backup = db.createMemento()

    # Commit transaction - discard backup
    def commitTransaction(self):
        print("=== COMMIT TRANSACTION ===")
        if self.backup is not None:
            self.backup = None
        print("Transaction committed successfully!")

    # Rollback transaction - restore from backup
    def rollbackTransaction(self, db):
        print("=== ROLLBACK TRANSACTION ===")
        if self.backup is not None:
            db.restoreFromMemento(self.backup)
            self.backup = None
            print("Transaction rolled back!")
        else:
            print("No backup available for rollback!")


class MementoPattern:
    @staticmethod
    def main(args=None):
        db = Database()
        txManager = TransactionManager()

        # success scenario
        txManager.beginTransaction(db)
        db.insert("user1", "Aditya")
        db.insert("user2", "Rohit")
        txManager.commitTransaction()

        db.displayRecords()

        # Failed scenario
        txManager.beginTransaction(db)
        db.insert("user3", "Saurav")
        db.insert("user4", "Manish")

        db.displayRecords()

        # Some error -> Rollback
        print("ERROR: Something went wrong during transaction!")
        txManager.rollbackTransaction(db)

        db.displayRecords()


if __name__ == "__main__":
    MementoPattern.main()
