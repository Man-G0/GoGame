from piece import Piece
from empty import Empty


class GameLogic:
    def __init__(self):
        '''
        init function
        '''
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
        '''
        function to add a piece
        input : the color and the position of the piece
        '''
        self.piecesArray[x][y] = Piece(color, x, y)
        self.lastGrid .append(self.duplicateGrid())
        self.calcLiberties()
        self.removeCapture(color)

    def calcLiberties(self):
        '''
        function to calculate the liberties in the current board
        '''
        self.calcLibertiesVar(self.piecesArray)

    def calcLibertiesVar(self, array):
        '''
        function to calculate the liberties of a board
        inout : the board where we want to calculate the liberties
        '''
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

        groupLiberties = [0]*group

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
        '''
        function to remove the piece with no liberties and put them in prison
        input : the color of the player playing
        '''
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
        '''
        function to find where the black player can play
        '''
        self.bPlayable = []
        for i in range(self.xSize):
            yArray = [None] * self.ySize
            self.bPlayable.append(yArray)
        self.findPlayable("B", self.bPlayable)
        return self.bPlayable

    def findWPlayable(self):
        '''
        function to find where the white player can play
        '''
        self.wPlayable = []
        for i in range(self.xSize):
            yArray = [None] * self.ySize
            self.wPlayable.append(yArray)
        self.findPlayable("W", self.wPlayable)
        return self.wPlayable

    def findPlayable(self, color, playableArray):
        '''
        function to find where a player can play$
        input : the color of the player and the list of all pieces
        '''
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
        '''
        function to create a duplicate grid from the current one
        '''
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
        '''
        function to compare two grid and see if there are the same
        '''
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
        '''
        function to see if a grid is in the list of the last grid
        '''
        inPrevious = False
        i = len(self.lastGrid)-1
        while i >= 0 and not inPrevious:
            if self.compareGrid(self.lastGrid[i], gridToCheck):
                inPrevious = True
            i -= 1
        return inPrevious

    def calcTerritori(self):
        '''
        function to calcul the territories of the two player
        '''
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
        '''
        function to calcul the score of the two player
        '''
        self.calcTerritori()

        self.scoreB = self.territoriB
        self.scoreW = self.territoriW

        self.scoreB -= len(self.bCaptured)
        self.scoreW -= len(self.wCaptured) + 6.5

    def removeDead(self, x, y):
        '''
        function to remove the dead stone
        input : the position of the stone
        '''
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
