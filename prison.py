from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint, QRect, QSize



class Prison(QFrame):

    def __init__(self, parent, board):
        super().__init__(parent)

        self.go = parent
        self.board = board

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
        prisonWidth = self.contentsRect().width()
        prisonHeight = self.contentsRect().height()
        self.board.drawPrison(painter, prisonWidth,prisonHeight,self.size)