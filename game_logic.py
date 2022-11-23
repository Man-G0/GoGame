from piece import Piece
class GameLogic:
    def __init__(self):
        self.piecesArray = []
        print("Game Logic Object Created")

    def printPiecesArray(self):
        print(self.piecesArray)

    def addPiece(self, color, x, y):
        self.piecesArray.append(Piece(color, x, y))

