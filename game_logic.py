from piece import Piece


class GameLogic:
    def __init__(self):
        self.xSize = 9
        self.ySize = 9
        self.piecesArray = []
        for i in range(self.xSize):
            yArray = [None]*self.ySize
            self.piecesArray.append(yArray)
        print("Game Logic Object Created")

    def printPiecesArray(self):
        for i in range(self.xSize):
            aLine = "-"
            for j in range(self.ySize):
                aLine += "----"
            print(aLine)
            aLine = "|"
            for j in range(self.ySize):
                if self.piecesArray[i][j] is None:
                    aLine += "   |"
                elif self.piecesArray[i][j].color == 'W':
                    aLine += " W |"
                elif self.piecesArray[i][j].color == 'B':
                    aLine += " B |"
                else:
                    aLine += " X |"
            print(aLine)
            aLine = "-"
        for j in range(self.ySize):
            aLine += "----"
        print(aLine)

    def printLibertiesArray(self):
        for i in range(self.xSize):
            aLine = "-"
            for j in range(self.ySize):
                aLine += "----"
            print(aLine)
            aLine = "|"
            for j in range(self.ySize):
                if self.piecesArray[i][j] is None:
                    aLine += "   |"
                else:
                    aLine += " " + str(self.piecesArray[i][j].liberties) + " |"
            print(aLine)
            aLine = "-"
        for j in range(self.ySize):
            aLine += "----"
        print(aLine)

    def addPiece(self, color, x, y):
        self.piecesArray[x][y] = (Piece(color, x, y))

    def calcLiberties(self):
        group = 0
        for i in range(self.xSize):
            for j in range(self.ySize):
                pieceCheck = self.piecesArray[i][j]
                if pieceCheck is not None:
                    if pieceCheck.group == 0:
                        group += 1
                        pieceCheck.findLiberties(group, self.xSize, self.ySize, self.piecesArray)

        groupLiberties=[0]*group

        for i in range(self.xSize):
            for j in range(self.ySize):
                pieceCheck = self.piecesArray[i][j]
                if pieceCheck is not None:
                    groupLiberties[pieceCheck.group-1] += pieceCheck.liberties

        for i in range(self.xSize):
            for j in range(self.ySize):
                pieceCheck = self.piecesArray[i][j]
                if pieceCheck is not None:
                    pieceCheck.liberties = groupLiberties[pieceCheck.group-1]
