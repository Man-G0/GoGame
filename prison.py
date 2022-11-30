from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint, QRect, QSize




class Prison(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.go = parent
        self.blackList = parent.logic.bCaptured

    def paintEvent(self, event):
        self.setMinimumSize(100, 300)

        painter = QPainter(self)
        painter.fillRect(QRect(0, 0, self.contentsRect().width(), self.contentsRect().height()), self.go.backgroundColor)

        self.size = int(self.contentsRect().width()/4)
        self.whiteStone = QPixmap("WhiteStone.png")
        self.whiteStone.scaled(QSize(self.size, self.size))
        self.blackStone = QPixmap("BlackStone.png")
        self.blackStone.scaled(QSize(self.size, self.size))

        image = QRect(0, 0, 70, 70)
        piece = QRect(int(self.contentsRect().width()/4), 100, self.size, self.size)
        self.blackStone.scaled(QSize(self.size, self.size))
        painter.drawPixmap(piece, self.blackStone, image)



