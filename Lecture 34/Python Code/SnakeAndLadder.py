import random
from abc import ABC, abstractmethod
from collections import deque
from enum import Enum


# Mirrors java.util.Scanner over input() so nextInt/nextLine keep the same prompts and token rules.
class Scanner:
    def __init__(self):
        self._tokens = []
        self._pending_line = False

    def nextInt(self):
        while not self._tokens:
            line = input()
            self._tokens = line.split()
            self._pending_line = True
        self._pending_line = True
        return int(self._tokens.pop(0))

    def nextLine(self):
        if self._pending_line:
            rest = " ".join(self._tokens)
            self._tokens = []
            self._pending_line = False
            return rest
        return input()

    def close(self):
        pass


# Observer Pattern
class IObserver(ABC):
    @abstractmethod
    def update(self, msg):
        pass


# Sample observer implementation
class SnakeAndLadderConsoleNotifier(IObserver):
    def update(self, msg):
        print("[NOTIFICATION] " + msg)


# Dice class
class Dice:
    def __init__(self, f):
        self.faces = f

    def roll(self):
        return int(random.random() * self.faces) + 1


# Base class for Snake and Ladder (both have start and end positions)
class BoardEntity(ABC):
    def __init__(self, start, end):
        self.startPosition = start
        self.endPosition = end

    def getStart(self):
        return self.startPosition

    def getEnd(self):
        return self.endPosition

    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def name(self):
        pass


# Snake class
class Snake(BoardEntity):
    def __init__(self, start, end):
        super().__init__(start, end)
        if end >= start:
            print("Invalid snake! End must be less than start.")

    def display(self):
        print("Snake: " + str(self.startPosition) + " -> " + str(self.endPosition))

    def name(self):
        return "SNAKE"


# Ladder class
class Ladder(BoardEntity):
    def __init__(self, start, end):
        super().__init__(start, end)
        if end <= start:
            print("Invalid ladder! End must be greater than start.")

    def display(self):
        print("Ladder: " + str(self.startPosition) + " -> " + str(self.endPosition))

    def name(self):
        return "LADDER"


# Board class
class Board:
    def __init__(self, s):
        self.size = s * s  # m*m board
        self.snakesAndLadders = []
        self.boardEntities = {}

    def canAddEntity(self, position):
        return position not in self.boardEntities

    def addBoardEntity(self, boardEntity):
        if self.canAddEntity(boardEntity.getStart()):
            self.snakesAndLadders.append(boardEntity)
            self.boardEntities[boardEntity.getStart()] = boardEntity

    def setupBoard(self, strategy):
        strategy.setupBoard(self)

    def getEntity(self, position):
        return self.boardEntities.get(position)

    def getBoardSize(self):
        return self.size

    def display(self):
        print("\n=== Board Configuration ===")
        print("Board Size: " + str(self.size) + " cells")

        snakeCount = 0
        ladderCount = 0
        for entity in self.snakesAndLadders:
            if entity.name() == "SNAKE":
                snakeCount += 1
            else:
                ladderCount += 1

        print("\nSnakes: " + str(snakeCount))
        for entity in self.snakesAndLadders:
            if entity.name() == "SNAKE":
                entity.display()

        print("\nLadders: " + str(ladderCount))
        for entity in self.snakesAndLadders:
            if entity.name() == "LADDER":
                entity.display()
        print("=========================")


# Strategy Pattern for Board Setup
class BoardSetupStrategy(ABC):
    @abstractmethod
    def setupBoard(self, board):
        pass


# Random Strategy with difficulty levels
class RandomBoardSetupStrategy(BoardSetupStrategy):
    class Difficulty(Enum):
        EASY = 1    # More ladders, fewer snakes
        MEDIUM = 2  # Equal snakes and ladders
        HARD = 3    # More snakes, fewer ladders

    def __init__(self, d):
        self.difficulty = d

    def setupWithProbability(self, board, snakeProbability):
        boardSize = board.getBoardSize()
        totalEntities = boardSize // 10  # Roughly 10% of board has entities

        for _i in range(totalEntities):
            prob = random.random()

            if prob < snakeProbability:
                # Add snake
                attempts = 0
                while attempts < 50:
                    start = int(random.random() * (boardSize - 10)) + 10
                    end = int(random.random() * (start - 1)) + 1

                    if board.canAddEntity(start):
                        board.addBoardEntity(Snake(start, end))
                        break
                    attempts += 1
            else:
                # Add ladder
                attempts = 0
                while attempts < 50:
                    start = int(random.random() * (boardSize - 10)) + 1
                    end = int(random.random() * (boardSize - start)) + start + 1

                    if board.canAddEntity(start) and end < boardSize:
                        board.addBoardEntity(Ladder(start, end))
                        break
                    attempts += 1

    def setupBoard(self, board):
        if self.difficulty == RandomBoardSetupStrategy.Difficulty.EASY:
            self.setupWithProbability(board, 0.3)  # 30% snakes, 70% ladders
        elif self.difficulty == RandomBoardSetupStrategy.Difficulty.MEDIUM:
            self.setupWithProbability(board, 0.5)  # 50% snakes, 50% ladders
        elif self.difficulty == RandomBoardSetupStrategy.Difficulty.HARD:
            self.setupWithProbability(board, 0.7)  # 70% snakes, 30% ladders


# Custom Strategy - User provides count
class CustomCountBoardSetupStrategy(BoardSetupStrategy):
    # Simple Pair class for Java
    class Pair:
        def __init__(self, first, second):
            self.first = first
            self.second = second

    def __init__(self, snakes, ladders, randomPositions):
        self.numSnakes = snakes
        self.numLadders = ladders
        self.randomPositions = randomPositions
        self.snakePositions = []
        self.ladderPositions = []

    def addSnakePosition(self, start, end):
        self.snakePositions.append(CustomCountBoardSetupStrategy.Pair(start, end))

    def addLadderPosition(self, start, end):
        self.ladderPositions.append(CustomCountBoardSetupStrategy.Pair(start, end))

    def setupBoard(self, board):
        if self.randomPositions:
            # Random placement with user-defined counts
            boardSize = board.getBoardSize()

            # Add snakes
            snakesAdded = 0
            while snakesAdded < self.numSnakes:
                start = int(random.random() * (boardSize - 10)) + 10
                end = int(random.random() * (start - 1)) + 1

                if board.canAddEntity(start):
                    board.addBoardEntity(Snake(start, end))
                    snakesAdded += 1

            # Add ladders
            laddersAdded = 0
            while laddersAdded < self.numLadders:
                start = int(random.random() * (boardSize - 10)) + 1
                end = int(random.random() * (boardSize - start)) + start + 1

                if board.canAddEntity(start) and end < boardSize:
                    board.addBoardEntity(Ladder(start, end))
                    laddersAdded += 1
        else:
            # User-defined positions
            for pos in self.snakePositions:
                if board.canAddEntity(pos.first):
                    board.addBoardEntity(Snake(pos.first, pos.second))

            for pos in self.ladderPositions:
                if board.canAddEntity(pos.first):
                    board.addBoardEntity(Ladder(pos.first, pos.second))


# Standard Board Strategy - Traditional Snake & Ladder positions
class StandardBoardSetupStrategy(BoardSetupStrategy):
    def setupBoard(self, board):
        # Only works for 10x10 board (100 cells)
        if board.getBoardSize() != 100:
            print("Standard setup only works for 10x10 board!")
            return

        # Standard snake positions (based on traditional board)
        board.addBoardEntity(Snake(99, 54))
        board.addBoardEntity(Snake(95, 75))
        board.addBoardEntity(Snake(92, 88))
        board.addBoardEntity(Snake(89, 68))
        board.addBoardEntity(Snake(74, 53))
        board.addBoardEntity(Snake(64, 60))
        board.addBoardEntity(Snake(62, 19))
        board.addBoardEntity(Snake(49, 11))
        board.addBoardEntity(Snake(46, 25))
        board.addBoardEntity(Snake(16, 6))

        # Standard ladder positions
        board.addBoardEntity(Ladder(2, 38))
        board.addBoardEntity(Ladder(7, 14))
        board.addBoardEntity(Ladder(8, 31))
        board.addBoardEntity(Ladder(15, 26))
        board.addBoardEntity(Ladder(21, 42))
        board.addBoardEntity(Ladder(28, 84))
        board.addBoardEntity(Ladder(36, 44))
        board.addBoardEntity(Ladder(51, 67))
        board.addBoardEntity(Ladder(71, 91))
        board.addBoardEntity(Ladder(78, 98))
        board.addBoardEntity(Ladder(87, 94))


# Player class
class SnakeAndLadderPlayer:
    def __init__(self, playerId, n):
        self.playerId = playerId
        self.name = n
        self.position = 0
        self.score = 0

    # Getters and Setters
    def getName(self):
        return self.name

    def getPosition(self):
        return self.position

    def setPosition(self, pos):
        self.position = pos

    def getScore(self):
        return self.score

    def incrementScore(self):
        self.score += 1


# Strategy Pattern for game rules
class SnakeAndLadderRules(ABC):
    @abstractmethod
    def isValidMove(self, currentPos, diceValue, boardSize):
        pass

    @abstractmethod
    def calculateNewPosition(self, currentPos, diceValue, board):
        pass

    @abstractmethod
    def checkWinCondition(self, position, boardSize):
        pass


# Standard rules
class StandardSnakeAndLadderRules(SnakeAndLadderRules):
    def isValidMove(self, currentPos, diceValue, boardSize):
        return (currentPos + diceValue) <= boardSize

    def calculateNewPosition(self, currentPos, diceValue, board):
        newPos = currentPos + diceValue
        entity = board.getEntity(newPos)

        if entity is not None:
            return entity.getEnd()
        return newPos

    def checkWinCondition(self, position, boardSize):
        return position == boardSize


# Game class
class SnakeAndLadderGame:
    def __init__(self, b, d):
        self.board = b
        self.dice = d
        self.players = deque()
        self.rules = StandardSnakeAndLadderRules()
        self.observers = []
        self.gameOver = False

    def addPlayer(self, player):
        self.players.append(player)

    def addObserver(self, observer):
        self.observers.append(observer)

    def notify(self, msg):
        for observer in self.observers:
            observer.update(msg)

    def displayPlayerPositions(self):
        print("\n=== Current Positions ===")
        for player in self.players:
            print(player.getName() + ": " + str(player.getPosition()))
        print("=======================")

    def play(self):
        if len(self.players) < 2:
            print("Need at least 2 players!")
            return

        self.notify("Game started")

        self.board.display()

        scanner = Scanner()

        while not self.gameOver:
            currentPlayer = self.players[0]

            print("\n" + currentPlayer.getName() + "'s turn. Press Enter to roll dice...")
            scanner.nextLine()

            diceValue = self.dice.roll()
            print("Rolled: " + str(diceValue))

            currentPos = currentPlayer.getPosition()

            if self.rules.isValidMove(currentPos, diceValue, self.board.getBoardSize()):
                intermediatePos = currentPos + diceValue
                newPos = self.rules.calculateNewPosition(currentPos, diceValue, self.board)

                currentPlayer.setPosition(newPos)

                # Check if player encountered snake or ladder
                entity = self.board.getEntity(intermediatePos)
                if entity is not None:
                    isSnake = entity.name() == "SNAKE"
                    if isSnake:
                        print("Oh no! Snake at " + str(intermediatePos) + "! Going down to " + str(newPos))
                        self.notify(currentPlayer.getName() + " encountered snake at " + str(intermediatePos) + " now going down to " + str(newPos))
                    else:
                        print("Great! Ladder at " + str(intermediatePos) + "! Going up to " + str(newPos))
                        self.notify(currentPlayer.getName() + " encountered ladder at " + str(intermediatePos) + " now going up to " + str(newPos))

                self.notify(currentPlayer.getName() + " played. New Position : " + str(newPos))
                self.displayPlayerPositions()

                if self.rules.checkWinCondition(newPos, self.board.getBoardSize()):
                    print("\n" + currentPlayer.getName() + " wins!")
                    currentPlayer.incrementScore()

                    self.notify("Game Ended. Winner is : " + currentPlayer.getName())
                    self.gameOver = True
                else:
                    # Move player to back of queue
                    self.players.popleft()
                    self.players.append(currentPlayer)
            else:
                print("Need exact roll to reach " + str(self.board.getBoardSize()) + "!")
                # Move player to back of queue
                self.players.popleft()
                self.players.append(currentPlayer)

        scanner.close()


# Factory Pattern
class SnakeAndLadderGameFactory:
    @staticmethod
    def createStandardGame():
        board = Board(10)  # Standard 10x10 board
        strategy = StandardBoardSetupStrategy()
        board.setupBoard(strategy)

        dice = Dice(6)  # Standard 6-faced dice

        return SnakeAndLadderGame(board, dice)

    @staticmethod
    def createRandomGame(boardSize, difficulty):
        board = Board(boardSize)
        strategy = RandomBoardSetupStrategy(difficulty)
        board.setupBoard(strategy)

        dice = Dice(6)

        return SnakeAndLadderGame(board, dice)

    @staticmethod
    def createCustomGame(boardSize, strategy):
        board = Board(boardSize)
        board.setupBoard(strategy)

        dice = Dice(6)

        return SnakeAndLadderGame(board, dice)


# Main class for Snake and Ladder
class SnakeAndLadder:
    @staticmethod
    def main(args=None):
        print("=== SNAKE AND LADDER GAME ===")

        game = None
        board = None

        print("Choose game setup:")
        print("1. Standard Game (10x10 board with traditional positions)")
        print("2. Random Game with Difficulty")
        print("3. Custom Game")

        scanner = Scanner()
        choice = scanner.nextInt()

        if choice == 1:
            # Standard game
            game = SnakeAndLadderGameFactory.createStandardGame()
            board = Board(10)

        elif choice == 2:
            # Random game with difficulty
            print("Enter board size (e.g., 10 for 10x10 board): ", end="")
            boardSize = scanner.nextInt()

            print("Choose difficulty:")
            print("1. Easy (more ladders)")
            print("2. Medium (balanced)")
            print("3. Hard (more snakes)")

            diffChoice = scanner.nextInt()

            if diffChoice == 1:
                diff = RandomBoardSetupStrategy.Difficulty.EASY
            elif diffChoice == 2:
                diff = RandomBoardSetupStrategy.Difficulty.MEDIUM
            elif diffChoice == 3:
                diff = RandomBoardSetupStrategy.Difficulty.HARD
            else:
                diff = RandomBoardSetupStrategy.Difficulty.MEDIUM

            game = SnakeAndLadderGameFactory.createRandomGame(boardSize, diff)
            board = Board(boardSize)

        elif choice == 3:
            # Custom game
            print("Enter board size (e.g., 10 for 10x10 board): ", end="")
            boardSize = scanner.nextInt()

            print("Choose custom setup type:")
            print("1. Specify counts only (random placement)")
            print("2. Specify exact positions")

            customChoice = scanner.nextInt()

            if customChoice == 1:
                print("Enter number of snakes: ", end="")
                numSnakes = scanner.nextInt()
                print("Enter number of ladders: ", end="")
                numLadders = scanner.nextInt()

                strategy = CustomCountBoardSetupStrategy(numSnakes, numLadders, True)
                game = SnakeAndLadderGameFactory.createCustomGame(boardSize, strategy)

            else:
                print("Enter number of snakes: ", end="")
                numSnakes = scanner.nextInt()
                print("Enter number of ladders: ", end="")
                numLadders = scanner.nextInt()

                strategy = CustomCountBoardSetupStrategy(numSnakes, numLadders, False)

                # Get snake positions
                for i in range(numSnakes):
                    print("Enter snake " + str(i + 1) + " start and end positions: ", end="")
                    start = scanner.nextInt()
                    end = scanner.nextInt()
                    strategy.addSnakePosition(start, end)

                # Get ladder positions
                for i in range(numLadders):
                    print("Enter ladder " + str(i + 1) + " start and end positions: ", end="")
                    start = scanner.nextInt()
                    end = scanner.nextInt()
                    strategy.addLadderPosition(start, end)

                game = SnakeAndLadderGameFactory.createCustomGame(boardSize, strategy)

            board = Board(boardSize)

        if game is None:
            print("Invalid choice!")
            scanner.close()
            return

        # Add observer
        notifier = SnakeAndLadderConsoleNotifier()
        game.addObserver(notifier)

        # Create players
        print("Enter number of players: ", end="")
        numPlayers = scanner.nextInt()
        scanner.nextLine()  # consume newline

        for i in range(numPlayers):
            print("Enter name for player " + str(i + 1) + ": ", end="")
            name = scanner.nextLine()
            player = SnakeAndLadderPlayer(i + 1, name)
            game.addPlayer(player)

        # Play the game
        game.play()

        scanner.close()


if __name__ == "__main__":
    SnakeAndLadder.main()
