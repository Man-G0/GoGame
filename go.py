from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QCursor, QPixmap, QColor, QIcon, QPainter, QAction
from board import Board
from prison import Prison
from game_logic import GameLogic
from score_board import ScoreBoard


class Go(QMainWindow):
    def __init__(self):
        super().__init__()
        self.backgroundBoardColorhex = "#AF000D"
        self.backgroundWindowColorhex = "#FFE3C6"
        self.backgroundMenuColorhex = "#5E0603"
        self.textWindowColorhex = "#2040A9"
        self.textMenuColorhex = "#FF8080"
        self.textPrisonColorhex = "#003333"
        self.playableColorhex = "#D2A665"

        self.backgroundBoardColor = QColor(self.backgroundBoardColorhex)
        self.gridColor = Qt.GlobalColor.black
        self.playableColor = QColor(self.playableColorhex)
        self.setStyleSheet("background-color:"+str(self.backgroundWindowColorhex) +"; color : "+str(self.textWindowColorhex))
        self.setWindowIcon(QIcon("assets/icon.png"))
        self.initLogic()
        self.initUI()

    def resizeEvent(self, event):
        self.scoreBoard.resize(QSize(self.scoreBoard.contentsRect().width(), self.board.contentsRect().height()))
    def initLogic(self):
        self.logic = GameLogic()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
        self.board = Board(self, self.logic)
        self.cursor()
        self.prison = Prison(self,self.board)

        self.scoreBoard = ScoreBoard(self.board)

        self.mainLayout = Layout(self.board, self.scoreBoard, self.prison)



        self.setCentralWidget(self.mainLayout)

        # set up menus
        mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setStyleSheet("background-color:" + str(self.backgroundMenuColorhex) + "; color:" + str(self.textMenuColorhex))
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(" File")  # add the file menu to the menu bar
        helpMenu = mainMenu.addMenu(" Help")  # add the "Help" menu to the menu bar

        # save menu item
        restartAction = QAction(QIcon("./icons/save.png"), "Restart",self)
        restartAction.setShortcut(
            "Ctrl+S")  # connect this save action to a keyboard shortcut, documentation: https://doc.qt.io/qt-6/qaction.html#shortcut-prop
        fileMenu.addAction(
            restartAction)  # add the save action to the file menu, documentation: https://doc.qt.io/qt-6/qwidget.html#addAction
        restartAction.triggered.connect(self.board.buttonRestartEvent)

        # Help Menu
        rulesAction = QAction(QIcon("assets/rules-icon.png"), "Rules", self)
        helpMenu.addAction(rulesAction)
        rulesAction.triggered.connect(self.rules)
        rulesAction.setShortcut("Ctrl+I")

        """contactAction = QAction(QIcon("./icons/support-icon.png"), "Contact us", self)
        contactAction.setShortcut("Ctrl+*")
        helpMenu.addAction(contactAction)
        contactAction.triggered.connect(self.contact)

        AboutUsAction = QAction(QIcon("./icons/dizzy-person.png"), "About us", self)
        AboutUsAction.setShortcut("Ctrl+U")
        helpMenu.addAction(AboutUsAction)
        AboutUsAction.triggered.connect(self.about)"""


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


    def rules(self):
        self.rulesWidget = QWidget()
        self.rulesWidget.setWindowTitle("rules")
        self.rulesWidget.setWindowIcon(QIcon("assets/rules-icon.png"))
        #self.rulesWidget.setStyleSheet("background-color:"+self.draw.backgroundBoardColor)

        rulesLayout = QVBoxLayout()

        # Display of the Drawing role icon
        self.drawingHbox = QHBoxLayout()

        qLabelDrawingText = QLabel()
        qLabelDrawingText.setText("Drawing player: Draw the word +2 points")
        self.drawingHbox.addWidget(qLabelDrawingText)
        self.drawingHbox.addStretch(3)
        rulesLayout.addLayout(self.drawingHbox)

        #Display of the Guessing role icon
        self.guessingHbox = QHBoxLayout()
        qLabelGuessingText = QLabel()
        qLabelGuessingText.setText("Guessing player: Find the word! +1 point")
        self.guessingHbox.addWidget(qLabelGuessingText)
        self.guessingHbox.addStretch(3)
        rulesLayout.addLayout(self.guessingHbox)

        #Text part of the rules
        rulesText = QLabel()
        rulesText.setText("\t\tMay the best win")
        rulesLayout.addWidget(rulesText)

        self.rulesWidget.setLayout(rulesLayout)

        self.rulesWidget.show()


class Layout(QWidget):
    def __init__(self, board, scoreBoard, prison):
        super().__init__()

        self.prisonSize = 1
        self.boardSize = 3
        self.scoreSize = 1

        hbox = QHBoxLayout()
        hbox.addWidget(prison, self.prisonSize)
        hbox.addWidget(board, self.boardSize)
        hbox.addWidget(scoreBoard, self.scoreSize)
        self.setLayout(hbox)
