
import sys
from  UI_Frame import Ui_CreateLogin



from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from pymongo import MongoClient




class CreateLoginWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui =Ui_CreateLogin.Ui_CreateLogin()
        # 初始化界面
        self.ui.setupUi(self)
        #按键响应
        self.ui.CreateUser.clicked.connect(self.on_click_CreateUser)


    def on_click_CreateUser(self):
      #获取账号文本内容
      Account=self.ui.lineEditAccount.text()
      #获取密码文本内容
      Password=self.ui.lineEditPassword.text()

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
        userinfo={
            'UserName':Account,
            'PassWord':Password,
        }

        if co.find_one({'UserName':Account}) :
          msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '用户名已存在请更换用户名')
          msg_box.exec_() 
        else :
          result=co.insert_one(userinfo)
          msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '成功创建')
          msg_box.exec_() 


if __name__=='__main__':
    app = QApplication(sys.argv)
    a= CreateLoginWindow()
    a.show()
    sys.exit(app.exec_())
      





