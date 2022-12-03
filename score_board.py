from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel, \
    QPushButton
from PyQt6.QtCore import pyqtSlot


class ScoreBoard(QWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self, board):
        super().__init__()
        self.initUI(board)

    def initUI(self, board):
        '''initiates ScoreBoard UI'''
        self.board = board
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')

        #self.go = Go()
        #create a widget to hold other widgets
        self.mainLayout = QVBoxLayout()
        self.mainLayout = QVBoxLayout()

        #create two labels which will be updated by signals
        self.label_playerTurn = QLabel("Turn to player Black")
        self.button_skipTurn = QPushButton("Skip turn")

        self.button_skipTurn.clicked.connect(self.board.skipTurn)
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.mainLayout.addWidget(self.label_playerTurn)
        self.mainLayout.addWidget(self.button_skipTurn)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.make_connection(board)
        self.setLayout(self.mainLayout)
        self.show()

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''
        #self.go.center()

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.clickUpdate)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)


    def clickUpdate(self, player):
        '''updates the label to show the click location'''
        if player == 'W':
            self.label_playerTurn.setText("Turn to player White")
        elif player == 'B':
            self.label_playerTurn.setText("Turn to player Black")

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemaining):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining:" + str(timeRemaining)
        self.label_timeRemaining.setText(update)
        if timeRemaining < 10:
            self.label_timeRemaining.setStyleSheet("color: red")
        else:
            self.label_timeRemaining.setStyleSheet("color: black")

