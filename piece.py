class Piece(object):
    def __init__(self, color, x, y):  # constructor
        self.color = color
        self.liberties = 0
        self.x = x
        self.y = y

    def getLiberties(self):  # return Liberties
        return self.liberties

    def setLiberties(self, liberties):  # set Liberties
        self.liberties = liberties

