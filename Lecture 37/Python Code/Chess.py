import time
from abc import ABC, abstractmethod
from enum import Enum


# Enums for better type safety
class Color(Enum):
    WHITE = 1
    BLACK = 2


class PieceType(Enum):
    KING = 1
    QUEEN = 2
    ROOK = 3
    BISHOP = 4
    KNIGHT = 5
    PAWN = 6


class GameStatus(Enum):
    WAITING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    ABORTED = 4


# Position class to represent coordinates
class Position:
    def __init__(self, r=0, c=0):
        self.row = r
        self.col = c

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def isValid(self):
        return self.row >= 0 and self.row < 8 and self.col >= 0 and self.col < 8

    def equals(self, obj):
        if self is obj:
            return True
        if obj is None or type(self) is not type(obj):
            return False
        return self.row == obj.row and self.col == obj.col

    def __eq__(self, obj):
        return self.equals(obj)

    def hashCode(self):
        return hash((self.row, self.col))

    def __hash__(self):
        return self.hashCode()

    def compareTo(self, other):
        if self.row != other.row:
            return (self.row > other.row) - (self.row < other.row)
        return (self.col > other.col) - (self.col < other.col)

    def toString(self):
        return "(" + str(self.row) + "," + str(self.col) + ")"

    # Convert to chess notation (e.g., e4, f7)
    def toChessNotation(self):
        file = chr(ord('a') + self.col)
        rank = chr(ord('8') - self.row)
        return file + rank


# Move class to represent a chess move
class Move:
    def __init__(self, f=None, t=None, p=None, captured=None):
        self._from = f
        self._to = t
        self.piece = p
        self.capturedPiece = captured

    def getFrom(self):
        return self._from

    def getTo(self):
        return self._to

    def getPiece(self):
        return self.piece

    def getCapturedPiece(self):
        return self.capturedPiece


# Abstract Piece class following Strategy Pattern
class Piece(ABC):
    def __init__(self, c, t):
        self.color = c
        self.type = t
        self.hasMoved = False

    def getColor(self):
        return self.color

    def getType(self):
        return self.type

    def getHasMoved(self):
        return self.hasMoved

    def setMoved(self, moved):
        self.hasMoved = moved

    @abstractmethod
    def getPossibleMoves(self, currentPos, board):
        pass

    @abstractmethod
    def getSymbol(self):
        pass

    def toString(self):
        colorStr = "W" if self.color == Color.WHITE else "B"
        return colorStr + self.getSymbol()


# Concrete Piece implementations
class King(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.KING)

    def getPossibleMoves(self, currentPos, board):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for i in range(8):
            newPos = Position(currentPos.getRow() + directions[i][0], currentPos.getCol() + directions[i][1])
            if newPos.isValid() and not board.isOccupiedBySameColor(newPos, self.color):
                moves.append(newPos)
        return moves

    def getSymbol(self):
        return "K"


class Queen(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.QUEEN)

    def getPossibleMoves(self, currentPos, board):
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for d in range(8):
            for i in range(1, 8):
                newPos = Position(currentPos.getRow() + directions[d][0] * i, currentPos.getCol() + directions[d][1] * i)
                if not newPos.isValid():
                    break

                if board.isOccupiedBySameColor(newPos, self.color):
                    break

                moves.append(newPos)
                if board.isOccupied(newPos):
                    break  # Stop after capturing
        return moves

    def getSymbol(self):
        return "Q"


class Rook(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.ROOK)

    def getPossibleMoves(self, currentPos, board):
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for d in range(4):
            for i in range(1, 8):
                newPos = Position(currentPos.getRow() + directions[d][0] * i, currentPos.getCol() + directions[d][1] * i)
                if not newPos.isValid():
                    break

                if board.isOccupiedBySameColor(newPos, self.color):
                    break

                moves.append(newPos)
                if board.isOccupied(newPos):
                    break
        return moves

    def getSymbol(self):
        return "R"


class Bishop(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.BISHOP)

    def getPossibleMoves(self, currentPos, board):
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for d in range(4):
            for i in range(1, 8):
                newPos = Position(currentPos.getRow() + directions[d][0] * i, currentPos.getCol() + directions[d][1] * i)
                if not newPos.isValid():
                    break
                if board.isOccupiedBySameColor(newPos, self.color):
                    break
                moves.append(newPos)
                if board.isOccupied(newPos):
                    break
        return moves

    def getSymbol(self):
        return "B"


class Knight(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.KNIGHT)

    def getPossibleMoves(self, currentPos, board):
        moves = []
        knightMoves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

        for i in range(8):
            newPos = Position(currentPos.getRow() + knightMoves[i][0], currentPos.getCol() + knightMoves[i][1])
            if newPos.isValid() and not board.isOccupiedBySameColor(newPos, self.color):
                moves.append(newPos)
        return moves

    def getSymbol(self):
        return "N"


class Pawn(Piece):
    def __init__(self, color):
        super().__init__(color, PieceType.PAWN)

    def getPossibleMoves(self, currentPos, board):
        moves = []
        direction = -1 if self.color == Color.WHITE else 1

        # Forward move
        oneStep = Position(currentPos.getRow() + direction, currentPos.getCol())
        if oneStep.isValid() and not board.isOccupied(oneStep):
            moves.append(oneStep)

            # Double move from starting position
            if not self.hasMoved:
                twoStep = Position(currentPos.getRow() + 2 * direction, currentPos.getCol())
                if twoStep.isValid() and not board.isOccupied(twoStep):
                    moves.append(twoStep)

        # Diagonal captures
        leftCapture = Position(currentPos.getRow() + direction, currentPos.getCol() - 1)
        rightCapture = Position(currentPos.getRow() + direction, currentPos.getCol() + 1)

        if leftCapture.isValid() and board.isOccupied(leftCapture) and not board.isOccupiedBySameColor(leftCapture, self.color):
            moves.append(leftCapture)

        if rightCapture.isValid() and board.isOccupied(rightCapture) and not board.isOccupiedBySameColor(rightCapture, self.color):
            moves.append(rightCapture)

        return moves

    def getSymbol(self):
        return "P"


# Factory Pattern for creating pieces
class PieceFactory:
    @staticmethod
    def createPiece(type_, color):
        if type_ == PieceType.KING:
            return King(color)
        if type_ == PieceType.QUEEN:
            return Queen(color)
        if type_ == PieceType.ROOK:
            return Rook(color)
        if type_ == PieceType.BISHOP:
            return Bishop(color)
        if type_ == PieceType.KNIGHT:
            return Knight(color)
        if type_ == PieceType.PAWN:
            return Pawn(color)
        return None


# Board class - Dumb object that manages pieces
class Board:
    def __init__(self):
        # Initialize board to null
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.piecePositions = {}
        self.initializeBoard()

    def initializeBoard(self):
        # Initialize white pieces
        self.placePiece(Position(7, 0), PieceFactory.createPiece(PieceType.ROOK, Color.WHITE))
        self.placePiece(Position(7, 1), PieceFactory.createPiece(PieceType.KNIGHT, Color.WHITE))
        self.placePiece(Position(7, 2), PieceFactory.createPiece(PieceType.BISHOP, Color.WHITE))
        self.placePiece(Position(7, 3), PieceFactory.createPiece(PieceType.QUEEN, Color.WHITE))
        self.placePiece(Position(7, 4), PieceFactory.createPiece(PieceType.KING, Color.WHITE))
        self.placePiece(Position(7, 5), PieceFactory.createPiece(PieceType.BISHOP, Color.WHITE))
        self.placePiece(Position(7, 6), PieceFactory.createPiece(PieceType.KNIGHT, Color.WHITE))
        self.placePiece(Position(7, 7), PieceFactory.createPiece(PieceType.ROOK, Color.WHITE))

        for i in range(8):
            self.placePiece(Position(6, i), PieceFactory.createPiece(PieceType.PAWN, Color.WHITE))

        # Initialize black pieces
        self.placePiece(Position(0, 0), PieceFactory.createPiece(PieceType.ROOK, Color.BLACK))
        self.placePiece(Position(0, 1), PieceFactory.createPiece(PieceType.KNIGHT, Color.BLACK))
        self.placePiece(Position(0, 2), PieceFactory.createPiece(PieceType.BISHOP, Color.BLACK))
        self.placePiece(Position(0, 3), PieceFactory.createPiece(PieceType.QUEEN, Color.BLACK))
        self.placePiece(Position(0, 4), PieceFactory.createPiece(PieceType.KING, Color.BLACK))
        self.placePiece(Position(0, 5), PieceFactory.createPiece(PieceType.BISHOP, Color.BLACK))
        self.placePiece(Position(0, 6), PieceFactory.createPiece(PieceType.KNIGHT, Color.BLACK))
        self.placePiece(Position(0, 7), PieceFactory.createPiece(PieceType.ROOK, Color.BLACK))

        for i in range(8):
            self.placePiece(Position(1, i), PieceFactory.createPiece(PieceType.PAWN, Color.BLACK))

    def placePiece(self, pos, piece):
        self.board[pos.getRow()][pos.getCol()] = piece
        self.piecePositions[pos] = piece

    def removePiece(self, pos):
        self.board[pos.getRow()][pos.getCol()] = None
        self.piecePositions.pop(pos, None)

    def getPiece(self, pos):
        return self.board[pos.getRow()][pos.getCol()]

    def isOccupied(self, pos):
        return self.getPiece(pos) is not None

    def isOccupiedBySameColor(self, pos, color):
        piece = self.getPiece(pos)
        return piece is not None and piece.getColor() == color

    def movePiece(self, fromPos, to):
        piece = self.getPiece(fromPos)
        if piece is not None:
            # Remove captured piece if any
            capturedPiece = self.getPiece(to)
            if capturedPiece is not None:
                self.piecePositions.pop(to, None)

            # Move the piece
            self.board[fromPos.getRow()][fromPos.getCol()] = None
            self.board[to.getRow()][to.getCol()] = piece

            # Update piece positions map
            self.piecePositions.pop(fromPos, None)
            self.piecePositions[to] = piece

            piece.setMoved(True)

    def findKing(self, color):
        for pos, piece in self.piecePositions.items():
            if piece.getType() == PieceType.KING and piece.getColor() == color:
                return pos
        return Position(-1, -1)  # Invalid position if not found

    def getAllPiecesOfColor(self, color):
        pieces = []
        for pos, piece in self.piecePositions.items():
            if piece.getColor() == color:
                pieces.append(pos)
        return pieces

    def display(self):
        cellW = 3  # cell width

        # — horizontal border —
        def printBorder():
            print("  +", end="")
            for _i in range(8):
                print("-" * cellW + "+", end="")
            print()

        # — top border —
        printBorder()

        # — column labels inside the grid —
        print("  |", end="")
        for f in range(ord('a'), ord('h') + 1):
            pad = (cellW - 1) // 2
            ch = chr(f)
            print(" " * pad + ch + " " * (cellW - 1 - pad) + "|", end="")
        print()

        # — border under labels —
        printBorder()

        # — each rank of pieces —
        for rank in range(8, 0, -1):
            row = 8 - rank
            print(str(rank) + " |", end="")

            for file in range(8):
                p = self.board[row][file]
                s = p.toString() if p is not None else "  "  # two spaces if empty

                # center a 2-char string in cellW
                pad = (cellW - 2) // 2
                print(" " * pad + s + " " * (cellW - 2 - pad) + "|", end="")

            print(" " + str(rank))
            printBorder()

        # — bottom labels inside the grid —
        print("  |", end="")
        for f in range(ord('a'), ord('h') + 1):
            pad = (cellW - 1) // 2
            ch = chr(f)
            print(" " * pad + ch + " " * (cellW - 1 - pad) + "|", end="")
        print()

        # — final border —
        printBorder()


# Chess Rules interface - Strategy Pattern for game rules
class ChessRules(ABC):
    @abstractmethod
    def isValidMove(self, move, board):
        pass

    @abstractmethod
    def isInCheck(self, color, board):
        pass

    @abstractmethod
    def isCheckmate(self, color, board):
        pass

    @abstractmethod
    def isStalemate(self, color, board):
        pass

    @abstractmethod
    def wouldMoveCauseCheck(self, move, board, kingColor):
        pass


class StandardChessRules(ChessRules):
    def isValidMove(self, move, board):
        piece = move.getPiece()
        possibleMoves = piece.getPossibleMoves(move.getFrom(), board)

        # Check if the target position is in possible moves
        validDestination = False
        for pos in possibleMoves:
            if pos.equals(move.getTo()):
                validDestination = True
                break

        if not validDestination:
            return False

        # Check if move would put own king in check
        return not self.wouldMoveCauseCheck(move, board, piece.getColor())

    def wouldMoveCauseCheck(self, move, board, kingColor):
        # Create a temporary copy to simulate the move safely
        movingPiece = board.getPiece(move.getFrom())
        capturedPiece = board.getPiece(move.getTo())

        if movingPiece is None:
            return True  # Invalid move

        # Temporarily execute the move
        board.removePiece(move.getFrom())
        if capturedPiece is not None:
            board.removePiece(move.getTo())
        board.placePiece(move.getTo(), movingPiece)

        # Check if king is in check after the move
        inCheck = self.isInCheck(kingColor, board)

        # Undo the move
        board.removePiece(move.getTo())
        board.placePiece(move.getFrom(), movingPiece)
        if capturedPiece is not None:
            board.placePiece(move.getTo(), capturedPiece)

        return inCheck

    def isInCheck(self, color, board):
        kingPos = board.findKing(color)
        if kingPos.getRow() == -1:
            return False  # King not found

        opponentColor = Color.BLACK if color == Color.WHITE else Color.WHITE
        opponentPieces = board.getAllPiecesOfColor(opponentColor)

        for pos in opponentPieces:
            piece = board.getPiece(pos)
            moves = piece.getPossibleMoves(pos, board)
            for targetPos in moves:
                if targetPos.equals(kingPos):
                    return True
        return False

    def isCheckmate(self, color, board):
        if not self.isInCheck(color, board):
            return False

        pieces = board.getAllPiecesOfColor(color)
        for pos in pieces:
            piece = board.getPiece(pos)
            moves = piece.getPossibleMoves(pos, board)

            for targetPos in moves:
                move = Move(pos, targetPos, piece, board.getPiece(targetPos))
                if self.isValidMove(move, board):
                    return False  # Found a valid move, not checkmate
        return True

    def isStalemate(self, color, board):
        if self.isInCheck(color, board):
            return False

        pieces = board.getAllPiecesOfColor(color)
        for pos in pieces:
            piece = board.getPiece(pos)
            moves = piece.getPossibleMoves(pos, board)

            for targetPos in moves:
                move = Move(pos, targetPos, piece, board.getPiece(targetPos))
                if self.isValidMove(move, board):
                    return False  # Found a valid move, not stalemate
        return True


# Message class for chat functionality
class Message:
    def __init__(self, sId, msg):
        self.senderId = sId
        self.content = msg
        self.timestamp = int(time.time() * 1000)

    def getSenderId(self):
        return self.senderId

    def getContent(self):
        return self.content

    def getTimestamp(self):
        return self.timestamp

    def toString(self):
        return "[" + self.senderId + "]: " + self.content


# Mediator Pattern - Interface
class ChatMediator(ABC):
    @abstractmethod
    def sendMessage(self, message, user):
        pass

    @abstractmethod
    def addUser(self, user):
        pass

    @abstractmethod
    def removeUser(self, user):
        pass


# Colleague interface for Mediator Pattern
class Colleague(ABC):
    def __init__(self):
        self.mediator = None

    @abstractmethod
    def send(self, message):
        pass

    @abstractmethod
    def receive(self, message):
        pass

    def setMediator(self, med):
        self.mediator = med

    def getMediator(self):
        return self.mediator


# User class now inheriting from Colleague for proper Mediator Pattern
class User(Colleague):
    def __init__(self, userId, userName):
        super().__init__()
        self.id = userId
        self.name = userName
        self.score = 1000  # Starting score

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getScore(self):
        return self.score

    def incrementScore(self, points):
        self.score += points

    def decrementScore(self, points):
        self.score -= points

    def toString(self):
        return self.name + " (Score: " + str(self.score) + ")"

    # Implement Colleague interface
    def send(self, message):
        if self.mediator is not None:
            self.mediator.sendMessage(message, self)

    def receive(self, message):
        print("User " + self.name + " received message from " + message.getSenderId() + ": " + message.getContent())


# Match class implementing Mediator Pattern
class Match(ChatMediator):
    def __init__(self, mId, white, black):
        self.matchId = mId
        self.whitePlayer = white
        self.blackPlayer = black
        self.board = Board()
        self.rules = StandardChessRules()
        self.currentTurn = Color.WHITE
        self.status = GameStatus.IN_PROGRESS
        self.moveHistory = []
        self.chatHistory = []

        # Set mediator for both users
        self.whitePlayer.setMediator(self)
        self.blackPlayer.setMediator(self)

        print("Match started between " + self.whitePlayer.getName() + " (White) and "
              + self.blackPlayer.getName() + " (Black)")

    def makeMove(self, fromPos, to, player):
        if self.status != GameStatus.IN_PROGRESS:
            print("Game is not in progress!")
            return False

        playerColor = self.getPlayerColor(player)
        if playerColor != self.currentTurn:
            print("It's not your turn!")
            return False

        piece = self.board.getPiece(fromPos)
        if piece is None or piece.getColor() != playerColor:
            print("Invalid piece selection!")
            return False

        move = Move(fromPos, to, piece, self.board.getPiece(to))

        if not self.rules.isValidMove(move, self.board):
            print("Invalid move!")
            return False

        # Execute move
        self.board.movePiece(fromPos, to)
        self.moveHistory.append(move)

        print(player.getName() + " moved " + piece.getSymbol()
              + " from " + fromPos.toChessNotation() + " to " + to.toChessNotation())

        self.board.display()

        # Check game end conditions
        opponentColor = Color.BLACK if self.currentTurn == Color.WHITE else Color.WHITE
        if self.rules.isCheckmate(opponentColor, self.board):
            self.endGame(player, "checkmate")
            return True
        elif self.rules.isStalemate(opponentColor, self.board):
            self.endGame(player, "stalemate")
            return True
        else:
            self.currentTurn = opponentColor
            if self.rules.isInCheck(opponentColor, self.board):
                print(self.getPlayerByColor(opponentColor).getName() + " is in check!")

        return True

    def quitGame(self, player):
        opponent = self.blackPlayer if player is self.whitePlayer else self.whitePlayer
        self.endGame(opponent, "quit")
        player.decrementScore(50)  # Penalty for quitting
        print(player.getName() + " quit the game. Score decreased by 50.")

    def endGame(self, winner, reason):
        self.status = GameStatus.COMPLETED

        if winner is not None:
            loser = self.blackPlayer if winner is self.whitePlayer else self.whitePlayer
            winner.incrementScore(30)
            loser.decrementScore(20)
            print("Game ended - " + winner.getName() + " wins by " + reason + "!")
            print("Score update: " + winner.getName() + " +30, " + loser.getName() + " -20")
        else:
            print("Game ended in " + reason + "! No score change.")

    def getPlayerColor(self, player):
        return Color.WHITE if player is self.whitePlayer else Color.BLACK

    def getPlayerByColor(self, color):
        return self.whitePlayer if color == Color.WHITE else self.blackPlayer

    # Mediator Pattern implementation
    def sendMessage(self, message, user):
        self.chatHistory.append(message)

        recipient = self.blackPlayer if user is self.whitePlayer else self.whitePlayer
        recipient.receive(message)
        print("Chat in match " + self.matchId + " - " + message.getContent())

    def addUser(self, user):
        # Not applicable for chess match (always 2 users)
        return

    def removeUser(self, user):
        self.quitGame(user)

    def getMatchId(self):
        return self.matchId

    def getStatus(self):
        return self.status

    def getWhitePlayer(self):
        return self.whitePlayer

    def getBlackPlayer(self):
        return self.blackPlayer

    def getBoard(self):
        return self.board


# Matching Strategy interface
class MatchingStrategy(ABC):
    @abstractmethod
    def findMatch(self, user, waitingUsers):
        pass


# Score-based matching strategy
class ScoreBasedMatching(MatchingStrategy):
    def __init__(self, tolerance):
        self.scoreTolerance = tolerance

    def findMatch(self, user, waitingUsers):
        bestMatch = None
        bestScoreDiff = 2147483647  # Integer.MAX_VALUE

        for waitingUser in waitingUsers:
            if waitingUser.getId() != user.getId():
                scoreDiff = abs(waitingUser.getScore() - user.getScore())
                if scoreDiff <= self.scoreTolerance and scoreDiff < bestScoreDiff:
                    bestMatch = waitingUser
                    bestScoreDiff = scoreDiff
        return bestMatch


# Game Manager - Singleton Pattern
class GameManager:
    instance = None

    def __init__(self):
        self.activeMatches = {}
        self.waitingUsers = []
        self.matchingStrategy = ScoreBasedMatching(100)  # 100 points tolerance
        self.matchCounter = 0

    @staticmethod
    def getInstance():
        if GameManager.instance is None:
            GameManager.instance = GameManager()
        return GameManager.instance

    def requestMatch(self, user):
        print(user.getName() + " is looking for a match...")

        opponent = self.matchingStrategy.findMatch(user, self.waitingUsers)

        if opponent is not None:
            # Remove opponent from waiting list
            self.waitingUsers.remove(opponent)

            self.matchCounter += 1
            matchId = "MATCH_" + str(self.matchCounter)
            match = Match(matchId, user, opponent)
            self.activeMatches[matchId] = match

            print("Match found! " + user.getName() + " vs " + opponent.getName())
            match.getBoard().display()
        else:
            self.waitingUsers.append(user)
            print(user.getName() + " added to waiting list.")

    def makeMove(self, matchId, fromPos, to, player):
        if matchId in self.activeMatches:
            match = self.activeMatches[matchId]
            match.makeMove(fromPos, to, player)

            if match.getStatus() == GameStatus.COMPLETED:
                del self.activeMatches[matchId]
                print("Match " + matchId + " completed and removed from active matches.")

    def quitMatch(self, matchId, player):
        if matchId in self.activeMatches:
            match = self.activeMatches[matchId]
            match.quitGame(player)
            del self.activeMatches[matchId]

    def sendChatMessage(self, matchId, message, user):
        if matchId in self.activeMatches:
            match = self.activeMatches[matchId]
            msg = Message(user.getId(), message)
            match.sendMessage(msg, user)

    def getMatch(self, matchId):
        if matchId in self.activeMatches:
            return self.activeMatches[matchId]
        return None

    def displayActiveMatches(self):
        print("\n=== Active Matches ===")
        for _matchId, match in self.activeMatches.items():
            print("Match " + match.getMatchId() + ": "
                  + match.getWhitePlayer().getName() + " vs "
                  + match.getBlackPlayer().getName())
        print("Total active matches: " + str(len(self.activeMatches)))
        print("Users waiting: " + str(len(self.waitingUsers)))


# Util class for basic demo
class ChessSystemDemo:
    # Method to demonstrate Scholar's Mate (4-move checkmate)
    @staticmethod
    def demonstrateScholarsMate():
        print("\n=== Scholar's Mate Demo (4-move checkmate) ===")

        aditya = User("DEMO_1", "Aditya")
        rohit = User("DEMO_2", "Rohit")

        demoMatch = Match("DEMO_MATCH", aditya, rohit)
        demoMatch.getBoard().display()

        # Proper Scholar's Mate sequence with correct coordinates
        print("\nMove 1: White e2-e4")
        demoMatch.makeMove(Position(6, 4), Position(4, 4), aditya)  # e2-e4

        print("\nMove 1: Black e7-e5")
        demoMatch.makeMove(Position(1, 4), Position(3, 4), rohit)  # e7-e5

        print("\nMove 2: White Bf1-c4 (targeting f7)")
        demoMatch.makeMove(Position(7, 5), Position(4, 2), aditya)  # Bf1-c4

        print("\nMove 2: Black Nb8-c6 (developing)")
        demoMatch.makeMove(Position(0, 1), Position(2, 2), rohit)  # Nb8-c6

        print("\nMove 3: White Qd1-h5 (attacking f7 and h7)")
        demoMatch.makeMove(Position(7, 3), Position(3, 7), aditya)  # Qd1-h5 (row 3, col 7 = h5)

        print("\nMove 3: Black Ng8-f6?? (defending h7 but exposing f7)")
        demoMatch.makeMove(Position(0, 6), Position(2, 5), rohit)  # Ng8-f6

        print("\nMove 4: White Qh5xf7# (Checkmate!)")
        gameEnded = demoMatch.makeMove(Position(3, 7), Position(1, 5), aditya)  # Qh5xf7#

        if demoMatch.getStatus() != GameStatus.COMPLETED:
            print("Note: Checkmate detection may need refinement for this position.")

        # Demonstrate chat functionality
        print("\n=== Testing Chat Functionality ===")
        aditya.send(Message(aditya.getId(), "Good game!"))
        rohit.send(Message(rohit.getId(), "Thanks, that was a quick one!"))


# Main class to run the chess system
class Chess:
    @staticmethod
    def main(args=None):
        print("=== Chess System with Design Patterns Demo ===")

        # Test Scholar's Mate
        ChessSystemDemo.demonstrateScholarsMate()

        # Demonstrate Game Manager functionality
        print("\n=== Game Manager Demo ===")
        gm = GameManager.getInstance()

        saurav = User("USER_1", "Saurav")
        manish = User("USER_2", "Manish")
        abhishek = User("USER_3", "Abishek")

        print("\nUsers: " + saurav.toString() + ", " + manish.toString() + ", " + abhishek.toString())

        # Request matches
        gm.requestMatch(saurav)
        gm.requestMatch(manish)  # Should create a match
        gm.requestMatch(abhishek)  # Should go to waiting list

        gm.displayActiveMatches()


if __name__ == "__main__":
    Chess.main()
