from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt
from board import Board
from game_logic import GameLogic
from score_board import ScoreBoard


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initLogic()
        self.initUI()

    def initLogic(self):
        self.logic = GameLogic()
        self.logic.addPiece('W', 2, 5)
        self.logic.addPiece('B', 3, 5)
        self.logic.addPiece('W', 2, 6)
        self.logic.printPiecesArray()
        self.logic.calcLiberties()
        self.logic.printLibertiesArray()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
        self.board = Board(self)
        self.scoreBoard = ScoreBoard(self.board)

        self.setCentralWidget(Layout(self.board, self.scoreBoard))

        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        #size = self.geometry()
        #self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)


class Layout(QWidget):
    def __init__(self, board, scoreBoard):
        super().__init__()
        hbox = QHBoxLayout()
        hbox.addWidget(board, 2)
        hbox.addWidget(scoreBoard, 1)
        self.setLayout(hbox)
