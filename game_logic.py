from piece import Piece
from empty import Empty

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
        self.currentPlayer = "B"
        self.territoriB = 0
        self.territoriW = 0

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
        return same

    def checkPreviousGrid(self, gridToCheck):
        inPrevious = False
        i = len(self.lastGrid)-1
        while i >= 0 and not inPrevious:
            if self.compareGrid(self.lastGrid[i], gridToCheck):
                inPrevious = True
            i -= 1
        return inPrevious

    def calcTerritori(self):
        duplicate = self.duplicateGrid()
        for i in range(self.xSize):
            for j in range(self.ySize):
                if duplicate[i][j] is None:
                    duplicate[i][j] = Empty(i, j)

        group = 0
        listColorNear = []
        for i in range(self.xSize):
            for j in range(self.ySize):
                if type(duplicate[i][j]) == Empty:
                    if duplicate[i][j].group == 0:
                        group += 1
                        listColorNear.append(duplicate[i][j].calcGroup(self.xSize, self.ySize, group, duplicate))

        for i in range(group):
            if "B" in listColorNear[i] and "W" in listColorNear[i]:
                listColorNear[i] = "both"
            elif "B" in listColorNear[i]:
                listColorNear[i] = "B"
            elif "W" in listColorNear[i]:
                listColorNear[i] = "W"

        self.territoriB = 0
        self.territoriW = 0

        for i in range(self.xSize):
            for j in range(self.ySize):
                if type(duplicate[i][j]) == Empty:
                    if listColorNear[duplicate[i][j].group-1] == 'B':
                        self.territoriB += 1
                    if listColorNear[duplicate[i][j].group-1] == 'W':
                        self.territoriW += 1

    def calcPoint(self):

        self.calcTerritori()
        self.scoreB = self.territoriB
        self.scoreW = self.territoriW

        self.scoreB -= len(self.bCaptured) + 6.5
        self.scoreW -= len(self.wCaptured)
        print("scoreB = " + str(self.scoreB))
        print("scoreW = " + str(self.scoreW))

    def removeDead(self, x, y):
        pieceCheck = self.piecesArray[x][y]
        if pieceCheck is None:
            return False
        else :
            if pieceCheck.color == "B":
                self.bCaptured.append(pieceCheck)
                self.piecesArray[x][y] = None
                return True
            elif pieceCheck.color == "W":
                self.wCaptured.append(pieceCheck)
                self.piecesArray[x][y] = None
                return True


