import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QFrame, QWidget, QVBoxLayout, QLabel, QGridLayout, QHBoxLayout, QSizePolicy, QPushButton
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint, QRect, QSize
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen, QBrush, QCursor, QIcon
from PyQt6.QtTest import QTest
from piece import Piece

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerBSignal = pyqtSignal(int) # signal sent when timer is updated
    updateTimerWSignal = pyqtSignal(int)
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location
    updatePrison = pyqtSignal(str)
    boardWidth  = 6    # board is 6 squares wide
    boardHeight = 6     # board is 6 squares high
    timerSpeed  = 1000     # the timer updates every 1 second
    totalTime = 120
    counterB = totalTime    # the number the counter will count down from
    counterW = totalTime
    cursorCoef = 0.9

    def __init__(self, parent, logic):
        super().__init__(parent)
        self.go = parent
        self.logic = logic

        self.widgetEndGame = None
        self.initBoard()

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False      # true if the players are currently playing, false if the game hasn't started yet, or after a double skip/endgame
        self.playGame = False       # true if isStarted was set to true at a point
        self.finished = False       # is set to true if all actions of the game, including the deadstones part were done
        self.setMinimumSize(500, 500)
        self.skipnumber = 0
        self.restart = QWidget()
        self.exit = QWidget()


        if self.squareWidth() <= self.squareHeight():
            self.squareSide = self.squareWidth()
        else:
            self.squareSide = self.squareHeight()
        self.oldSquareSide = self.squareSide
        self.initCursor()

    def initCursor(self):
        self.whiteStone = QPixmap("assets/" + self.go.whiteStoneFile)
        self.whiteStone.scaled(QSize(int(self.squareSide), int(self.squareSide)))
        self.blackStone = QPixmap("assets/" + self.go.blackStoneFile)
        self.blackStone.scaled(QSize(int(self.squareSide), int(self.squareSide)))
        self.go.cursor_scaled_pix_white = self.whiteStone.scaled(QSize(int(self.squareSide * self.cursorCoef), int(self.squareSide * self.cursorCoef)))
        self.go.cursor_scaled_pix_black = self.blackStone.scaled(QSize(int(self.squareSide * self.cursorCoef), int(self.squareSide * self.cursorCoef)))
        self.go.cursor_white = QCursor(self.go.cursor_scaled_pix_white, -1, -1)
        self.go.cursor_black = QCursor(self.go.cursor_scaled_pix_black, -1, -1)


    def resizeEvent(self, event):

        if self.contentsRect().height() > self.contentsRect().width():
            new_size = QtCore.QSize(self.contentsRect().width(), self.contentsRect().width())
        else:
            new_size = QtCore.QSize(self.contentsRect().height(), self.contentsRect().height())
        self.resize(new_size)
        self.go.scoreBoard.resize(QSize(self.go.scoreBoard.contentsRect().width(), self.contentsRect().height()))
        if self.squareWidth()<=self.squareHeight():
            self.squareSide = self.squareWidth()
        else:
            self.squareSide = self.squareHeight()
        if self.oldSquareSide != self.squareSide:
            self.oldSquareSide = self.squareSide
            self.go.cursor_scaled_pix_white = self.whiteStone.scaled(QSize(int(self.squareSide * self.cursorCoef), int(self.squareSide * self.cursorCoef)))
            self.go.cursor_scaled_pix_black = self.blackStone.scaled(QSize(int(self.squareSide * self.cursorCoef), int(self.squareSide * self.cursorCoef)))
            self.go.cursor_white = QCursor(self.go.cursor_scaled_pix_white, -1, -1)
            self.go.cursor_black = QCursor(self.go.cursor_scaled_pix_black, -1, -1)
            self.go.cursor()



    def squareWidth(self):
        '''returns the width of one square in the board'''
        return (self.contentsRect().width()-(self.contentsRect().width()/self.boardWidth))/self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return (self.contentsRect().height()-(self.contentsRect().height()/self.boardHeight)) / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True                       # set the boolean which determines if the game has started to TRUE
        self.timer.start(self.timerSpeed, self)     # start the timer with the correct speed
        self.clickLocationSignal.emit(self.logic.currentPlayer)

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if self.logic.currentPlayer == "B":
                if self.counterB == 0:
                    self.endGame("BNoTime")
                else:
                    self.counterB -= 1
                    self.updateTimerBSignal.emit(self.counterB)
            elif self.logic.currentPlayer == "W":
                if self.counterW == 0:
                    self.endGame("WNoTime")
                else:
                    self.counterW -= 1
                    self.updateTimerWSignal.emit(self.counterW)
        else:
            super(Board, self).timerEvent(event)      # if we do not handle an event we should pass it to the super
                                                        # class for handling
    def skipTurn(self):
        if self.finished:
            pass
        else:
            if not self.isStarted and self.playGame:
                self.endGame("deadStones were retired")
            else:
                self.skipnumber += 1
                self.counter = 20
                if self.skipnumber < 2:
                    if self.logic.currentPlayer == "W":
                        self.logic.currentPlayer = "B"
                    elif self.logic.currentPlayer == "B":
                        self.logic.currentPlayer = "W"
                    self.go.cursor()
                    self.clickLocationSignal.emit(self.logic.currentPlayer)
                else:
                    self.endGame("2 skips")


    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        self.drawBoardSquares(painter)
        self.playablePosition(painter)
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        posX = event.position().x()
        posY = event.position().y()
        if self.squareWidth() <= self.squareHeight():
            self.squareSide = self.squareWidth()
        else:
            self.squareSide = self.squareHeight()
        if self.logic.currentPlayer == "W":
            self.listPlayable = self.logic.findWPlayable()
        elif self.logic.currentPlayer == "B":
            self.listPlayable = self.logic.findBPlayable()
        for col in range(0, Board.boardWidth+1):
            for row in range(0, Board.boardHeight+1):
                colTransformation = self.squareSide * 0.5 + self.squareSide * col
                rowTransformation = self.squareSide * 0.5 + self.squareSide * row

                if (posX+self.squareSide * 0.3>colTransformation)&(posX-self.squareSide * 0.3<colTransformation)&(posY+self.squareSide * 0.3>rowTransformation)&(posY-self.squareSide * 0.3<rowTransformation):
                    if not self.isStarted and self.playGame:
                        self.go.logic.removeDead(col,row)
                        self.go.cursor()
                    elif not self.playGame:
                        if self.listPlayable[col][row]:
                            if not self.isStarted:
                                self.start()  # start the game which will start the timer
                            self.updatePrison.emit("")
                            if self.skipnumber > 0:
                                self.skipnumber = 0
                            self.counter = 20
                            if self.logic.currentPlayer == "W":
                                self.logic.addPiece('W', col, row)
                                self.logic.currentPlayer = "B"
                            elif self.logic.currentPlayer == "B":
                                self.logic.addPiece('B', col, row)
                                self.logic.currentPlayer = "W"
                            self.go.cursor()
                            self.logic.calcTerritori()
                            self.go.scoreBoard.labelTerritoriW.setText(
                                "White Territories : " + str(self.logic.territoriW))
                            self.go.scoreBoard.labelTerritoriB.setText(
                                "Black Territories : " + str(self.logic.territoriB))

        self.clickLocationSignal.emit(self.logic.currentPlayer)

    def endGame(self, reason):
        self.timer.stop()
        self.skipnumber =0
        self.logic.calcPoint()

        self.widgetEndGame = QWidget()
        self.widgetEndGame.setWindowIcon(QIcon("assets/icon.png"))
        self.widgetEndGame.setStyleSheet("background-color:" + str(self.go.backgroundWindowColorhex) + "; color : " + str(
            self.go.textWindowColorhex))
        self.widgetEndGame.setMinimumSize(250, 150)
        self.widgetEndGame.setWindowTitle("Game end")
        labelEnd = QLabel("The game has ended !")
        labelReason = QLabel()

        layoutButtonsEnd = QHBoxLayout()

        buttonRestart = QPushButton("Restart")
        buttonRestart.clicked.connect(self.resetGame)
        layoutButtonsEnd.addWidget(buttonRestart)

        buttonDeadStones = QPushButton("dead stones ?")
        buttonDeadStones.clicked.connect(self.deadStoneEvent)

        buttonExit = QPushButton("Exit")
        buttonExit.clicked.connect(self.exitEvent)
        labelDeadStones = QLabel("You can now choose to remove the dead stones")
        layoutButtonsEnd.addWidget(buttonExit)
        self.playGame = True
        self.isStarted = False
        if reason == "2 skips":
            labelReason.setText("Both players skipped their turn")
            layoutButtonsEnd.addWidget(buttonDeadStones)
        elif reason == "BNoTime":
            labelReason.setText("Black has no time left. White wins")
            self.finished = True
        elif reason == "WNoTime":
            labelReason.setText("White has no time left. Black Wins.")
            self.finished = True
        elif reason == "deadStones were retired":
            labelReason.setText("Dead stones were taken off the board")
            self.finished = True


        self.layoutEnd = QVBoxLayout()
        self.layoutEnd.addWidget(labelEnd)
        self.layoutEnd.addWidget(labelReason)

        layoutScore = QHBoxLayout()

        layoutB = QVBoxLayout()
        widgetB = QWidget()
        widgetB.setStyleSheet("background-color: black ;color : white ;border-radius: 15px")

        layoutW = QVBoxLayout()
        widgetW = QWidget()
        widgetW.setStyleSheet("background-color: white ;color : black; border-radius: 15px")

        winner = QLabel("👑winner👑")
        loser = QLabel("😣")
        layloss = QHBoxLayout()
        layloss.addStretch(1)
        layloss.addWidget(loser)
        layloss.addStretch(1)
        laywin = QHBoxLayout()
        laywin.addStretch(1)
        laywin.addWidget(winner)
        laywin.addStretch(1)

        if reason == "2 skips":
            self.layoutEnd.addWidget(labelDeadStones)
        if reason == "deadStones were retired" or reason=="2 skips":

            if self.logic.scoreW > self.logic.scoreB:
                layoutW.addLayout(laywin)
                layoutB.addLayout(layloss)
            elif self.logic.scoreW < self.logic.scoreB:
                layoutB.addLayout(laywin)
                layoutW.addLayout(layloss)
            else:
                layoutB.addLayout(laywin)
                layoutW.addLayout(laywin)
        elif reason == "WNoTime":
            layoutB.addLayout(laywin)
            layoutW.addLayout(layloss)
        elif reason == "deadStones were retired":
            layoutW.addLayout(laywin)
            layoutB.addLayout(layloss)

        labelTerritoriB = QLabel("Black Territories : " + str(self.logic.territoriB))
        layoutB.addWidget(labelTerritoriB)
        labelScoreB = QLabel("Score : " + str(self.logic.scoreB))
        layoutB.addWidget(labelScoreB)

        labelTerritoriW = QLabel("White Territories : " + str(self.logic.territoriW))
        layoutW.addWidget(labelTerritoriW)
        labelScoreW = QLabel("Score : " + str(self.logic.scoreW))
        layoutW.addWidget(labelScoreW)

        widgetB.setLayout(layoutB)
        widgetW.setLayout(layoutW)
        layoutScore.addWidget(widgetB)
        layoutScore.addWidget(widgetW)
        self.layoutEnd.addLayout(layoutScore)

        self.layoutEnd.addLayout(layoutButtonsEnd)
        self.widgetEndGame.setLayout(self.layoutEnd)

        self.widgetEndGame.show()

        gr = self.widgetEndGame.frameGeometry()
        screen = self.screen().availableGeometry().center()
        gr.moveCenter(screen)
        self.widgetEndGame.move(gr.topLeft())

    def buttonExitEvent(self):
        self.exit.setWindowTitle("exit")
        self.exit.setWindowIcon(QIcon("./assets/icon.png"))
        self.exit.setStyleSheet("background-color:" + str(self.go.backgroundWindowColorhex) + "; color : " + str(self.go.textWindowColorhex))

        exitLayout = QVBoxLayout()

        # Text part
        exitText = QLabel("Do you really want to exit the game? ")
        exitLayout.addWidget(exitText)

        buttonLay = QHBoxLayout()

        buttonYes = QPushButton()
        buttonYes.setText("Yes")
        buttonYes.clicked.connect(self.exitEvent)
        buttonLay.addWidget(buttonYes)

        buttonNo = QPushButton()
        buttonNo.setText("No")
        buttonNo.clicked.connect(self.endExit)
        buttonLay.addWidget(buttonNo)

        exitLayout.addLayout(buttonLay)

        self.exit.setLayout(exitLayout)
        self.exit.show()

        gr = self.exit.frameGeometry()
        screen = self.go.screen().availableGeometry().center()
        gr.moveCenter(screen)
        self.exit.move(gr.topLeft())
    def exitEvent(self):
        sys.exit(self.go.app.exec())

    def endExit(self):
        self.exit.hide()
    def deadStoneEvent(self):
        self.widgetEndGame.hide()
        self.go.deadStonesEnd()

    def buttonRestartEvent(self):

        self.restart.setWindowTitle("restart")
        self.restart.setWindowIcon(QIcon("./assets/icon.png"))
        self.restart.setStyleSheet("background-color:" + str(self.go.backgroundWindowColorhex) + "; color : " + str(self.go.textWindowColorhex))

        restartLayout = QVBoxLayout()

        # Text part
        restartText = QLabel("Do you really want to restart the game? ")
        restartLayout.addWidget(restartText)

        buttonLay = QHBoxLayout()

        buttonYes = QPushButton()
        buttonYes.setText("Yes")
        buttonYes.clicked.connect(self.resetGame)
        buttonLay.addWidget(buttonYes)

        buttonNo = QPushButton()
        buttonNo.setText("No")
        buttonNo.clicked.connect(self.endRestart)
        buttonLay.addWidget(buttonNo)

        restartLayout.addLayout(buttonLay)

        self.restart.setLayout(restartLayout)
        self.restart.show()

        gr = self.restart.frameGeometry()
        screen = self.go.screen().availableGeometry().center()
        gr.moveCenter(screen)
        self.restart.move(gr.topLeft())
    def endRestart(self):
        self.restart.hide()
    def resetGame(self):
        '''clears pieces from the board'''
        if self.restart.isVisible():
            self.restart.hide()

        painter = QPainter()
        self.go.logic.__init__()
        self.drawBoardSquares(painter)
        self.counterB = self.totalTime  # the number the counter will count down from
        self.counterW = self.totalTime
        self.isStarted = False      # game is not currently started
        self.playGame = False
        self.finished = False
        self.skipnumber = 0
        self.go.scoreBoard.labelTerritoriW.setText("White Territories : " + str(self.logic.territoriW))
        self.go.scoreBoard.labelTerritoriB.setText("Black Territories : " + str(self.logic.territoriB))
        self.go.scoreBoard.setTimeWRemaining(self.counterW)
        self.go.scoreBoard.setTimeBRemaining(self.counterB)
        self.go.scoreBoard.button_skipTurn.setText("Skip turn")
        self.go.scoreBoard.button_skipTurn.setStyleSheet("background-color:" + self.go.backgroundWindowColorhex)
        if self.widgetEndGame is not None:
            self.widgetEndGame.setVisible(False)

    def playablePosition(self,painter):

        if self.logic.currentPlayer == "W":
            self.listPlayable = self.logic.findWPlayable()
        elif self.logic.currentPlayer == "B":
            self.listPlayable = self.logic.findBPlayable()

        if self.squareWidth()<=self.squareHeight():
            self.squareSide = self.squareWidth()
        else:
            self.squareSide = self.squareHeight()

        for col in range(0, Board.boardWidth + 1):
            for row in range(0, Board.boardHeight + 1):
                if self.listPlayable[col][row]:
                    self.brushSize = 1
                    self.brushColor = self.go.playableColor
                    painter.setPen(QPen(self.brushColor, self.brushSize))
                    painter.setBrush(QBrush(self.brushColor, Qt.BrushStyle.SolidPattern))
                    colTransformation = self.squareSide * 0.47 + self.squareSide * col
                    rowTransformation = self.squareSide * 0.47 + self.squareSide * row
                    painter.drawEllipse(int(colTransformation), int(rowTransformation), 5,5)


    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black
        painter.setPen(QPen(self.brushColor, self.brushSize))
        painter.fillRect(QRect(0, 0, self.contentsRect().width(), self.contentsRect().height()),self.go.backgroundBoardColor)

        if self.squareWidth()<=self.squareHeight():
            self.squareSide = self.squareWidth()
        else:
            self.squareSide = self.squareHeight()
        for row in range(0, Board.boardHeight):
            for col in range (0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareSide*0.5+self.squareSide* col
                rowTransformation = self.squareSide*0.5+self.squareSide* row
                painter.fillRect(QRect(int(colTransformation),int(rowTransformation),int(self.squareSide),int(self.squareSide)),self.go.backgroundBoardColor)
                painter.drawRect(QRect(int(colTransformation),int(rowTransformation),int(self.squareSide),int(self.squareSide)))
                painter.restore()
                self.brushColor = self.go.backgroundBoardColor



    def drawPieces(self, painter):
        '''draw the prices on the board'''

        if self.squareWidth()<=self.squareHeight():
            self.squareSide = self.squareWidth()
        else:
            self.squareSide = self.squareHeight()
        image = QRect(0, 0, 70, 70)
        for row in range(0, Board.boardHeight+1):
            for col in range(0, Board.boardWidth+1):
                painter.save()
                colTransformation = self.squareSide * col
                rowTransformation = self.squareSide * row
                if self.logic.piecesArray[col][row] is not None:
                    if self.logic.piecesArray[col][row].color == 'W':
                        piece = QRect(int(colTransformation),int(rowTransformation),int(self.squareSide), int(self.squareSide))
                        self.whiteStone.scaled(QSize(int(self.squareSide), int(self.squareSide)))
                        painter.drawPixmap(piece, self.whiteStone, image)
                    elif self.logic.piecesArray[col][row].color == 'B':
                        piece = QRect(int(colTransformation),int(rowTransformation), int(self.squareSide), int(self.squareSide))
                        self.blackStone.scaled(QSize(int(self.squareSide), int(self.squareSide)))
                        painter.drawPixmap(piece, self.blackStone, image)
                painter.restore()



    
