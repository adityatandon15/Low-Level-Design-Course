from abc import ABC, abstractmethod

# --- Strategy Interface for Walk ---
class WalkableRobot(ABC):
    @abstractmethod
    def walk(self):
        pass


# --- Concrete Strategies for walk ---
class NormalWalk(WalkableRobot):
    def walk(self):
        print("Walking normally...")


class NoWalk(WalkableRobot):
    def walk(self):
        print("Cannot walk.")


# --- Strategy Interface for Talk ---
class TalkableRobot(ABC):
    @abstractmethod
    def talk(self):
        pass


# --- Concrete Strategies for Talk ---
class NormalTalk(TalkableRobot):
    def talk(self):
        print("Talking normally...")


class NoTalk(TalkableRobot):
    def talk(self):
        print("Cannot talk.")


# --- Strategy Interface for Fly ---
class FlyableRobot(ABC):
    @abstractmethod
    def fly(self):
        pass


class NormalFly(FlyableRobot):
    def fly(self):
        print("Flying normally...")


class NoFly(FlyableRobot):
    def fly(self):
        print("Cannot fly.")


# --- Robot Base Class ---
class Robot(ABC):
    def __init__(self, w, t, f):
        self.walkBehavior = w
        self.talkBehavior = t
        self.flyBehavior = f

    def walk(self):
        self.walkBehavior.walk()

    def talk(self):
        self.talkBehavior.talk()

    def fly(self):
        self.flyBehavior.fly()

    @abstractmethod
    def projection(self):  # Abstract method for subclasses
        pass


# --- Concrete Robot Types ---
class CompanionRobot(Robot):
    def __init__(self, w, t, f):
        super().__init__(w, t, f)

    def projection(self):
        print("Displaying friendly companion features...")


class WorkerRobot(Robot):
    def __init__(self, w, t, f):
        super().__init__(w, t, f)

    def projection(self):
        print("Displaying worker efficiency stats...")


# --- Main Function ---
class StrategyDesignPattern:
    @staticmethod
    def main(args):
        robot1 = CompanionRobot(NormalWalk(), NormalTalk(), NoFly())
        robot1.walk()
        robot1.talk()
        robot1.fly()
        robot1.projection()

        print("--------------------")

        robot2 = WorkerRobot(NoWalk(), NoTalk(), NormalFly())
        robot2.walk()
        robot2.talk()
        robot2.fly()
        robot2.projection()


if __name__ == "__main__":
    # call the same demo as Java main
    StrategyDesignPattern.main(None)
