from abc import ABC, abstractmethod


class ISubscriber(ABC):
    @abstractmethod
    def update(self):
        pass


# Observable interface: a YouTube channel interface
class IChannel(ABC):
    @abstractmethod
    def subscribe(self, subscriber):
        pass

    @abstractmethod
    def unsubscribe(self, subscriber):
        pass

    @abstractmethod
    def notifySubscribers(self):
        pass


# Concrete Subject: a YouTube channel that observers can subscribe to
class Channel(IChannel):
    def __init__(self, name):
        self._name = name
        self._subscribers = []
        self._latestVideo = None

    def subscribe(self, subscriber):
        if subscriber not in self._subscribers:
            self._subscribers.append(subscriber)

    def unsubscribe(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)

    def notifySubscribers(self):
        for sub in self._subscribers:
            sub.update()

    def uploadVideo(self, title):
        self._latestVideo = title
        print("\n[" + self._name + " uploaded \"" + title + "\"]")
        self.notifySubscribers()

    def getVideoData(self):
        return "\nCheckout our new Video : " + self._latestVideo + "\n"


# Concrete Observer: represents a subscriber to the channel
class Subscriber(ISubscriber):
    def __init__(self, name, channel):
        self._name = name
        self._channel = channel

    def update(self):
        print("Hey " + self._name + "," + self._channel.getVideoData())


class ObserverDesignPattern:
    @staticmethod
    def main(args=None):
        # Create a channel and subscribers
        channel = Channel("CoderArmy")

        subs1 = Subscriber("Varun", channel)
        subs2 = Subscriber("Tarun", channel)

        # Varun and Tarun subscribe to CoderArmy
        channel.subscribe(subs1)
        channel.subscribe(subs2)

        # Upload a video: both Varun and Tarun are notified
        channel.uploadVideo("Observer Pattern Tutorial")

        # Varun unsubscribes; Tarun remains subscribed
        channel.unsubscribe(subs1)

        # Upload another video: only Tarun is notified
        channel.uploadVideo("Decorator Pattern Tutorial")


if __name__ == "__main__":
    ObserverDesignPattern.main()
