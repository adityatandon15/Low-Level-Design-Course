class HttpRequest:
    # Private constructor - can only be accessed by the Builder
    def __init__(self):
        self.headers = {}
        self.queryParams = {}
        self.body = ""
        self.url = None
        self.method = None
        self.timeout = 0  # in seconds; Java int default

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

        if self.body is not None and self.body != "":
            print("Body: " + self.body)

        print("Timeout: " + str(self.timeout) + " seconds")
        print("Request executed successfully!")

    # Builder class as a nested class to access private members
    class HttpRequestBuilder:
        def __init__(self):
            self.req = HttpRequest()

        # Method chaining
        def withUrl(self, u):
            self.req.url = u
            return self

        def withMethod(self, method):
            self.req.method = method
            return self

        def withHeader(self, key, value):
            self.req.headers[key] = value
            return self

        def withQueryParams(self, key, value):
            self.req.queryParams[key] = value
            return self

        def withBody(self, body):
            self.req.body = body
            return self

        def withTimeout(self, timeout):
            self.req.timeout = timeout
            return self

        # Build method to create the immutable HttpRequest object
        def build(self):
            # Validation logic can be added here
            if self.req.url is None or self.req.url == "":
                raise RuntimeError("URL cannot be empty")
            return self.req
