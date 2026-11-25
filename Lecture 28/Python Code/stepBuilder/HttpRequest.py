from abc import ABC, abstractmethod


class HttpRequest:
    # Private constructor - can only be accessed by the Builder
    def __init__(self):
        self.headers = {}
        self.queryParams = {}
        self.body = ""
        self.url = None
        self.method = None
        self.timeout = 0  # in seconds

    # Method to execute the HTTP request
    def execute(self):
        print("Executing " + self.method + " request to " + self.url)

        if self.queryParams:
            print("Query Parameters:")
            for key, value in self.queryParams.items():
                print("  " + key + "=" + value)

        print("Headers:")
        for key, value in self.headers.items():
            print("  " + key + ": " + value)

        if self.body != "":
            print("Body: " + self.body)

        print("Timeout: " + str(self.timeout) + " seconds")
        print("Request executed successfully!")

    # Nested Step interfaces
    class UrlStep(ABC):
        @abstractmethod
        def withUrl(self, url):
            pass

    class MethodStep(ABC):
        @abstractmethod
        def withMethod(self, method):
            pass

    class HeaderStep(ABC):
        @abstractmethod
        def withHeader(self, key, value):
            pass

    class OptionalStep(ABC):
        @abstractmethod
        def withBody(self, body):
            pass

        @abstractmethod
        def withTimeout(self, timeout):
            pass

        @abstractmethod
        def build(self):
            pass

    # Concrete step builder as static nested class
    class HttpRequestStepBuilder(UrlStep, MethodStep, HeaderStep, OptionalStep):
        def __init__(self):
            self.req = HttpRequest()

        # UrlStep implementation
        def withUrl(self, url):
            self.req.url = url
            return self

        # MethodStep implementation
        def withMethod(self, method):
            self.req.method = method
            return self

        # HeaderStep implementation
        def withHeader(self, key, value):
            self.req.headers[key] = value
            return self

        # OptionalStep implementation
        def withBody(self, body):
            self.req.body = body
            return self

        def withTimeout(self, timeout):
            self.req.timeout = timeout
            return self

        def build(self):
            if self.req.url is None or self.req.url == "":
                raise RuntimeError("URL cannot be empty")
            return self.req

        # Static method to start the building process
        @staticmethod
        def getBuilder():
            return HttpRequest.HttpRequestStepBuilder()
