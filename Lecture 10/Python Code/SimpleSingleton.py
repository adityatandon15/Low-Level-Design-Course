class SimpleSingleton:
    _instance = None

    def __init__(self):
        print("Singleton Constructor called")

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @staticmethod
    def main(args):
        s1 = SimpleSingleton.getInstance()
        s2 = SimpleSingleton.getInstance()

        print(str(s1 is s2).lower())


if __name__ == "__main__":
    # call the same demo as Java main
    SimpleSingleton.main(None)
