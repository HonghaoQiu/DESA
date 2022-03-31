import sys
from  UI_Frame import Ui_Login 
import Main
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from pymongo import MongoClient



class MainLoginWindow(QDialog):

    username=''
    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui =Ui_Login.Ui_Login()
        # 初始化界面
        self.ui.setupUi(self)
        #按键响应
        self.ui.pushButtonRegister.clicked.connect(self.on_click_pushButtonRegister)
        self.ui.pushButtonLogin.clicked.connect(self.on_click_pushButtonLogin)

    #按下注册键后  
    def on_click_pushButtonRegister(self):
        msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '请联系管理员创建账户')
        msg_box.exec_()
    #按下登录键后
    def on_click_pushButtonLogin(self):
        #获取账号文本内容
        Account=self.ui.AccountEdit.text()
        #获取密码文本内容
        Password=self.ui.PasswordEdit.text()
        #依次判断不同情况
        if Account=="" or Password == "":
            msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '账号或密码为空')
            msg_box.exec_()  
        else: 
            #链接mongodb
            client=MongoClient('localhost',27017)
            #取得对应的collection名字为UserInfo
            collectionName="UserInfo"
            db=client.Users
            co=db[collectionName]
            #查找的用户名密码
            condition = {'UserName':Account,
                    'PassWord':Password,}  
            if co.find_one(condition) :
                self.username=Account
                msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '登陆成功')
                msg_box.exec_() 
                self.accept() 
            else:
                msg_box = QMessageBox(QMessageBox.Warning, '温馨提示', '账号或密码错误')
                msg_box.exec_()   







