import Login
import Main
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore

if __name__=='__main__':
    app = QApplication(sys.argv)
    login= Login.MainLoginWindow()
    login.show()
    if login.exec_() == QDialog.Accepted:
        mainWindow = Main.MainWindow()
        mainWindow.username=login.username
        mainWindow.show()
        sys.exit(app.exec_())