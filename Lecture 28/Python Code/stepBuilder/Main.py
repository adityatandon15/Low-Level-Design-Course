from .HttpRequest import HttpRequest


class Main:
    @staticmethod
    def main(args):
        stepRequest = (HttpRequest.HttpRequestStepBuilder.getBuilder()
            .withUrl("https://api.example.com/products")
            .withMethod("POST")
            .withHeader("Content-Type", "application/json")
            .withBody("{\"product\": \"Laptop\", \"price\": 49999}")
            .withTimeout(45)
            .build())

        stepRequest.execute()


if __name__ == "__main__":
    import sys
    Main.main(sys.argv[1:])
