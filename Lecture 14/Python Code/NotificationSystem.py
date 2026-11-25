# Java version of the C++ Notification System using Decorator, Observer, Strategy, and Singleton Patterns
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
        for observer in self._observers:
            observer.update()

    def setNotification(self, notification):
        self._currentNotification = notification
        self.notifyObservers()

    def getNotification(self):
        return self._currentNotification

    def getNotificationContent(self):
        return self._currentNotification.getContent()


# Concrete Observer 1
class Logger(IObserver):
    def __init__(self, observable):
        self._notificationObservable = observable

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
        print("Sending email Notification to: " + self._emailId + "\n" + content)


class SMSStrategy(INotificationStrategy):
    def __init__(self, mobileNumber):
        self._mobileNumber = mobileNumber

    def sendNotification(self, content):
        print("Sending SMS Notification to: " + self._mobileNumber + "\n" + content)


class PopUpStrategy(INotificationStrategy):
    def sendNotification(self, content):
        print("Sending Popup Notification: \n" + content)


class NotificationEngine(IObserver):
    def __init__(self, observable):
        self._notificationObservable = observable
        self._notificationStrategies = []

    def addNotificationStrategy(self, ns):
        self._notificationStrategies.append(ns)

    def update(self):
        notificationContent = self._notificationObservable.getNotificationContent()
        for strategy in self._notificationStrategies:
            strategy.sendNotification(notificationContent)


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

    def getObservable(self):
        return self._observable

    def sendNotification(self, notification):
        self._notifications.append(notification)
        self._observable.setNotification(notification)


class NotificationSystem:
    @staticmethod
    def main(args=None):

        # Create NotificationService.
        notificationService = NotificationService.getInstance()

        # Get Observable
        notificationObservable = notificationService.getObservable()

        # Create Logger Observer
        logger = Logger(notificationObservable)

        # Create NotificationEngine observers.
        notificationEngine = NotificationEngine(notificationObservable)

        notificationEngine.addNotificationStrategy(EmailStrategy("random.person@gmail.com"))
        notificationEngine.addNotificationStrategy(SMSStrategy("+91 9876543210"))
        notificationEngine.addNotificationStrategy(PopUpStrategy())

        # Attach these observers.
        notificationObservable.addObserver(logger)
        notificationObservable.addObserver(notificationEngine)

        # Create a notification with decorators.
        notification = SimpleNotification("Your order has been shipped!")
        notification = TimestampDecorator(notification)
        notification = SignatureDecorator(notification, "Customer Care")

        notificationService.sendNotification(notification)


if __name__ == "__main__":
    NotificationSystem.main()
