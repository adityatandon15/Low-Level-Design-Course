from .HttpRequest import HttpRequest
from .HttpRequestDirector import HttpRequestDirector


class Main:
    @staticmethod
    def main(args):
        # Normal Request from Builder Directly
        normalRequest = (HttpRequest.HttpRequestBuilder()
            .withUrl("https://api.example.com")
            .withMethod("POST")
            .withHeader("Content-Type", "application/json")
            .withHeader("Accept", "application/json")
            .withQueryParams("key", "12345")
            .withBody("{\"name\": \"Aditya\"}")
            .withTimeout(60)
            .build())

        normalRequest.execute()  # Guaranteed to be in a consistent state

        print("\n----------------------------\n")

        getRequest = HttpRequestDirector.createGetRequest("https://api.example.com/users")
        getRequest.execute()

        print("\n----------------------------\n")

        postRequest = HttpRequestDirector.createJsonPostRequest(
            "https://api.example.com/users",
            "{\"name\": \"Aditya\", \"email\": \"aditya@example.com\"}")
        postRequest.execute()


if __name__ == "__main__":
    import sys
    Main.main(sys.argv[1:])
