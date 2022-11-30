from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QCursor, QPixmap, QColor
from board import Board
from prison import Prison
from game_logic import GameLogic
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.backgroundColor = QColor("#E0BD6B")
        self.gridColor = Qt.GlobalColor.black

        self.initLogic()
        self.initUI()


    def initLogic(self):
        self.logic = GameLogic()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
        self.board = Board(self, self.logic)
        self.prison = Prison(self)
        if self.board.squareWidth()<=self.board.squareHeight():
            squareSide = self.board.squareWidth()
        else:
            squareSide = self.board.squareHeight()
        self.cursor_pix_white = QPixmap('WhiteStone.png')
        self.cursor_pix_black = QPixmap('BlackStone.png')

        self.scoreBoard = ScoreBoard(self.board)

        self.setCentralWidget(Layout(self.board, self.scoreBoard, self.prison))

        self.resize(1000, 650)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def cursor(self):
        if self.logic.currentPlayer == "W":
            self.board.setCursor(self.cursor_white)
        elif self.logic.currentPlayer == "B":
            self.board.setCursor(self.cursor_black)



    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        """size = self.geometry()
        self.move(int(screen.x() - size.width()/2), int(screen.y() - size.height()/2))"""




class Layout(QWidget):
    def __init__(self, board, scoreBoard, prison):
        super().__init__()
        hbox = QHBoxLayout()
        hbox.addWidget(prison, 1)
        hbox.addWidget(board, 3)
        hbox.addWidget(scoreBoard, 1)
        self.setLayout(hbox)
