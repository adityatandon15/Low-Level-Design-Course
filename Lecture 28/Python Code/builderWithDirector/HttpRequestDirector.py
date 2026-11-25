from .HttpRequest import HttpRequest


class HttpRequestDirector:
    @staticmethod
    def createGetRequest(url):
        return (HttpRequest.HttpRequestBuilder()
                .withUrl(url)
                .withMethod("GET")
                .build())

    # Creates a JSON POST request
    @staticmethod
    def createJsonPostRequest(url, jsonBody):
        return (HttpRequest.HttpRequestBuilder()
            .withUrl(url)
            .withMethod("POST")
            .withHeader("Content-Type", "application/json")
            .withHeader("Accept", "application/json")
            .withBody(jsonBody)
            .build())
