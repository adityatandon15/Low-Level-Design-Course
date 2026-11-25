class NoSingleton:
    def __init__(self):
        print("Singleton Constructor called. New Object created.")

    @staticmethod
    def main(args):
        s1 = NoSingleton()
        s2 = NoSingleton()

        print(str(s1 is s2).lower())


if __name__ == "__main__":
    # call the same demo as Java main
    NoSingleton.main(None)
