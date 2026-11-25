# Java version of the given C++ Notification System code
from abc import ABC, abstractmethod

# ============================
#       Notification & Decorators
# =============================


class INotification(ABC):
    @abstractmethod
    def getContent(self):
        pass


# Concrete Notification: simple text notification.
class SimpleNotification(INotification):
    def __init__(self, msg):
        self._text = msg

    def getContent(self):
        return self._text


# Abstract Decorator: wraps a Notification object.
class INotificationDecorator(INotification):
    def __init__(self, n):
        self.notification = n


# Decorator to add a timestamp to the content.
class TimestampDecorator(INotificationDecorator):
    def __init__(self, n):
        super().__init__(n)

    def getContent(self):
        return "[2025-04-13 14:22:00] " + self.notification.getContent()


# Decorator to append a signature to the content.
class SignatureDecorator(INotificationDecorator):
    def __init__(self, n, sig):
        super().__init__(n)
        self._signature = sig

    def getContent(self):
        return self.notification.getContent() + "\n-- " + self._signature + "\n\n"


# ============================
#   Observer Pattern Components
# =============================

# Observer interface: each observer gets an update with a Notification pointer.
class IObserver(ABC):
    @abstractmethod
    def update(self):
        pass


class IObservable(ABC):
    @abstractmethod
    def addObserver(self, observer):
        pass

    @abstractmethod
    def removeObserver(self, observer):
        pass

    @abstractmethod
    def notifyObservers(self):
        pass


# Concrete Observable
class NotificationObservable(IObservable):
    def __init__(self):
        self._observers = []
        self._currentNotification = None

    def addObserver(self, obs):
        self._observers.append(obs)

    def removeObserver(self, obs):
        if obs in self._observers:
            self._observers.remove(obs)

    def notifyObservers(self):
        for obs in self._observers:
            obs.update()

    def setNotification(self, notification):
        self._currentNotification = notification
        self.notifyObservers()

    def getNotification(self):
        return self._currentNotification

    def getNotificationContent(self):
        return self._currentNotification.getContent()


# ============================
#        NotificationService
# =============================

# The NotificationService manages notifications. It keeps track of notifications.
# Any client code will interact with this service.

# Singleton class
class NotificationService:
    _instance = None

    def __init__(self):
        self._observable = NotificationObservable()
        self._notifications = []

    @staticmethod
    def getInstance():
        if NotificationService._instance is None:
            NotificationService._instance = NotificationService()
        return NotificationService._instance

    # Expose the observable so observers can attach.
    def getObservable(self):
        return self._observable

    # Creates a new Notification and notifies observers.
    def sendNotification(self, notification):
        self._notifications.append(notification)
        self._observable.setNotification(notification)


# ============================
#        ConcreteObservers
# =============================
class Logger(IObserver):
    def __init__(self, observable=None):
        if observable is None:
            self._notificationObservable = NotificationService.getInstance().getObservable()
            self._notificationObservable.addObserver(self)
        else:
            self._notificationObservable = observable
            self._notificationObservable.addObserver(self)

    def update(self):
        print("Logging New Notification : \n" + self._notificationObservable.getNotificationContent())


# ============================
#   Strategy Pattern Components (Concrete Observer 2)
# =============================


class INotificationStrategy(ABC):
    @abstractmethod
    def sendNotification(self, content):
        pass


class EmailStrategy(INotificationStrategy):
    def __init__(self, emailId):
        self._emailId = emailId

    def sendNotification(self, content):
        # Simulate the process of sending an email notification,
        # representing the dispatch of messages to users via email.
        print("Sending email Notification to: " + self._emailId + "\n" + content)


class SMSStrategy(INotificationStrategy):
    def __init__(self, mobileNumber):
        self._mobileNumber = mobileNumber

    def sendNotification(self, content):
        # Simulate the process of sending an SMS notification,
        # representing the dispatch of messages to users via SMS.
        print("Sending SMS Notification to: " + self._mobileNumber + "\n" + content)


class PopUpStrategy(INotificationStrategy):
    def sendNotification(self, content):
        # Simulate the process of sending popup notification.
        print("Sending Popup Notification: \n" + content)


class NotificationEngine(IObserver):
    def __init__(self, observable=None):
        self._notificationStrategies = []
        if observable is None:
            self._notificationObservable = NotificationService.getInstance().getObservable()
            self._notificationObservable.addObserver(self)
        else:
            self._notificationObservable = observable

    def addNotificationStrategy(self, ns):
        self._notificationStrategies.append(ns)

    # Can have RemoveNotificationStrategy as well.

    def update(self):
        notificationContent = self._notificationObservable.getNotificationContent()
        for strategy in self._notificationStrategies:
            strategy.sendNotification(notificationContent)


class NotificationSystemUpdated:
    @staticmethod
    def main(args=None):

        # Create NotificationService.
        notificationService = NotificationService.getInstance()

        # Create Logger Observer
        logger = Logger()

        # Create NotificationEngine observers.
        notificationEngine = NotificationEngine()

        notificationEngine.addNotificationStrategy(EmailStrategy("random.person@gmail.com"))
        notificationEngine.addNotificationStrategy(SMSStrategy("+91 9876543210"))
        notificationEngine.addNotificationStrategy(PopUpStrategy())

        notification = SimpleNotification("Your order has been shipped!")
        notification = TimestampDecorator(notification)
        notification = SignatureDecorator(notification, "Customer Care")

        notificationService.sendNotification(notification)


if __name__ == "__main__":
    NotificationSystemUpdated.main()
