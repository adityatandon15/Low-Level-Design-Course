# Exception Rule:
# A subclass should throw fewer or narrower exceptions
# (but not additional or broader exceptions) than the parent.
# Java enforces this only for checked Exceptions.

# └── java.lang.Exception                        // Conditions your application might want to catch
#     ├── java.io.IOException                    // Checked I/O failures
#     │   ├── java.io.FileNotFoundException
#     │   ├── java.io.EOFException
#     │   └── java.net.MalformedURLException
#     ├── java.lang.ClassNotFoundException       // Checked reflect/… failures
#     ├── java.lang.InterruptedException         // Checked thread interruption
#     ├── java.sql.SQLException                  // Checked SQL/database errors
#     ├── java.text.ParseException               // Checked parsing errors
#     └── java.lang.RuntimeException             // Unchecked; subclasses may be thrown anywhere
#         ├── java.lang.ArithmeticException      // e.g. divide by zero
#         ├── java.lang.NullPointerException
#         ├── java.lang.ArrayIndexOutOfBoundsException
#         ├── java.lang.StringIndexOutOfBoundsException
#         ├── java.lang.IllegalArgumentException
#         │    └── java.lang.NumberFormatException
#         ├── java.lang.IllegalStateException
#         ├── java.lang.UnsupportedOperationException
#         └── java.lang.IndexOutOfBoundsException // parent of the two “…OutOfBounds” above

class RuntimeException(Exception):
    def getMessage(self):
        return self.args[0] if self.args else None


class ArithmeticException(RuntimeException):
    pass


class Parent:
    # throws RuntimeException
    def getValue(self):
        raise RuntimeException("Parent error")


# Subclass overrides getValue and throws the narrower ChildException
class Child(Parent):
    # throws ArithmeticException
    def getValue(self):
        raise ArithmeticException("Child error")
        # throw new Exception("Child error"); // This is wrong & not allowed


# Client that invokes getValue and catches the parent exception type
class Client:
    def __init__(self, p):
        self._p = p

    def takeValue(self):
        try:
            self._p.getValue()
        except RuntimeException as e:
            print("RuntimeException occurred: " + e.getMessage())


class ExceptionRule:
    @staticmethod
    def main(args):
        parent = Parent()
        child = Child()

        client = Client(parent)
        # Client client = new Client(child);

        client.takeValue()


if __name__ == "__main__":
    # call the same demo as Java main
    ExceptionRule.main(None)
