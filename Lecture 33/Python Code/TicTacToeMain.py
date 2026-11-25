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


# Observer Pattern - for future notification service
class IObserver(ABC):
    @abstractmethod
    def update(self, msg):
        pass


# Sample observer implementation
class ConsoleNotifier(IObserver):
    def update(self, msg):
        print("[Notification] " + msg)


# Symbol/Mark class
class Symbol:
    def __init__(self, m):
        self.mark = m

    def getMark(self):
        return self.mark


# Board class - Dumb object that only manages the grid
class Board:
    def __init__(self, s):
        self.size = s
        self.emptyCell = Symbol('-')
        self.grid = [[self.emptyCell for _ in range(self.size)] for _ in range(self.size)]

    def isCellEmpty(self, row, col):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        # Same Symbol instance marks every empty cell (Java reference equality).
        return self.grid[row][col] is self.emptyCell

    def placeMark(self, row, col, mark):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return False
        if not self.isCellEmpty(row, col):
            return False
        self.grid[row][col] = mark
        return True

    def getCell(self, row, col):
        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return self.emptyCell
        return self.grid[row][col]

    def getSize(self):
        return self.size

    def getEmptyCell(self):
        return self.emptyCell

    def display(self):
        print("\n  ", end="")
        for i in range(self.size):
            print(str(i) + " ", end="")
        print()

        for i in range(self.size):
            print(str(i) + " ", end="")
            for j in range(self.size):
                print(self.grid[i][j].getMark() + " ", end="")
            print()
        print()


# Player class -->
class TicTacToePlayer:
    def __init__(self, playerId, n, s):
        self.playerId = playerId
        self.name = n
        self.symbol = s
        self.score = 0

    # Getters and setters
    def getName(self):
        return self.name

    def getSymbol(self):
        return self.symbol

    def getScore(self):
        return self.score

    def incrementScore(self):
        self.score += 1


# Strategy Pattern for game rules
class TicTacToeRules(ABC):
    @abstractmethod
    def isValidMove(self, board, row, col):
        pass

    @abstractmethod
    def checkWinCondition(self, board, symbol):
        pass

    @abstractmethod
    def checkDrawCondition(self, board):
        pass


# Standard Tic Tac Toe rules
class StandardTicTacToeRules(TicTacToeRules):
    def isValidMove(self, board, row, col):
        return board.isCellEmpty(row, col)

    def checkWinCondition(self, board, symbol):
        size = board.getSize()

        # Check rows
        for i in range(size):
            win = True
            for j in range(size):
                if board.getCell(i, j) is not symbol:
                    win = False
                    break
            if win:
                return True

        # Check columns
        for j in range(size):
            win = True
            for i in range(size):
                if board.getCell(i, j) is not symbol:
                    win = False
                    break
            if win:
                return True

        # Check main diagonal
        win = True
        for i in range(size):
            if board.getCell(i, i) is not symbol:
                win = False
                break
        if win:
            return True

        # Check anti-diagonal
        win = True
        for i in range(size):
            if board.getCell(i, size - 1 - i) is not symbol:
                win = False
                break
        return win

    # If all cells are filled and no winner
    def checkDrawCondition(self, board):
        size = board.getSize()
        for i in range(size):
            for j in range(size):
                if board.getCell(i, j) is board.getEmptyCell():
                    return False
        return True


# Game class --> Observable
class TicTacToeGame:
    def __init__(self, boardSize):
        self.board = Board(boardSize)
        self.players = deque()
        self.rules = StandardTicTacToeRules()
        self.observers = []
        self.gameOver = False

    def addPlayer(self, player):
        self.players.append(player)

    def addObserver(self, observer):
        self.observers.append(observer)

    def notify(self, msg):
        for observer in self.observers:
            observer.update(msg)

    def play(self):
        if len(self.players) < 2:
            print("Need at least 2 players!")
            return

        self.notify("Tic Tac Toe Game Started!")

        scanner = Scanner()

        while not self.gameOver:
            self.board.display()

            # Take out the current player from dequeue
            currentPlayer = self.players[0]
            print(currentPlayer.getName() + " (" + currentPlayer.getSymbol().getMark() + ") - Enter row and column: ", end="")

            row = scanner.nextInt()
            col = scanner.nextInt()

            # check if move is valid
            if self.rules.isValidMove(self.board, row, col):
                self.board.placeMark(row, col, currentPlayer.getSymbol())
                self.notify(currentPlayer.getName() + " played (" + str(row) + "," + str(col) + ")")

                if self.rules.checkWinCondition(self.board, currentPlayer.getSymbol()):
                    self.board.display()
                    print(currentPlayer.getName() + " wins!")
                    currentPlayer.incrementScore()

                    self.notify(currentPlayer.getName() + " wins!")

                    self.gameOver = True
                elif self.rules.checkDrawCondition(self.board):
                    self.board.display()

                    print("It's a draw!")
                    self.notify("Game is Draw!")

                    self.gameOver = True
                else:
                    # Move player to back of queue
                    self.players.popleft()
                    self.players.append(currentPlayer)
            else:
                print("Invalid move! Try again.")


# Enum & Factory Pattern for game creation
class GameType(Enum):
    STANDARD = 1


class TicTacToeGameFactory:
    @staticmethod
    def createGame(gt, boardSize):
        if GameType.STANDARD == gt:
            return TicTacToeGame(boardSize)
        return None


# Main class for Tic Tac Toe
class TicTacToeMain:
    @staticmethod
    def main(args=None):
        print("=== TIC TAC TOE GAME ===")

        # Create game with custom board size
        scanner = Scanner()
        print("Enter board size (e.g., 3 for 3x3): ", end="")
        boardSize = scanner.nextInt()

        game = TicTacToeGameFactory.createGame(GameType.STANDARD, boardSize)

        # Add observer
        notifier = ConsoleNotifier()
        game.addObserver(notifier)

        # Create players with custom symbols
        player1 = TicTacToePlayer(1, "Aditya", Symbol('X'))
        player2 = TicTacToePlayer(2, "Harshita", Symbol('O'))

        game.addPlayer(player1)
        game.addPlayer(player2)

        # Play the game
        game.play()

        scanner.close()


if __name__ == "__main__":
    TicTacToeMain.main()
