from piece import Piece


class GameLogic:
    def __init__(self):
        self.xSize = 7
        self.ySize = 7
        self.bCaptured = []
        self.wCaptured = []
        self.piecesArray = []
        for i in range(self.xSize):
            yArray = [None]*self.ySize
            self.piecesArray.append(yArray)
        self.lastGrid = [self.duplicateGrid()]
        self.currentPlayer = "W"

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

    def printPayable(self, playableArray):
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
        self.lastGrid .append(self.duplicateGrid())
        self.calcLiberties()
        self.removeCapture(color)

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

    def removeCapture(self, color):
        for i in range(self.xSize):
            for j in range(self.ySize):
                pieceCheck = self.piecesArray[i][j]
                if pieceCheck is not None:
                    if pieceCheck.color != color:
                        if pieceCheck.liberties == 0 and pieceCheck.color == "W":
                            self.wCaptured.append(pieceCheck)
                            print("white remove")
                            self.piecesArray[i][j] = None
                        elif pieceCheck.liberties == 0 and pieceCheck.color == "B":
                            self.bCaptured.append(pieceCheck)
                            print("black remove")
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
                    if self.checkPreviousGrid(self.duplicatedArray):
                        playableArray[i][j] = False
                    else:
                        self.calcLibertiesVar(self.duplicatedArray)
                        for m in range(self.xSize):
                            for n in range(self.ySize):
                                pieceCheck = self.duplicatedArray[m][n]
                                if pieceCheck is not None:
                                    if pieceCheck.liberties == 0 and pieceCheck.color != color:
                                        self.duplicatedArray[m][n] = None
                        self.calcLibertiesVar(self.duplicatedArray)


                        playable = True
                        m = 0
                        while m < self.xSize and playable:
                            n = 0
                            while n < self.ySize and playable:
                                pieceCheck = self.duplicatedArray[m][n]
                                if pieceCheck is not None:
                                    if pieceCheck.liberties == 0 and pieceCheck.color == color:
                                        playable = False
                                n +=1
                            m += 1
                        playableArray[i][j] = playable

    def duplicateGrid(self):
        duplicatedArray = []
        for i in range(self.xSize):
            yArray = []
            for j in range(self.ySize):
                if self.piecesArray[i][j] is None:
                    yArray.append(None)
                else:
                    yArray.append(Piece(self.piecesArray[i][j].color, self.piecesArray[i][j].x, self.piecesArray[i][j].y))
            duplicatedArray.append(yArray)
        return duplicatedArray

    def compareGrid(self, grid1, grid2):
        same = True
        i = 0
        while i < self.xSize and same:
            j = 0
            while j < self.ySize and same:
                if not (grid1[i][j] is None and grid2[i][j] is None):
                    if grid1[i][j] is None or grid2[i][j] is None:
                        same = False
                    elif grid1[i][j].color != grid2[i][j].color:
                        same = False
                j += 1
            i += 1
        if same:
            print(same)
        return same

    def checkPreviousGrid(self, gridToCheck):
        inPrevious = False
        i = len(self.lastGrid)-1
        while i >= 0 and not inPrevious:
            if self.compareGrid(self.lastGrid[i], gridToCheck):
                inPrevious = True
            i -= 1
        return inPrevious
