import threading


class ThreadSafeLockingSingleton:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        print("Singleton Constructor Called!")

    @classmethod
    def getInstance(cls):
        with cls._lock:  # Lock for thread safety
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    @staticmethod
    def main(args):
        s1 = ThreadSafeLockingSingleton.getInstance()
        s2 = ThreadSafeLockingSingleton.getInstance()

        print(str(s1 is s2).lower())


if __name__ == "__main__":
    # call the same demo as Java main
    ThreadSafeLockingSingleton.main(None)
