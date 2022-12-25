from PyQt6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QPainter, QPixmap
from PyQt6.QtCore import QRect, QSize

class Prison(QFrame):

    def __init__(self, parent, board):
        super().__init__(parent)

        self.go = parent
        self.board = board

        self.whiteStone = QPixmap("assets/" + self.go.whiteStoneFile)
        self.size = int(self.contentsRect().width() / 4)
        self.whiteStone.scaled(QSize(self.size, self.size))
        self.blackStone = QPixmap("assets/" + self.go.blackStoneFile)
        self.blackStone.scaled(QSize(self.size, self.size))
        self.board.updatePrison.connect(self.paintEvent)

        self.blackList = self.board.logic.bCaptured
        self.whiteList = self.board.logic.wCaptured

        self.capturedWhite = QLabel(str(len(self.whiteList)))
        self.capturedBlack = QLabel(str(len(self.blackList)))
        #self.capturedBlack.setStyleSheet("background-color : white")

        self.prisonLayout = QVBoxLayout()
        self.prisonLayout.addStretch(1)
        self.scoreLayout = QHBoxLayout()
        self.scoreLayout.addStretch(1)
        self.scoreLayout.addWidget(self.capturedBlack)
        self.scoreLayout.addStretch(1)
        self.scoreLayout.addWidget(self.capturedWhite)
        self.scoreLayout.addStretch(1)
        self.prisonLayout.addLayout(self.scoreLayout)
        self.setLayout(self.prisonLayout)

    def resizeEvent(self, event):
        # Create a square base size of 10x10 and scale it to the new size
        # maintaining aspect ratio.
        new_size = QSize(int(self.board.width()*2/5), self.board.contentsRect().height())
        self.resize(new_size)
        self.size = int(self.contentsRect().width() / 4)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawPrison(painter)
    def drawPrison(self,painter):

        self.setMinimumSize(int(self.board.width()*2/5), self.board.height())
        prisonWidth = self.width()
        prisonHeight = self.height()
        painter.fillRect(QRect(0, 0, prisonWidth, prisonHeight), self.go.backgroundBoardColor)
        self.blackList = self.board.logic.bCaptured
        self.whiteList = self.board.logic.wCaptured
        image = QRect(0, 0, 70, 70)
        painter.save()
        self.setStyleSheet("background-color:" +str(self.go.backgroundBoardColorhex) + "; color : " + str(self.go.textPrisonColorhex) +"; font-weight: bold")

        if len(self.blackList)<=20:
            lenB = len(self.blackList)+1
        else :
            lenB = 21

        if len(self.whiteList) <= 20:
            lenW = len(self.whiteList) + 1
        else:
            lenW = 21

        for i in range(1, lenB):
            piece = QRect(int(1 / 3 * prisonWidth-self.size/2), int(prisonHeight-(prisonHeight / 24 * i)-image.height()), self.size, self.size)
            painter.drawPixmap(piece, self.blackStone, image)

        for i in range(1, lenW):
            piece = QRect(int(2 / 3 * prisonWidth-self.size/2), int(prisonHeight-(prisonHeight / 24 * i)-image.height()), self.size, self.size)
            painter.drawPixmap(piece, self.whiteStone, image)
        painter.restore()

        self.capturedWhite.setText(str(len(self.whiteList)))
        self.capturedBlack.setText(str(len(self.blackList)))
        self.update()