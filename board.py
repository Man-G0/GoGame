from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint, QRect, QSize
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen
from PyQt6.QtTest import QTest
from go import Go
from piece import Piece

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location
    boardWidth  = 6    # board is 6 squares wide
    boardHeight = 6     # board is 6 squares high
    timerSpeed  = 1     # the timer updates every 1 millisecond
    counter     = 10    # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.go = Go()
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        #self.timer = QBasicTimer()  # create a timer for the game
        #self.isStarted = False      # game is not currently started
        #self.start()                # start the game which will start the timer
        #self.setStyleSheet("background-color: blue")
        boardImage = QPixmap("board-19x19.jpg")
        self.setMinimumSize(300, 300)

        self.boardGridLayout = QGridLayout()

        self.boardLayout = QHBoxLayout()

        if self.squareWidth() <= self.squareHeight():
            squareSide = self.squareWidth()
        else:
            squareSide = self.squareHeight()
        self.whiteStone = QPixmap("WhiteStone.png")
        self.whiteStone.scaled(QSize(int(squareSide), int(squareSide)))
        self.blackStone = QPixmap("BlackStone.png")
        self.blackStone.scaled(QSize(int(squareSide), int(squareSide)))
        self.empty = QPixmap("Empty.png")
        self.empty.scaled(QSize(int(squareSide), int(squareSide)))


        """self.whiteQlabel = QLabel()
        self.whiteQlabel.setPixmap(self.whiteStone)
        self.boardLayout.addWidget(self.whiteQlabel)
        self.whiteQlabel.setStyleSheet("background-image: url(Empty.png)")

        self.boardLayout.addStretch(15)

        self.blackQlabel = QLabel()
        self.blackQlabel.setPixmap(self.blackStone)
        self.boardLayout.addWidget(self.blackQlabel)
        self.blackQlabel.setStyleSheet("background-image: url(Empty.png)")

        self.emptyQlabel = QLabel()
        self.emptyQlabel.setPixmap(self.empty)
        #self.boardLayout.addWidget(self.emptyQlabel)
        self.emptyQlabel.setStyleSheet("background-image: url(Empty.png)")

        self.boardGridLayout.addWidget(self.blackQlabel, 0, 1)
        self.boardGridLayout.addWidget(self.whiteQlabel, 0, 10)
        self.setLayout(self.boardLayout)"""

        #self.setLayout(self.boardLayout)

    def resizeEvent(self, event):
        # Create a square base size of 10x10 and scale it to the new size
        # maintaining aspect ratio.
        if self.contentsRect().height()> self.contentsRect().width():
            new_size = QtCore.QSize(self.contentsRect().width(), self.contentsRect().width())
        else:
            new_size = QtCore.QSize(self.contentsRect().height(), self.contentsRect().height())
        self.resize(new_size)
        painter = QPainter(self)
        self.drawPieces(painter)


    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''

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
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location ["+str(event.position().x())+","+str(event.position().y())+"]"     # the location where a mouse click was registered
        print("mousePressEvent() - "+clickLoc)
        # TODO you could call some game logic here
        if self.squareWidth() <= self.squareHeight():
            squareSide = self.squareWidth()
        else:
            squareSide = self.squareHeight()
        for row in range(0, Board.boardHeight+1):
            for col in range(0, Board.boardWidth+1):
                colTransformation = squareSide * 0.5 + squareSide * col
                rowTransformation = squareSide * 0.5 + squareSide * row
                if (event.position().x()+5>colTransformation)&(event.position().x()-5<colTransformation)&(event.position().y()+5>rowTransformation)&(event.position().y()-5>rowTransformation):
                    print("piece placed")
                    self.go.logic.addPiece('W',colTransformation,rowTransformation)

        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game


    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black
        painter.setPen(QPen(self.brushColor, self.brushSize))
        painter.fillRect(QRect(0, 0, self.contentsRect().width(), self.contentsRect().height()),
                         QColor("#0629F0"))

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
                self.brushColor = QColor("#E0BD6B")



    def drawPieces(self, painter):
        '''draw the prices on the board'''
        #colour = Qt.GlobalColor.transparent # empty square could be modeled with transparent pieces

        if self.squareWidth()<=self.squareHeight():
            squareSide = self.squareWidth()
        else:
            squareSide = self.squareHeight()
        image = QRect(0, 0, int(squareSide), int(squareSide))
        for row in range(0, Board.boardHeight+1):
            for col in range(0, Board.boardWidth+1):
                painter.save()
                colTransformation = squareSide * col
                rowTransformation = squareSide * row
                if self.go.logic.piecesArray[col,row]=='W':
                    piece = QRect(int(colTransformation),int(rowTransformation),int(squareSide), int(squareSide))
                    self.whiteStone.scaled(QSize(int(squareSide), int(squareSide)))
                    painter.drawPixmap(piece, self.whiteStone, image)
                elif self.go.logic.piecesArray[col,row]=='B':
                    piece = QRect(int(colTransformation),int(rowTransformation), int(squareSide), int(squareSide))
                    self.blackStone.scaled(QSize(int(squareSide), int(squareSide)))
                    painter.drawPixmap(piece, self.blackStone, image)
                painter.restore()
