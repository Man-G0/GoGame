from PyQt6.QtWidgets import QApplication
from go import Go
import sys

app = QApplication([])
myGo = Go(app)
sys.exit(app.exec())