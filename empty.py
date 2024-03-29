class Empty(object):
    def __init__(self, x, y):
        '''
        init function
        input : X and Y position
        '''
        self.x = x
        self.y = y
        self.group = 0
        self.colorNear = []

    def calcGroup(self, xSize, ySize, group, piecesArray):
        '''
        function to calcul the neighbour of the empty space
        input : x and y size of the board
                group of the empty sapce
                the array of all the pieces of the board
        '''
        self.group = group
        if self.x != 0:
            if type(piecesArray[self.x-1][self.y]) == Empty:
                if piecesArray[self.x-1][self.y].group == 0:
                    self.colorNear += piecesArray[self.x - 1][self.y].calcGroup(xSize, ySize, group, piecesArray)
            else:
                self.colorNear.append(piecesArray[self.x-1][self.y].color)

        if self.y != 0:
            if type(piecesArray[self.x][self.y - 1]) == Empty:
                if piecesArray[self.x][self.y - 1].group == 0:
                    self.colorNear += piecesArray[self.x][self.y - 1].calcGroup(xSize, ySize, group, piecesArray)
            else:
                self.colorNear.append(piecesArray[self.x][self.y - 1].color)

        if self.x != xSize - 1:
            if type(piecesArray[self.x + 1][self.y]) == Empty:
                if piecesArray[self.x + 1][self.y].group == 0:
                    self.colorNear += piecesArray[self.x + 1][self.y].calcGroup(xSize, ySize, group, piecesArray)
            else:
                self.colorNear.append(piecesArray[self.x + 1][self.y].color)

        if self.y != ySize - 1:
            if type(piecesArray[self.x][self.y + 1]) == Empty:
                if piecesArray[self.x][self.y + 1].group == 0:
                    self.colorNear += piecesArray[self.x][self.y + 1].calcGroup(xSize, ySize, group, piecesArray)
            else:
                self.colorNear.append(piecesArray[self.x][self.y + 1].color)

        return self.colorNear
