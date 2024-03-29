from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel, QPushButton, QProgressBar
from PyQt6.QtCore import pyqtSlot


class ScoreBoard(QWidget):
    def __init__(self, board):
        '''
        init function
        '''
        super().__init__()
        self.initUI(board)

    def initUI(self, board):
        '''
        function that initiates the ScoreBoard UI
        '''
        self.board = board
        self.resize(200, 200)
        self.setWindowTitle('ScoreBoard')

        #create a widget to hold other widgets
        self.mainLayout = QVBoxLayout()

        #create two labels which will be updated by signals
        self.label_playerTurn = QLabel("Turn to player Black")
        self.button_skipTurn = QPushButton("Skip turn")
        self.widgetB = QWidget()
        self.button_skipTurn.clicked.connect(self.board.skipTurn)
        self.label_timeB = QLabel("Time left for black : ")
        self.label_timeBRemaining = QLabel(str(int(self.board.counterB / 60))+" min "+str(self.board.counterB % 60)+" sec")
        self.pbarBRemaining = QProgressBar(self, textVisible=False)

        self.pbarBRemaining.setValue(100)
        self.labelTerritoriB = QLabel("Black Territories : " + str(self.board.logic.territoriB))
        layoutB = QVBoxLayout()
        layoutB.addWidget(self.label_timeB)
        layoutB.addWidget(self.label_timeBRemaining)
        layoutB.addWidget(self.pbarBRemaining)
        layoutB.addWidget(self.labelTerritoriB)
        self.widgetB.setLayout(layoutB)
        self.widgetB.setStyleSheet("background-color: black ;color : white ;border-radius: 15px")

        self.widgetW = QWidget()
        self.label_timeW = QLabel("Time left for white : ")
        self.label_timeWRemaining = QLabel(str(int(self.board.counterW / 60))+" min "+str(self.board.counterW % 60)+" sec")
        self.pbarWRemaining = QProgressBar(self,  textVisible=False)
        self.pbarWRemaining.setValue(100)
        self.labelTerritoriW = QLabel("White Territories : " + str(self.board.logic.territoriW))
        layoutW = QVBoxLayout()
        layoutW.addWidget(self.label_timeW)
        layoutW.addWidget(self.label_timeWRemaining)
        layoutW.addWidget(self.pbarWRemaining)
        layoutW.addWidget(self.labelTerritoriW)
        self.widgetW.setLayout(layoutW)
        self.widgetW.setStyleSheet("background-color: white ;color : black; border-radius: 15px")

        self.mainLayout.addWidget(self.label_playerTurn)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.widgetB)
        self.mainLayout.addStretch(1)
        self.mainLayout.addWidget(self.widgetW)
        self.mainLayout.addStretch(6)
        self.mainLayout.addWidget(self.button_skipTurn)
        self.make_connection(board)
        self.setLayout(self.mainLayout)
        self.show()

    def make_connection(self, board):
        '''
        function that handles a signal sent from the board class
        '''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.clickUpdate)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerBSignal.connect(self.setTimeBRemaining)
        board.updateTimerWSignal.connect(self.setTimeWRemaining)

    def clickUpdate(self, player):
        '''
        function that change the player turn label
        '''
        if player == 'W':
            self.label_playerTurn.setText("Turn to player White")
        elif player == 'B':
            self.label_playerTurn.setText("Turn to player Black")

    @pyqtSlot(int)
    def setTimeBRemaining(self, timeBRemaining):
        '''
        function to updates the time remaining label to show the time remaining for the black
        '''
        self.label_timeBRemaining.setText(str(int(timeBRemaining / 60))+" min "+str(timeBRemaining % 60)+" sec")
        val = int((timeBRemaining / self.board.totalTime) * 100)
        self.pbarBRemaining.setValue(val)
        if timeBRemaining < 30:
            self.label_timeBRemaining.setStyleSheet("color: red")
        else:
            self.label_timeBRemaining.setStyleSheet("color: white")

    @pyqtSlot(int)
    def setTimeWRemaining(self, timeWRemaining):
        '''
        function to updates the time remaining label to show the time remaining for the white
        '''
        self.label_timeWRemaining.setText(str(int(timeWRemaining / 60))+" min "+str(timeWRemaining % 60)+" sec")
        val = int((timeWRemaining / self.board.totalTime)*100)
        self.pbarWRemaining.setValue(val)
        if timeWRemaining < 30:
            self.label_timeWRemaining.setStyleSheet("color: red")
        else:
            self.label_timeWRemaining.setStyleSheet("color: black")
