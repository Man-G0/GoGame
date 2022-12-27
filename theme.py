from PyQt6.QtGui import QAction


class Theme:
    def __init__(self, file, name, go):
        '''
        init function
        '''
        self.file = file
        self.name = name
        self.go = go
        self.themeAction = QAction(self.name, self.go)
        self.themeAction.triggered.connect(self.changeTheme)

    def changeTheme(self):
        '''
        methode execute to change the theme
        '''
        self.go.changeTheme(self.file)
