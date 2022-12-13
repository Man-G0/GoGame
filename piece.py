class Piece(object):
    def __init__(self, color, x, y):  # constructor
        self.color = color
        self.liberties = 0
        self.x = x
        self.y = y
        self.group = 0

    def findLiberties(self, group, xSize, ySize, piecesArray):
        self.liberties = 0
        self.group = group
        if self.x != 0:
            if piecesArray[self.x-1][self.y] is None:
                self.liberties += 1
            elif piecesArray[self.x-1][self.y].color == self.color and piecesArray[self.x-1][self.y].group == 0:
                piecesArray[self.x-1][self.y].findLiberties(group, xSize, ySize, piecesArray)

        if self.y != 0:
            if piecesArray[self.x][self.y-1] is None:
                self.liberties += 1
            elif piecesArray[self.x][self.y-1].color == self.color and piecesArray[self.x][self.y-1].group == 0:
                piecesArray[self.x][self.y-1].findLiberties(group, xSize, ySize, piecesArray)

        if self.x != xSize - 1:
            if piecesArray[self.x+1][self.y] is None:
                self.liberties += 1
            elif piecesArray[self.x+1][self.y].color == self.color and piecesArray[self.x+1][self.y].group == 0:
                piecesArray[self.x+1][self.y].findLiberties(group, xSize, ySize, piecesArray)

        if self.y != ySize - 1:
            if piecesArray[self.x][self.y+1] is None:
                self.liberties += 1
            elif piecesArray[self.x][self.y+1].color == self.color and piecesArray[self.x][self.y+1].group == 0:
                piecesArray[self.x][self.y+1].findLiberties(group, xSize, ySize, piecesArray)

