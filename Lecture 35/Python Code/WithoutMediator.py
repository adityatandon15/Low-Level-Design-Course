# Each User knows *all* the others directly.
# If you have N users, you wind up wiring N*(N–1)/2 connections,
# and every new feature (mute, private send, logging...) lives in User too.
class User:
    def __init__(self, n):
        self.name = n
        self.peers = []
        self.mutedUsers = []

    # must manually connect every pair → N^2 wiring
    def addPeer(self, u):
        self.peers.append(u)

    # duplication: everyone has its own mute list
    def mute(self, userToMute):
        self.mutedUsers.append(userToMute)

    # broadcast to all peers
    def send(self, msg):
        print("[" + self.name + " broadcasts]: " + msg)
        for peer in self.peers:

            # if they have muted me dont send.
            if not peer.isMuted(self.name):
                peer.receive(self.name, msg)

    def isMuted(self, userName):
        for mutedName in self.mutedUsers:
            if mutedName == userName:
                return True
        return False

    # private send - duplicated in every class
    def sendTo(self, target, msg):
        print("[" + self.name + "→" + target.name + "]: " + msg)
        if not target.isMuted(self.name):
            target.receive(self.name, msg)

    def receive(self, from_, msg):
        print("    " + self.name + " got from " + from_ + ": " + msg)


class WithoutMediator:
    @staticmethod
    def main(args=None):
        # create users
        user1 = User("Rohan")
        user2 = User("Neha")
        user3 = User("Mohan")

        # wire up peers (each knows each other) → n*(n-1)/2 connections
        user1.addPeer(user2)
        user2.addPeer(user1)

        user1.addPeer(user3)
        user3.addPeer(user1)

        user2.addPeer(user3)
        user3.addPeer(user2)

        # mute example: Mohan mutes Rohan (Hence Rohan add Mohan to its muted list).
        user1.mute("Mohan")

        # broadcast
        user1.send("Hello everyone!")

        # private
        user3.sendTo(user2, "Hey Neha!")


if __name__ == "__main__":
    WithoutMediator.main()
