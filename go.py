from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QColor, QIcon, QAction
from board import Board
from prison import Prison
from game_logic import GameLogic
from score_board import ScoreBoard
from theme import Theme


class Go(QMainWindow):
    def __init__(self, app):
        '''
        inti function
        input : the app
        '''
        super().__init__()
        self.app = app
        self.getListTheme()

        self.board = None
        self.prison = None
        self.mainMenu = self.menuBar()  # create a menu bar now because we need it to be created wen we applied theme
        self.changeTheme(self.listTheme[0].file)

        self.setWindowIcon(QIcon("assets/icon.png"))
        self.initLogic()
        self.initUI()

    def changeTheme(self, file):
        '''
        function to change the theme
        input : the name of the file where is the color
        '''
        self.getColorHex(file)

        self.backgroundBoardColor = QColor(self.backgroundBoardColorhex)
        self.gridColor = Qt.GlobalColor.black
        self.playableColor = QColor(self.playableColorhex)
        self.setStyleSheet("background-color:" + str(self.backgroundWindowColorhex) + "; color : " + str(self.textWindowColorhex))
        self.mainMenu.setStyleSheet("background-color:" + str(self.backgroundMenuColorhex) + "; color:" + str(self.textMenuColorhex))
        if self.board is not None:
            self.board.initCursor()
            self.cursor()

        if self.prison is not None:
            self.prison.initStone()

    def resizeEvent(self, event):
        '''
        function to resize the scoreboard when the window is resized and keep it at the same height of the board
        '''
        self.scoreBoard.resize(QSize(self.scoreBoard.contentsRect().width(), self.board.contentsRect().height()))

    def initLogic(self):
        '''
        function to create the game logic
        '''
        self.logic = GameLogic()

    def initUI(self):
        '''
        ifunction to nitiates the application UI
        '''
        self.board = Board(self, self.logic)
        self.cursor()
        self.prison = Prison(self,self.board)

        self.scoreBoard = ScoreBoard(self.board)

        self.mainLayout = Layout(self.board, self.scoreBoard, self.prison)

        self.setCentralWidget(self.mainLayout)

        # set up menus

        self.mainMenu.setNativeMenuBar(False)
        gameMenu = self.mainMenu.addMenu(" Game")  # add the file menu to the menu bar
        helpMenu = self.mainMenu.addMenu(" Help")  # add the "Help" menu to the menu bar
        themeMenu = self.mainMenu.addMenu(" Theme")

        # game menu item
        restartAction = QAction("Restart",self)
        restartAction.setShortcut("Ctrl+R")
        gameMenu.addAction(restartAction)
        restartAction.triggered.connect(self.board.buttonRestartEvent)

        exitAction = QAction("Exit", self)
        restartAction.setShortcut("Ctrl+E")
        gameMenu.addAction(exitAction)
        exitAction.triggered.connect(self.board.buttonExitEvent)

        # Help Menu
        rulesAction = QAction(QIcon("assets/rules-icon.png"), "Rules", self)
        helpMenu.addAction(rulesAction)
        rulesAction.triggered.connect(self.rules)
        rulesAction.setShortcut("Ctrl+I")

        for theme in self.listTheme:
            themeMenu.addAction(theme.themeAction)

        self.resize(1000, 650)
        self.center()
        self.setWindowTitle('Go')
        self.show()

    def cursor(self):
        '''
        function to change the cursor each time we change the player
        '''
        if self.logic.currentPlayer == "W":
            self.board.setCursor(self.cursor_white)
        elif self.logic.currentPlayer == "B":
            self.board.setCursor(self.cursor_black)

    def center(self):
        '''
        function to centers the window on the screen
        '''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()
        gr.moveCenter(screen)
        self.move(gr.topLeft())

    def rules(self):
        '''
        function to display the rules
        '''
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
        '''
        function to change the skip button when we remove the stones
        '''
        self.scoreBoard.button_skipTurn.setText("calculate scores")
        self.scoreBoard.button_skipTurn.setStyleSheet("background-color:"+self.playableColorhex)

    def getColorHex(self, txtName):
        '''
        function to have the color from the txt file
        '''
        self.backgroundBoardColorhex = '#AF000D' #we put the basic color to be sure to have a color event if there is an issue in the txt
        self.backgroundWindowColorhex = '#FFE3C6'
        self.backgroundMenuColorhex = '#5E0603'
        self.textWindowColorhex = '#2040A9'
        self.textMenuColorhex = '#FF8080'
        self.textPrisonColorhex = '#003333'
        self.playableColorhex = '#D2A665'
        self.whiteStoneFile = 'WhiteStone.png'
        self.blackStoneFile = 'BlackStone.png'
        try :
            colortxt = open("assets/" + txtName, "r")

            for ligne in colortxt:
                ligne = ligne.strip('\n').split(' = ')
                match ligne[0]:
                    case "backgroundBoardColor":
                        self.backgroundBoardColorhex = ligne[1]
                    case "backgroundWindowColor":
                        self.backgroundWindowColorhex = ligne[1]
                    case "backgroundMenuColor":
                        self.backgroundMenuColorhex = ligne[1]
                    case "textWindowColor":
                        self.textWindowColorhex = ligne[1]
                    case "textMenuColor":
                        self.textMenuColorhex = ligne[1]
                    case "textPrisonColor":
                        self.textPrisonColorhex = ligne[1]
                    case "playableColor":
                        self.playableColorhex = ligne[1]
                    case "whiteStoneFile":
                        self.whiteStoneFile = ligne[1]
                    case "blackStoneFile":
                        self.blackStoneFile = ligne[1]

            colortxt.close()

        except:
            print('error with ' + txtName)

    def getListTheme(self):
        '''
        function to read the listtheme.txt
        '''
        try :
            themetxt = open("assets/listTheme.txt", "r")
            self.listTheme = []

            for ligne in themetxt:
                ligne = ligne.strip('\n').split(' => ')
                self.listTheme.append(Theme(ligne[0], ligne[1], self))

            themetxt.close()
        except:
            print('error with listTheme.txt')
            self.listTheme = [Theme('color1.txt', 'theme1', self)]


class Layout(QWidget):
    '''
    class to create the layout
    '''
    def __init__(self, board, scoreBoard, prison):
        '''
        init function that create the layout
        '''
        super().__init__()

        self.prisonSize = 1
        self.boardSize = 3
        self.scoreSize = 1

        hbox = QHBoxLayout()
        hbox.addWidget(prison, self.prisonSize)
        hbox.addWidget(board, self.boardSize)
        hbox.addWidget(scoreBoard, self.scoreSize)
        self.setLayout(hbox)
