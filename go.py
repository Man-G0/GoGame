from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QPoint, QSize
from PyQt6.QtGui import QCursor, QPixmap, QColor, QIcon, QPainter, QAction
from board import Board
from prison import Prison
from game_logic import GameLogic
from score_board import ScoreBoard


class Go(QMainWindow):
    def __init__(self,app):
        super().__init__()
        self.app = app
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
        self.rulesWidget.setStyleSheet("background-color:"+str(self.backgroundWindowColorhex) +"; color : "+str(self.textWindowColorhex))

        rulesLayout = QVBoxLayout()
        rulesLayout.addStretch(1)

        # Display of the Drawing role icon
        qLabel1 = QLabel("1.    The board is empty at the onset of the game (unless players agree to place a handicap).")
        qLabel2 = QLabel("2.    Black makes the first move, after which White and Black alternate.")
        qLabel3 = QLabel("3.    A move consists of placing one stone of one's own color on an empty intersection on the board.")
        qLabel4 = QLabel("4.    A player may pass their turn at any time.")
        qLabel51= QLabel("5.    A stone or solidly connected group of stones of one color is captured and removed from the board when ")
        qLabel52= QLabel("      all the intersections directly adjacent to it are occupied by the enemy. (Capture of the enemy takes precedence over self-capture.)")
        qLabel6 = QLabel("6.    No stone may be played so as to recreate a former board position.")
        qLabel7 = QLabel("7.    Two consecutive passes end the game.")
        qLabel8 = QLabel("8.    A player's area consists of all the points the player has either occupied or surrounded.")
        qLabel9 = QLabel("9.    The player with more area wins.")
        
        hBoxLabel1 = QHBoxLayout()
        hBoxLabel1.addWidget(qLabel1)
        hBoxLabel1.addStretch(1)
        rulesLayout.addLayout(hBoxLabel1)
        
        hBoxLabel2 = QHBoxLayout()
        hBoxLabel2.addWidget(qLabel2)
        hBoxLabel2.addStretch(1)
        rulesLayout.addLayout(hBoxLabel2)

        hBoxLabel3 = QHBoxLayout()
        hBoxLabel3.addWidget(qLabel3)
        hBoxLabel3.addStretch(1)
        rulesLayout.addLayout(hBoxLabel3)

        hBoxLabel4 = QHBoxLayout()
        hBoxLabel4.addWidget(qLabel4)
        hBoxLabel4.addStretch(1)
        rulesLayout.addLayout(hBoxLabel4)

        hBoxLabel51 = QHBoxLayout()
        hBoxLabel51.addWidget(qLabel51)
        hBoxLabel51.addStretch(1)
        rulesLayout.addLayout(hBoxLabel51)

        hBoxLabel52 = QHBoxLayout()
        hBoxLabel52.addWidget(qLabel52)
        hBoxLabel52.addStretch(1)
        rulesLayout.addLayout(hBoxLabel52)

        hBoxLabel6 = QHBoxLayout()
        hBoxLabel6.addWidget(qLabel6)
        hBoxLabel6.addStretch(1)
        rulesLayout.addLayout(hBoxLabel6)

        hBoxLabel7 = QHBoxLayout()
        hBoxLabel7.addWidget(qLabel7)
        hBoxLabel7.addStretch(1)
        rulesLayout.addLayout(hBoxLabel7)

        hBoxLabel8 = QHBoxLayout()
        hBoxLabel8.addWidget(qLabel8)
        hBoxLabel8.addStretch(1)
        rulesLayout.addLayout(hBoxLabel8)

        hBoxLabel9 = QHBoxLayout()
        hBoxLabel9.addWidget(qLabel9)
        hBoxLabel9.addStretch(1)
        rulesLayout.addLayout(hBoxLabel9)



        #Text part of the rules
        rulesLink = QLabel()
        urlLink = "<a href=\"https://en.wikipedia.org/wiki/Rules_of_Go\">Click this link to go to the wikipedia page for the rules of GO </a>"
        rulesLink.setText(urlLink)
        rulesLink.setOpenExternalLinks(True)
        rulesLayout.addWidget(rulesLink)


        rulesText = QLabel()
        rulesText.setText("\t\tMay the best win")
        rulesLayout.addWidget(rulesText)

        rulesLayout.addStretch(1)
        self.rulesWidget.setLayout(rulesLayout)

        self.rulesWidget.show()

        gr = self.rulesWidget.frameGeometry()
        screen = self.screen().availableGeometry().center()
        gr.moveCenter(screen)
        self.rulesWidget.move(gr.topLeft())

    def deadStonesEnd(self):
        self.scoreBoard.button_skipTurn.setText("calculate scores")
        self.scoreBoard.button_skipTurn.setStyleSheet("background-color:"+self.playableColorhex)

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
