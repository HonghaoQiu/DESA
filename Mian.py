from fileinput import filename
from re import I
import sys
import Ui_dilizhijian


from PyQt5.QtWidgets import *
                   
DataID = 1
NumOfData = 1

def on_click_OpenFile():
    FilePath, _  =QFileDialog.getOpenFileName(None,"选择打开文件")
    ui.FilePath.setText(FilePath)
    
def on_click_First():
     global DataID
     DataID=1
     ui.ErrorLocation.clear()
     ui.ErrorType.clear()
     ui.ErrorDescription.clear()

def on_click_Previous():
     global DataID
     if DataID==1:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '已是首条')
            msg_box.exec_()
     else:    
            DataID=DataID-1   
     ui.ErrorLocation.clear()
     ui.ErrorType.clear()
     ui.ErrorDescription.clear()

def on_click_Next():
     global DataID
     if DataID==NumOfData :
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '已是末条')
            msg_box.exec_()
     else:    
         DataID=DataID+1
     print(DataID)
     ui.ErrorLocation.clear()
     ui.ErrorType.clear()
     ui.ErrorDescription.clear()

def on_click_Last():
     global DataID
     DataID = NumOfData
     print(DataID)
     ui.ErrorLocation.clear()
     ui.ErrorType.clear()
     ui.ErrorDescription.clear()

def on_click_Record():
    global NumOfData
    NumOfData = NumOfData + 1
    ErrorLocation=ui.ErrorLocation.toPlainText()
    ErrorType=ui.ErrorType.toPlainText()
    ErrorDescription=ui.ErrorDescription.toPlainText()
   




if __name__=='__main__':
    app = QApplication(sys.argv)
    mainWindow = QMainWindow()
    ui = Ui_dilizhijian.Ui_MainWindow()
    ui.setupUi(mainWindow)
    ui.OpenFile.clicked.connect(on_click_OpenFile) 

    ui.First.clicked.connect(on_click_First)
    ui.Previous.clicked.connect(on_click_Previous)
    ui.Next.clicked.connect(on_click_Next)
    ui.Last.clicked.connect(on_click_Last)

    ui.Record.clicked.connect(on_click_Record)
    mainWindow.show()
    
    sys.exit(app.exec_())


