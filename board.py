from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint, QRect, QSize
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen, QBrush, QCursor
from PyQt6.QtTest import QTest
from piece import Piece

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location
    boardWidth  = 6    # board is 6 squares wide
    boardHeight = 6     # board is 6 squares high
    timerSpeed  = 1     # the timer updates every 1 millisecond
    counter     = 10    # the number the counter will count down from

    def __init__(self, parent, logic):
        super().__init__(parent)
        self.go = parent
        self.logic = logic
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        #self.timer = QBasicTimer()  # create a timer for the game
        #self.isStarted = False      # game is not currently started
        #self.start()                # start the game which will start the timer
        #self.setStyleSheet("background-color: blue")
        self.setMinimumSize(300, 300)

        if self.squareWidth() <= self.squareHeight():
            squareSide = self.squareWidth()
        else:
            squareSide = self.squareHeight()
        self.whiteStone = QPixmap("WhiteStone.png")
        self.whiteStone.scaled(QSize(int(squareSide), int(squareSide)))
        self.blackStone = QPixmap("BlackStone.png")
        self.blackStone.scaled(QSize(int(squareSide), int(squareSide)))

    def resizeEvent(self, event):
        # Create a square base size of 10x10 and scale it to the new size
        # maintaining aspect ratio.
        if self.contentsRect().height() > self.contentsRect().width():
            new_size = QtCore.QSize(self.contentsRect().width(), self.contentsRect().width())
        else:
            new_size = QtCore.QSize(self.contentsRect().height(), self.contentsRect().height())
        self.resize(new_size)

        if self.squareWidth()<=self.squareHeight():
            squareSide = self.squareWidth()
        else:
            squareSide = self.squareHeight()
        self.go.cursor_scaled_pix = self.go.cursor_pix.scaled(QSize(int(squareSide * 1.5), int(squareSide * 1.5)))
        self.go.cursor_white = QCursor(self.go.cursor_scaled_pix, -1, -1)
        self.go.cursor_black = QCursor(self.go.cursor_scaled_pix, -1, -1)


    def squareWidth(self):
        '''returns the width of one square in the board'''
        return (self.contentsRect().width()-(self.contentsRect().width()/self.boardWidth))/self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return (self.contentsRect().height()-(self.contentsRect().height()/self.boardHeight)) / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True                       # set the boolean which determines if the game has started to TRUE
        self.resetGame()                            # reset the game
        self.timer.start(self.timerSpeed, self)     # start the timer with the correct speed
        print("start () - timer is started")

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if Board.counter == 0:
                print("Game over")
            self.counter -= 1
            print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)      # if we do not handle an event we should pass it to the super
                                                        # class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.playablePosition(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location ["+str(event.position().x())+","+str(event.position().y())+"]"     # the location where a mouse click was registered
        print("mousePressEvent() - "+clickLoc)
        if self.squareWidth() <= self.squareHeight():
            squareSide = self.squareWidth()
        else:
            squareSide = self.squareHeight()
        if self.logic.currentPlayer == "W":
            self.listPlayable = self.logic.findWPlayable()
        elif self.logic.currentPlayer == "B":
            self.listPlayable = self.logic.findBPlayable()
        for col in range(0, Board.boardWidth+1):
            for row in range(0, Board.boardHeight+1):
                colTransformation = squareSide * 0.5 + squareSide * col
                rowTransformation = squareSide * 0.5 + squareSide * row

                if (event.position().x()+squareSide * 0.3>colTransformation)&(event.position().x()-squareSide * 0.3<colTransformation)&(event.position().y()+squareSide * 0.3>rowTransformation)&(event.position().y()-squareSide * 0.3<rowTransformation)&(self.listPlayable[col][row]):
                    print("piece placed")
                    if self.logic.currentPlayer == "W":
                        self.logic.addPiece('W',col,row)
                        self.logic.currentPlayer = "B"
                    elif self.logic.currentPlayer == "B":
                        self.logic.addPiece('B',col,row)
                        self.logic.currentPlayer = "W"
                    self.go.cursor()


        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        '''clears pieces from the board'''
        painter = QPainter()
        self.drawBoardSquares(painter)

    def playablePosition(self,painter):

        if self.logic.currentPlayer == "W":
            self.listPlayable = self.logic.findWPlayable()
            self.logic.printPayable(self.listPlayable)
        elif self.logic.currentPlayer == "B":
            self.listPlayable = self.logic.findBPlayable()
            self.logic.printPayable(self.listPlayable)

        if self.squareWidth()<=self.squareHeight():
            squareSide = self.squareWidth()
        else:
            squareSide = self.squareHeight()

        for col in range(0, Board.boardWidth + 1):
            for row in range(0, Board.boardHeight + 1):
                if self.listPlayable[col][row]:
                    self.brushSize = 1
                    self.brushColor = QColor("#00E6FF")
                    painter.setPen(QPen(self.brushColor, self.brushSize))
                    painter.setBrush(QBrush(self.brushColor, Qt.BrushStyle.SolidPattern))
                    colTransformation = squareSide * 0.47 + squareSide * col
                    rowTransformation = squareSide * 0.47 + squareSide * row
                    painter.drawEllipse(int(colTransformation), int(rowTransformation), 5,5)


    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black
        painter.setPen(QPen(self.brushColor, self.brushSize))
        painter.fillRect(QRect(0, 0, self.contentsRect().width(), self.contentsRect().height()),self.go.backgroundColor)

        if self.squareWidth()<=self.squareHeight():
            squareSide = self.squareWidth()
        else:
            squareSide = self.squareHeight()
        for row in range(0, Board.boardHeight):
            for col in range (0, Board.boardWidth):
                painter.save()
                colTransformation = squareSide*0.5+squareSide* col
                rowTransformation = squareSide*0.5+squareSide* row
                painter.fillRect(QRect(int(colTransformation),int(rowTransformation),int(squareSide),int(squareSide)),QColor("#E0BD6B"))
                painter.drawRect(QRect(int(colTransformation),int(rowTransformation),int(squareSide),int(squareSide)))
                painter.restore()
                self.brushColor = self.go.backgroundColor



    def drawPieces(self, painter):
        '''draw the prices on the board'''
        #colour = Qt.GlobalColor.transparent # empty square could be modeled with transparent pieces

        if self.squareWidth()<=self.squareHeight():
            squareSide = self.squareWidth()
        else:
            squareSide = self.squareHeight()
        image = QRect(0, 0, 70, 70)
        for row in range(0, Board.boardHeight+1):
            for col in range(0, Board.boardWidth+1):
                painter.save()
                colTransformation = squareSide * col
                rowTransformation = squareSide * row
                if self.logic.piecesArray[col][row] is not None:
                    if self.logic.piecesArray[col][row].color == 'W':
                        piece = QRect(int(colTransformation),int(rowTransformation),int(squareSide), int(squareSide))
                        self.whiteStone.scaled(QSize(int(squareSide), int(squareSide)))
                        painter.drawPixmap(piece, self.whiteStone, image)
                    elif self.logic.piecesArray[col][row].color == 'B':
                        piece = QRect(int(colTransformation),int(rowTransformation), int(squareSide), int(squareSide))
                        self.blackStone.scaled(QSize(int(squareSide), int(squareSide)))
                        painter.drawPixmap(piece, self.blackStone, image)
                painter.restore()
