from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint, QRect
from PyQt6.QtGui import QPainter, QPixmap, QColor
from PyQt6.QtTest import QTest
from piece import Piece

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location

    boardWidth  = 7    # board is 7 squares wide
    boardHeight = 7     # board is 7 squares high
    timerSpeed  = 1     # the timer updates every 1 millisecond
    counter     = 10    # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        #self.timer = QBasicTimer()  # create a timer for the game
        #self.isStarted = False      # game is not currently started
        #self.start()                # start the game which will start the timer
        self.setStyleSheet("background-color: #E0BD6B")
        boardImage = QPixmap("board-19x19.jpg")
        """self.boardWidth = boardImage.width()
        self.boardHeight = boardImage.height()
        print("w: "+ str(self.boardWidth)+", h: "+str(self.boardHeight))"""
        self.setFixedSize(800, 800)
        self.boardGridLayout = QGridLayout()

        self.boardLayout = QVBoxLayout()


        whiteStone = QPixmap("WhiteStone.png")
        blackStone = QPixmap("BlackStone.png")
        empty = QPixmap("Empty.png")

        self.whiteQlabel = QLabel()
        self.whiteQlabel.setPixmap(whiteStone)
        self.boardLayout.addWidget(self.whiteQlabel)
        self.whiteQlabel.setStyleSheet("background-image: url(Empty.png)")

        self.blackQlabel = QLabel()
        self.blackQlabel.setPixmap(blackStone)
        self.boardLayout.addWidget(self.blackQlabel)
        self.blackQlabel.setStyleSheet("background-image: url(Empty.png)")

        self.emptyQlabel = QLabel()
        self.emptyQlabel.setPixmap(empty)
        self.boardLayout.addWidget(self.emptyQlabel)
        self.emptyQlabel.setStyleSheet("background-image: url(Empty.png)")

        """for i in range (0,6):
            for j in range(0,6):
                self.boardGridLayout.addWidget(self.blackQlabel,i,j)"""

        #self.boardGridLayout.addWidget(self.blackQlabel, 0, 1)
        #self.boardGridLayout.addWidget(self.whiteQlabel, 0, 1)
        self.setLayout(self.boardLayout)

        #self.setLayout(self.boardLayout)







    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.boardWidth/self.contentsRect().width()

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

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
        #self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location ["+str(event.position().x())+","+str(event.position().y())+"]"     # the location where a mouse click was registered
        print("mousePressEvent() - "+clickLoc)
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game


    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black
        for row in range(0, Board.boardHeight):
            for col in range (0, Board.boardWidth):
                painter.save()
                print("square width: "+ str(self.squareWidth()))
                print("square Height: " + str(self.squareHeight()))
                colTransformation = self.squareWidth()* col # TODO set this value equal the transformation in the column direction
                rowTransformation = self.squareHeight()* row                      # TODO set this value equal the transformation in the row direction
                painter.translate(colTransformation,rowTransformation)
                painter.fillRect(QRect(int(colTransformation),int(rowTransformation),int(self.squareWidth()),int(self.squareHeight())),QColor(0,0,0))
                painter.restore()
                self.brushColor = Qt.GlobalColor.black

    def drawPieces(self, painter):
        '''draw the prices on the board'''
        colour = Qt.GlobalColor.transparent # empty square could be modeled with transparent pieces
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate()

                # TODO draw some the pieces as ellipses
                # TODO choose your colour and set the painter brush to the correct colour
                radius = self.squareWidth() / 4
                center = QPointF(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()
