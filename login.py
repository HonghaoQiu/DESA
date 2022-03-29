
import sys
import Ui_Login


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from pymongo import MongoClient



class MainLoginWindow(QMainWindow):


  def __init__(self):
    super().__init__()
    # 使用ui文件导入定义界面类
    self.ui =Ui_Login.Ui_LoginWindow()
    # 初始化界面
    self.ui.setupUi(self)
    #按键响应
    self.ui.pushButtonRegister.clicked.connect(self.on_click_pushButtonRegister)
    self.ui.pushButtonLogin.clicked.connect(self.on_click_pushButtonLogin)
    
  def on_click_pushButtonRegister(self):
    msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '请联系管理员创建账户')
    msg_box.exec_()

  def on_click_pushButtonLogin(self):
    Account=self.ui.AccountEdit.text()
    Password=self.ui.PasswordEdit.text()
    if Account=="" or Password == "":
        msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '账号或密码为空')
        msg_box.exec_()  
    else: 
      #链接mongodb
      client=MongoClient('localhost',27017)
      #取得对应的collection
      collectionName="UserInfo"
      db=client.Users
      co=db[collectionName]
      condition = {'UserName':Account,
                    'PassWord':Password,}  
      if co.find_one(condition) :
          msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '登陆成功')
          msg_box.exec_() 
      else:
          msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '账号或密码错误')
          msg_box.exec_()   
          


if __name__=='__main__':

  app = QApplication(sys.argv)
  login= MainLoginWindow()
  login.show()
  sys.exit(app.exec_())


