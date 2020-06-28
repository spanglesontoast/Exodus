from PySide2.QtWidgets import QApplication,QMainWindow, QAction
import sys
from PySide2.QtGui import QIcon



class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Note Pad Application")
        self.setGeometry(300,300,500,400)

        self.create_menu()

        self.show()


    def create_menu(self):
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        viewMenu = mainMenu.addMenu("View")
        editMenu = mainMenu.addMenu("Edit")
        searchMenu = mainMenu.addMenu("Font")
        helpMenu = mainMenu.addMenu("Help")

        openAction = QAction(QIcon('open.png'), "Open", self)
        openAction.setShortcut("Ctrl+O")

        saveAction = QAction(QIcon('save.png'), "Save", self)
        saveAction.setShortcut("Ctrl+S")

        exitAction = QAction(QIcon('exit.png'), "Exit", self)
        exitAction.setShortcut("Ctrl+X")

        exitAction.triggered.connect(self.exit_app)



        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)


    def exit_app(self):
        self.close()










myApp = QApplication(sys.argv)
window = Window()
myApp.exec_()
sys.exit(0)