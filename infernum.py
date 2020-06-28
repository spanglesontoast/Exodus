import asyncio
import sys
import time

from PySide2 import QtCore
from PySide2.QtGui import QIcon, Qt
from PySide2.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QTextEdit, QPushButton,
    QVBoxLayout, QListWidget, QAction, QMenuBar, QGridLayout, QSplitter, QTabWidget,
    QDialog)
from asyncqt import QEventLoop, asyncSlot


class MainWindow(QWidget):

    def closeEvent(self, event):
        print("closing the application maybe we should do this more cleaner")
        sys.exit()

    def showdialog(self):
        dialog = QDialog()
        vbox = QGridLayout(dialog)
        networkLabel = QLabel("Nework List")
        vbox.addWidget(networkLabel)
        b2 = QListWidget(self)

        b2.addItem("localhost")
        b2.addItem("irc.freenode.net")
        b2.addItem("irc.quakenet.net")
        connectButton = QPushButton("Connect")
        addButton = QPushButton("Add")
        editButton = QPushButton("Edit")
        deleteButton = QPushButton("Delete")
        nickLabel = QLabel("Nickname")
        self.userNick = QLineEdit("dave")

        vbox.addWidget(b2, 0, 0)
        vbox.addWidget(connectButton, 1, 0)
        vbox.addWidget(addButton, 2, 0)
        vbox.addWidget(editButton, 3, 0)
        vbox.addWidget(deleteButton, 4, 0)
        vbox.addWidget(nickLabel, 5, 0)
        vbox.addWidget(self.userNick, 6, 0)

        # below we need to grab the username that the user has set in the QlineEdit if there isn't one set we use a default username
        self.nickname = "dave"
        dialog.setWindowTitle("Networks")
        dialog.setWindowIcon(QIcon("./devil.png"))
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec_()

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("./devil.png"))

        #######menu
        mainMenu = QMenuBar()

        fileMenu = mainMenu.addMenu("Infernum 2")

        openAction = QAction(QIcon('open.png'), "Connect", self)
        openAction.setShortcut("Ctrl+O")

        saveAction = QAction(QIcon('save.png'), "Networks", self)
        saveAction.setShortcut("Ctrl+S")

        exitAction = QAction(QIcon('exit.png'), "Exit", self)
        exitAction.setShortcut("Ctrl+X")

        openAction.triggered.connect(self.on_btnFetch_clicked)
        saveAction.triggered.connect(self.showdialog)

        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addAction(exitAction)

        # we use the same layout for both tabs because grid doesn't work :(
        self.layout = QVBoxLayout(self)

        self.layout.addWidget(mainMenu)
        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Server")
        self.tabs.addTab(self.tab2, "#general")

        #####tab 1##########
        self.tab1.layout = QVBoxLayout(self)

        self.tab1.setLayout(self.tab1.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.editResponse = QTextEdit(self)

        self.editResponse.setReadOnly(True)

        self.pushButtonOK = QPushButton(self)
        self.pushButtonOK.setText("Send")
        self.pushButtonOK.hide()
        self.pushButtonOK.clicked.connect(self.on_pushButtonOK_clicked)
        self.pushButtonOK.setAutoDefault(True)

        self.sendMessage = QLineEdit("", self)
        self.sendMessage.returnPressed.connect(self.pushButtonOK.click)

        self.splitter = QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.editResponse)

        # splitter contains it's own grid system see below for adjusting
        self.splitter.setStretchFactor(0, 500)
        self.splitter.setStretchFactor(1, 10)
        self.tab1.layout.addWidget(self.splitter)

        self.tab1.layout.addWidget(self.pushButtonOK)
        self.tab1.layout.addWidget(self.sendMessage)

        ######TAB2########################

        # Create first tab
        self.tab2.layout = QVBoxLayout(self)

        self.tab2.setLayout(self.tab2.layout)

        self.editResponse2 = QTextEdit(self)

        self.editResponse2.setReadOnly(True)

        self.pushButtonOK2 = QPushButton(self)
        self.pushButtonOK2.setText("Send")
        self.pushButtonOK2.hide()
        self.pushButtonOK2.clicked.connect(self.on_pushButtonOK_clicked)
        self.pushButtonOK2.setAutoDefault(True)

        self.editUrl2 = QLineEdit("", self)
        self.editUrl2.returnPressed.connect(self.pushButtonOK.click)

        self.users2 = QListWidget(self)
        self.users2.addItem("dave")

        self.splitter2 = QSplitter(QtCore.Qt.Horizontal)
        self.splitter2.addWidget(self.editResponse2)
        self.splitter2.addWidget(self.users2)
        # splitter contains it's own grid system see below for adjusting
        self.splitter2.setStretchFactor(0, 500)
        self.splitter2.setStretchFactor(1, 10)
        self.tab2.layout.addWidget(self.splitter2)

        self.tab2.layout.addWidget(self.pushButtonOK2)
        self.tab2.layout.addWidget(self.editUrl2)
        #####end of tab 2

    @asyncSlot()
    async def on_pushButtonOK_clicked(self):
        self.writer.write(bytes("PRIVMSG " + "#general" + " :" + self.sendMessage.text() + '\r\n', "UTF-8"))
        self.editResponse.append(self.nickname + ": " + self.sendMessage.text())

    @asyncSlot()
    async def on_btnFetch_clicked(self):
        #self.botnick = "davekells"

        self.editResponse.append('Connected')

        # async def getUsers(writer):
        # populate user tabs
        async def ponger(writer, useful):
            await asyncio.sleep(10)
            if useful.find('PING :') != -1:
                heyhey = useful.strip("PING :")

                writer.write(bytes('PONG :' + heyhey.strip("PING :") + '\r\n', "UTF-8"))
                i = 0
                if (i >= 0):
                    writer.write(bytes("JOIN " + "#general" + "\n", "UTF-8"))
                    i = 1

        async def getusers(useful):
            await asyncio.sleep(10)

        async def pinger(writer):
            await asyncio.sleep(30)
            millis = int(round(time.time() * 1000))
            writer.write(bytes('PING LAG' + str(millis) + '\r\n', "UTF-8"))
            i = 0
            if (i >= 0):
                writer.write(bytes("JOIN " + "#general" + "\n", "UTF-8"))
                i = 1

        try:
            reader, self.writer = await asyncio.open_connection('localhost', 6667)

            millis = int(round(time.time() * 1000))
            self.writer.write(bytes('PING LAG' + str(millis) + '\r\n', "UTF-8"))
            self.writer.write(bytes("NICK " + self.nickname + "\r\n", "UTF-8"))
            self.writer.write(
                bytes("USER " + self.nickname + " " + self.nickname + " " + self.nickname + " :infernum2\r\n", "UTF-8"))

            while True:
                data = await reader.readline()

                # result = re.search("PING :+[0-9]*", stripper)
                # fresh = result.group(0)
                useful = data.decode("UTF-8")
                useful.strip('\n\r')
                if useful.find('PRIVMSG') != -1:
                    self.editResponse2.append(useful)
                    #toaster = ToastNotifier()
                    #toaster.show_toast("New Message", data.decode("UTF-8"), threaded=True)
                else:
                    self.editResponse.append(useful)

                asyncio.ensure_future(ponger(self.writer, useful))
                asyncio.ensure_future(pinger(self.writer))
                # asyncio.ensure_future(getusers(useful))

        except Exception as exc:
            self.editResponse.append('Error: {}'.format(exc))
        else:
            self.editResponse.append('finished for some reason')
        finally:
            self.btnFetch.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    loop = QEventLoop(app)
    asyncio.set_event_loop(loop)

    w = 1024
    h = 768
    mainWindow = MainWindow()
    mainWindow.resize(w, h)
    mainWindow.setWindowTitle('Infernum 2')

    mainWindow.show()
    with loop:
        sys.exit(loop.run_forever())
