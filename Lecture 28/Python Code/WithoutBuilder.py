class HttpRequest:
    # url                     required
    # method                  required
    # headers
    # queryParams
    # body
    # timeout                 required

    # Telescoping constructors (1-arg through 6-arg).
    # Java needs a new overload for every extra field; each one repeats the
    # assignments below. Python has no overloads, so one signature stands in
    # for all six. Positional calls still pass every earlier field to set a later one.
    #
    # Constructor with only required parameter (1-arg)
    # 2 - args
    # 3 - args
    # 4 - args
    # 5 - args
    # 6 - args
    def __init__(self, url, method=None, timeout=None, headers=None, queryParams=None, body=None):
        self.url = url
        self.method = "GET" if method is None else method       # Default method
        self.timeout = 30 if timeout is None else timeout       # Default timeout
        self.headers = {} if headers is None else headers
        self.queryParams = {} if queryParams is None else queryParams
        self.body = body

    # Setters (leads to mutable object)
    def setUrl(self, url):
        self.url = url

    def setMethod(self, method):
        self.method = method

    def addHeader(self, key, value):
        self.headers[key] = value

    def addQueryParam(self, key, value):
        self.queryParams[key] = value

    def setBody(self, body):
        self.body = body

    def setTimeout(self, timeout):
        self.timeout = timeout

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


class WithoutBuilder:
    @staticmethod
    def main(args):
        # Using constructors (telescoping constructor problem)
        request1 = HttpRequest("https://api.example.com")
        request2 = HttpRequest("https://api.example.com", "POST")
        request3 = HttpRequest("https://api.example.com", "PUT", 60)

        # Using setters (mutable object problem)
        request4 = HttpRequest("https://api.example.com")
        request4.setMethod("POST")
        request4.addHeader("Content-Type", "application/json")
        request4.addQueryParam("key", "12345")
        request4.setBody("{\"name\": \"Aditya\"}")
        request4.setTimeout(60)

        # The problem: what if we forgot to set an important field?
        request4.execute()


if __name__ == "__main__":
    import sys
    WithoutBuilder.main(sys.argv[1:])
