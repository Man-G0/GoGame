from piece import Piece
class GameLogic:
    def __init__(self):
        xSize = 9
        ySize = 9
        self.piecesArray = []
        for i in range(xSize):
            yArray = [0]*ySize
            self.piecesArray.append(yArray)
        print("Game Logic Object Created")

    def printPiecesArray(self):
        print(self.piecesArray)

    def addPiece(self, color, x, y):
        self.piecesArray[x][y] = (Piece(color, x, y))
