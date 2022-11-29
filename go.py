from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout
from PyQt6.QtCore import Qt, QPoint
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
        self.logic.addPiece('W', 1, 1)
        #self.logic.addPiece('W', 1, 2)
        self.logic.addPiece('B', 1, 0)
        self.logic.addPiece('B', 0, 0)
        self.logic.addPiece('B', 0, 1)
        self.logic.addPiece('B', 0, 2)
        self.logic.addPiece('B', 2, 1)
        self.logic.addPiece('B', 2, 2)
        self.logic.addPiece('B', 1, 3)
        self.logic.printPiecesArray()
        self.logic.calcLiberties()
        self.logic.printLibertiesArray()
        self.logic.printPiecesArray()
        self.logic.printPayable(self.logic.findBPlayable())

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
        self.board = Board(self)
        self.scoreBoard = ScoreBoard(self.board)

        self.setCentralWidget(Layout(self.board, self.scoreBoard))

        self.resize(800,750)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)

        size = self.geometry()
        self.move(int(screen.x() - size.width()/2), int(screen.y() - size.height()/2))
        print(size.width()/2)
        print(screen.x())

        print(size.height()/2)
        print(screen.y())
        #self.move(int((screen.x() - size.x()) / 2),int((screen.y() - size.y()) / 2))



class Layout(QWidget):
    def __init__(self, board, scoreBoard):
        super().__init__()
        hbox = QHBoxLayout()
        hbox.addWidget(board, 2)
        hbox.addWidget(scoreBoard, 1)
        self.setLayout(hbox)
