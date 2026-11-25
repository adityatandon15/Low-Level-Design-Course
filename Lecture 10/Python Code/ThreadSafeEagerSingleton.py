class ThreadSafeEagerSingleton:
    def __init__(self):
        print("Singleton Constructor Called!")

    @classmethod
    def getInstance(cls):
        return cls._instance

    @staticmethod
    def main(args):
        s1 = ThreadSafeEagerSingleton.getInstance()
        s2 = ThreadSafeEagerSingleton.getInstance()

        print(str(s1 is s2).lower())


# Eager instance, created when the class is loaded (Java static field initializer).
ThreadSafeEagerSingleton._instance = ThreadSafeEagerSingleton()


if __name__ == "__main__":
    # call the same demo as Java main
    ThreadSafeEagerSingleton.main(None)
