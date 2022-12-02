from PyQt6.QtWidgets import QDockWidget, QVBoxLayout, QWidget, QLabel #TODO import additional Widget classes as desired
from PyQt6.QtCore import pyqtSlot
#from go import Go


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
        self.label_playerTurn = QLabel("Turn to player ")
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.mainLayout.addWidget(self.label_playerTurn)
        self.mainLayout.addWidget(self.label_timeRemaining)
        self.make_connection(board)
        self.setLayout(self.mainLayout)
        self.show()

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''

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
    def setTimeRemaining(self, timeRemainng):
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining:" + str(timeRemainng)
        self.label_timeRemaining.setText(update)
        print('slot '+update)
        # self.redraw()

