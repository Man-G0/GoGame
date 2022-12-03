from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint, QRect, QSize



class Prison(QFrame):

    def __init__(self, parent, board):
        super().__init__(parent)

        self.go = parent
        self.board = board
        self.blackList = parent.logic.bCaptured
        self.whiteList = parent.logic.wCaptured
        self.whiteStone = QPixmap("WhiteStone.png")
        self.size = int(self.contentsRect().width() / 4)
        self.whiteStone.scaled(QSize(self.size, self.size))
        self.blackStone = QPixmap("BlackStone.png")
        self.blackStone.scaled(QSize(self.size, self.size))
        self.board.updatePrison.connect(self.paintEvent)
        self.a = 0



    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawPrison(painter)
    def drawPrison(self,painter):
        self.setMinimumSize(100, 300)
        self.a+=1
        print(self.a)
        painter.fillRect(QRect(0, 0, self.contentsRect().width(), self.contentsRect().height()), self.go.backgroundColor)

        image = QRect(0, 0, 70, 70)
        painter.save()
        if self.a%2==0:
            print("pair")
            #piece = QRect(int(self.contentsRect().width() / 9), 100, self.size, self.size)
            piece = QRect(0, 100, self.size, self.size)
            painter.drawPixmap(piece, self.blackStone, image)

        for i in range(0, len(self.blackList)):
            #print(self.blackStone[i])
            piece = QRect(int(self.contentsRect().width() / 9), 100, self.size, self.size)
            painter.drawPixmap(piece, self.blackStone, image)
        for i in range(0, len(self.whiteList)):
            piece = QRect(int(self.contentsRect().width() / 9*i), 100, self.size, self.size)
            painter.drawPixmap(piece, self.whiteStone, image)
        painter.restore()