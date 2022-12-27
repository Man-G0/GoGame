from PyQt6.QtGui import QAction


class Theme:
    def __init__(self, file, name, go):
        self.file = file
        self.name = name
        self.go = go
        self.themeAction = QAction(self.name, self.go)
        self.themeAction.triggered.connect(self.changeTheme)

    def changeTheme(self):
        self.go.changeTheme(self.file)
