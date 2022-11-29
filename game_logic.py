from piece import Piece


class GameLogic:
    def __init__(self):
        self.xSize = 9
        self.ySize = 9
        self.bCaptured = []
        self.wCaptured = []
        self.piecesArray = []
        for i in range(self.xSize):
            yArray = [None]*self.ySize
            self.piecesArray.append(yArray)

    def printPiecesArray(self):
        for j in range(self.xSize):
            aLine = "+"
            for i in range(self.ySize):
                aLine += "---+"
            print(aLine)
            aLine = "|"
            for i in range(self.ySize):
                if self.piecesArray[i][j] is None:
                    aLine += "   |"
                elif self.piecesArray[i][j].color == 'W':
                    aLine += " W |"
                elif self.piecesArray[i][j].color == 'B':
                    aLine += " B |"
                else:
                    aLine += " X |"
            print(aLine)
            aLine = "+"
        for i in range(self.ySize):
            aLine += "---+"
        print(aLine)

    def printPayable(self,playableArray):
        for j in range(self.xSize):
            aLine = "+"
            for i in range(self.ySize):
                aLine += "---+"
            print(aLine)
            aLine = "|"
            for i in range(self.ySize):
                if playableArray[i][j]:
                    aLine += " O |"
                else:
                    aLine += " X |"
            print(aLine)
            aLine = "+"
        for i in range(self.ySize):
            aLine += "---+"
        print(aLine)

    def printLibertiesArray(self):
        for j in range(self.xSize):
            aLine = "+"
            for i in range(self.ySize):
                aLine += "---+"
            print(aLine)
            aLine = "|"
            for i in range(self.ySize):
                if self.piecesArray[i][j] is None:
                    aLine += "   |"
                else:
                    aLine += " " + str(self.piecesArray[i][j].liberties) + " |"
            print(aLine)
            aLine = "+"
        for i in range(self.ySize):
            aLine += "---+"
        print(aLine)

    def addPiece(self, color, x, y):
        self.piecesArray[x][y] = Piece(color, x, y)

    def calcLiberties(self):
        self.calcLibertiesVar(self.piecesArray)

    def calcLibertiesVar(self, array):
        group = 0
        for i in range(self.xSize):
            for j in range(self.ySize):
                pieceCheck = array[i][j]
                if pieceCheck is not None:
                    pieceCheck.group = 0

        for i in range(self.xSize):
            for j in range(self.ySize):
                pieceCheck = array[i][j]
                if pieceCheck is not None:
                    if pieceCheck.group == 0:
                        group += 1
                        pieceCheck.findLiberties(group, self.xSize, self.ySize, array)

        groupLiberties=[0]*group

        for i in range(self.xSize):
            for j in range(self.ySize):
                pieceCheck = array[i][j]
                if pieceCheck is not None:
                    groupLiberties[pieceCheck.group-1] += pieceCheck.liberties

        for i in range(self.xSize):
            for j in range(self.ySize):
                pieceCheck = array[i][j]
                if pieceCheck is not None:
                    pieceCheck.liberties = groupLiberties[pieceCheck.group-1]


    def removeCapture(self):
        for i in range(self.xSize):
            for j in range(self.ySize):
                pieceCheck = self.piecesArray[i][j]
                if pieceCheck is not None:
                    if pieceCheck.liberties == 0 and pieceCheck.color == "W":
                        self.wCaptured.append(pieceCheck)
                        self.piecesArray[i][j] = None
                    elif pieceCheck.liberties == 0 and pieceCheck.color == "B":
                        self.bCaptured.append(pieceCheck)
                        self.piecesArray[i][j] = None

    def findBPlayable(self):
        self.bPlayable = []
        for i in range(self.xSize):
            yArray = [None] * self.ySize
            self.bPlayable.append(yArray)
        self.findPlayable("B", self.bPlayable)
        return self.bPlayable

    def findWPlayable(self):
        self.wPlayable = []
        for i in range(self.xSize):
            yArray = [None] * self.ySize
            self.wPlayable.append(yArray)
        self.findPlayable("W", self.wPlayable)
        return self.wPlayable

    def findPlayable(self, color, playableArray):
        for i in range(self.xSize):
            for j in range(self.ySize):
                if self.piecesArray[i][j] is not None:
                    playableArray[i][j] = False
                else:
                    self.duplicatedArray = self.duplicateGrid()
                    self.duplicatedArray[i][j] = Piece(color, i, j)
                    self.calcLibertiesVar(self.duplicatedArray)
                    playable = True
                    for m in range(self.xSize):#optimisable avec des while
                        for n in range(self.ySize):#optimisable avec des while
                            pieceCheck = self.duplicatedArray[m][n]
                            if pieceCheck is not None:
                                if pieceCheck.liberties == 0 and pieceCheck.color == color:
                                    playable = False
                    playableArray[i][j] = playable

    def duplicateGrid(self):
        duplicatedArray = []
        for i in range(self.xSize):
            yArray = []
            for j in range(self.ySize):
                yArray.append(self.piecesArray[i][j])
            duplicatedArray.append(yArray)
        return duplicatedArray
