from abc import ABC, abstractmethod


class Iterator(ABC):
    @abstractmethod
    def hasNext(self):
        pass

    @abstractmethod
    def next(self):
        pass


class Iterable(ABC):
    @abstractmethod
    def getIterator(self):
        pass


# Linked List
class LinkedList(Iterable):
    def __init__(self, value):
        self.data = value
        self.next = None

    def getIterator(self):
        return LinkedListIterator(self)


# Binary Tree
class BinaryTree(Iterable):
    def __init__(self, value):
        self.data = value
        self.left = None
        self.right = None

    def getIterator(self):
        return BinaryTreeInorderIterator(self)


# Song and Playlist
class Song:
    def __init__(self, t, a):
        self.title = t
        self.artist = a


class Playlist(Iterable):
    def __init__(self):
        self.songs = []

    def addSong(self, s):
        self.songs.append(s)

    def getIterator(self):
        return PlaylistIterator(self.songs)


# Concrete Iterators

class LinkedListIterator(Iterator):
    def __init__(self, head):
        self.current = head

    def hasNext(self):
        return self.current is not None

    def next(self):
        val = self.current.data
        self.current = self.current.next
        return val


class BinaryTreeInorderIterator(Iterator):
    def __init__(self, root):
        self.stk = []
        self.pushLefts(root)

    def pushLefts(self, node):
        while node is not None:
            self.stk.append(node)
            node = node.left

    def hasNext(self):
        return len(self.stk) != 0

    def next(self):
        node = self.stk.pop()
        val = node.data
        if node.right is not None:
            self.pushLefts(node.right)
        return val


class PlaylistIterator(Iterator):
    def __init__(self, v):
        self.vec = v
        self.index = 0

    def hasNext(self):
        return self.index < len(self.vec)

    def next(self):
        song = self.vec[self.index]
        self.index += 1
        return song


# Main
class IteratorPattern:
    @staticmethod
    def main(args):
        #------------------------------------------------
        # LinkedList: 1 → 2 → 3
        list_ = LinkedList(1)
        list_.next = LinkedList(2)
        list_.next.next = LinkedList(3)

        iterator1 = list_.getIterator()

        print("LinkedList contents: ", end="")
        while iterator1.hasNext():
            print(str(iterator1.next()) + " ", end="")
        print()

        #------------------------------------------------

        # BinaryTree:
        #    2
        #   / \
        #  1   3
        root = BinaryTree(2)
        root.left = BinaryTree(1)
        root.right = BinaryTree(3)

        iterator2 = root.getIterator()

        print("BinaryTree inorder: ", end="")
        while iterator2.hasNext():
            print(str(iterator2.next()) + " ", end="")
        print()

        #------------------------------------------------

        # Playlist
        playlist = Playlist()
        playlist.addSong(Song("Admirin You", "Karan Aujla"))
        playlist.addSong(Song("Husn", "Anuv Jain"))

        iterator3 = playlist.getIterator()

        print("Playlist songs:")
        while iterator3.hasNext():
            s = iterator3.next()
            print("  " + s.title + " by " + s.artist)


if __name__ == "__main__":
    import sys
    IteratorPattern.main(sys.argv[1:])
