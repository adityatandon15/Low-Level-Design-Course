from abc import ABC, abstractmethod


# ─────────────── Mediator Interface ───────────────
class IMediator(ABC):
    @abstractmethod
    def registerColleague(self, c):
        pass

    @abstractmethod
    def send(self, from_, msg):
        pass

    @abstractmethod
    def sendPrivate(self, from_, to, msg):
        pass


# ─────────────── Colleague Interface ───────────────
class Colleague(ABC):
    def __init__(self, m):
        self.mediator = m
        self.mediator.registerColleague(self)

    @abstractmethod
    def getName(self):
        pass

    @abstractmethod
    def send(self, msg):
        pass

    @abstractmethod
    def sendPrivate(self, to, msg):
        pass

    @abstractmethod
    def receive(self, from_, msg):
        pass


# Simple Pair class
class Pair:
    def __init__(self, first, second):
        self.first = first
        self.second = second


# ─────────────── Concrete Mediator ───────────────
class ChatMediator(IMediator):
    def __init__(self):
        self.colleagues = []
        self.mutes = []  # (muter, muted)

    def registerColleague(self, c):
        self.colleagues.append(c)

    def mute(self, who, whom):
        self.mutes.append(Pair(who, whom))

    def send(self, from_, msg):
        print("[" + from_ + " broadcasts]: " + msg)
        for c in self.colleagues:
            # Don't send msg to itself.
            if c.getName() == from_:
                continue

            isMuted = False
            # Ignore if person is muted
            for p in self.mutes:
                if from_ == p.second and c.getName() == p.first:
                    isMuted = True
                    break
            if not isMuted:
                c.receive(from_, msg)

    def sendPrivate(self, from_, to, msg):
        print("[" + from_ + "→" + to + "]: " + msg)
        for c in self.colleagues:
            if c.getName() == to:
                for p in self.mutes:
                    # Dont send if muted
                    if from_ == p.second and to == p.first:
                        print("\n[Message is muted]\n")
                        return
                c.receive(from_, msg)
                return
        print("[Mediator] User \"" + to + "\" not found]")


# ─────────────── Concrete Colleague ───────────────
class User(Colleague):
    def __init__(self, n, m):
        self.name = n
        super().__init__(m)

    def getName(self):
        return self.name

    def send(self, msg):
        self.mediator.send(self.name, msg)

    def sendPrivate(self, to, msg):
        self.mediator.sendPrivate(self.name, to, msg)

    def receive(self, from_, msg):
        print("    " + self.name + " got from " + from_ + ": " + msg)


# ─────────────── Demo ───────────────
class MediatorPattern:
    @staticmethod
    def main(args=None):
        chatRoom = ChatMediator()

        user1 = User("Rohan", chatRoom)
        user2 = User("Neha", chatRoom)
        user3 = User("Mohan", chatRoom)

        # Rohan mutes Mohan
        chatRoom.mute("Rohan", "Mohan")

        # broadcast from Rohan
        user1.send("Hello Everyone!")

        # private from Mohan to Neha
        user3.sendPrivate("Neha", "Hey Neha!")


if __name__ == "__main__":
    MediatorPattern.main()
