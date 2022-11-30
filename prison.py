from PyQt6.QtWidgets import QFrame
from PyQt6.QtGui import QPainter, QPixmap, QColor, QPen
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint, QRect, QSize




class Prison(QFrame):  # base the board on a QFrame widget

    def __init__(self, parent):
        super().__init__(parent)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(QRect(0, 0, self.contentsRect().width(), self.contentsRect().height()),QColor("#0629F0"))
