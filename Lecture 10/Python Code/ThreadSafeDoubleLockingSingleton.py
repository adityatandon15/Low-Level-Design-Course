import threading


class ThreadSafeDoubleLockingSingleton:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        print("Singleton Constructor Called!")

    # Double check locking..
    @classmethod
    def getInstance(cls):
        if cls._instance is None:  # First check (no locking)
            with cls._lock:  # Lock only if needed
                if cls._instance is None:  # Second check (after acquiring lock)
                    cls._instance = cls()
        return cls._instance

    @staticmethod
    def main(args):
        s1 = ThreadSafeDoubleLockingSingleton.getInstance()
        s2 = ThreadSafeDoubleLockingSingleton.getInstance()

        print(str(s1 is s2).lower())


if __name__ == "__main__":
    # call the same demo as Java main
    ThreadSafeDoubleLockingSingleton.main(None)
