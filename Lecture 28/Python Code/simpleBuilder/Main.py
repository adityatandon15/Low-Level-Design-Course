from .HttpRequest import HttpRequest


class Main:
    @staticmethod
    def main(args):
        # Using Builder Pattern (nested class)
        request = (HttpRequest.HttpRequestBuilder()
            .withUrl("https://api.example2.com")
            .withMethod("POST")
            .withHeader("Content-Type", "application/json")
            .withHeader("Accept", "application/json")
            .withQueryParams("key", "12345")
            .withBody("{\"name\": \"Aditya\"}")
            .withTimeout(60)
            .build())

        request.execute()  # Guaranteed to be in a consistent state


if __name__ == "__main__":
    import sys
    Main.main(sys.argv[1:])
