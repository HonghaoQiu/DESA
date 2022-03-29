
import sys
import os
from  UI_Frame import Ui_dilizhijian


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore




class MainWindow(QMainWindow):
    #用于存储当前谁操作
    username=""
    #索引
    DataID = 0
    #数据数量
    NumOfData = 0
    #
    movex = ""
    movey = ""
    # 
    FilePath=""

    def __init__(self):
        super().__init__()
        self.listErrorLocation=[]
        self.listErrorType=[]
        self.listErrorDescription=[]
        # 使用ui文件导入定义界面类
        self.ui =Ui_dilizhijian.Ui_MainWindow()
        # 初始化界面
        self.ui.setupUi(self)
        #鼠标移入label中变成普通光标
        self.ui.label.setCursor(QtCore.Qt.PointingHandCursor)       #手型光标

        #为每个控件添加相应的响应
        self.ui.OpenFile.clicked.connect(self.on_click_OpenFile) 

        self.ui.First.clicked.connect(self.on_click_First)
        self.ui.Previous.clicked.connect(self.on_click_Previous)
        self.ui.Next.clicked.connect(self.on_click_Next)
        self.ui.Last.clicked.connect(self.on_click_Last)

        self.ui.Find.clicked.connect(self.on_click_Find)

        self.ui.Record.clicked.connect(self.on_click_Record)
        self.ui.Cancel.clicked.connect(self.on_click_Cancel)

    #点击打开文件
    def on_click_OpenFile(self):
        #确保文件路径显示为空
        self.ui.textShow.clear()
        #打开选择文件对话框，并讲文件路径存入FilePath
        self.FilePath, _  =QFileDialog.getOpenFileName(None,"选择打开文件")
        #显示文件路径显示
        self.ui.FilePath.setText(self.FilePath)
        #File_Name为全局变量
        global File_Name
        #获取文件名字以及文件类型
        File_Name,file_extension=os.path.splitext(self.FilePath)
        #如果文档为txt类型，在文档类型中显示
        if file_extension=='.txt': 
            f=open(self.FilePath,'r',encoding='utf-8')
            content=f.readlines()
            for line in content:
                    self.ui.textShow.append(line)
        #若为其它类型则读为图片，此处仅为栅格数据
        else:
            self.ui.label.setPixmap(QPixmap(self.FilePath).scaled(self.ui.label.width(),self.ui.label.height()))
            self.label_w = self.ui.label.width()
            self.label_x = self.ui.label.x()
            self.label_y = self.ui.label.y()
            self.label_h = self.ui.label.height()

        #判断错位信息集是否已经存在，若存在存入临时list中便与操作，特别注意文件名且文件与打开文件位于同一路径下
        if os.path.exists(File_Name+"_错误信息集.txt") == True:
            self.NumOfData=self.ReadDataFile(File_Name+"_错误信息集.txt")
            self.DataID=0
            self.ui.ID.setText("第  "+ str(self.DataID + 1)+"   条")
            self.ui.ErrorLocation.setPlainText(self.listErrorLocation[self.DataID])
            self.ui.ErrorType.setPlainText(self.listErrorType[self.DataID])
            self.ui.ErrorDescription.setPlainText(self.listErrorDescription[self.DataID])
    

    def mousePressEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            self.flag = True

    def mouseReleaseEvent(self, e):  #鼠标释放事件重写
        self.flag = False
        self.movex = ""
        self.movey = ""

    def mouseMoveEvent(self,e):
        if  e.x()>= self.ui.tabWidget.x() and e.x()<=(self.ui.tabWidget.width()+self.ui.tabWidget.x()) and  e.y()>= self.ui.tabWidget.y() and e.y()<=(self.ui.tabWidget.height()+self.ui.tabWidget.y()):
            if self.flag:
                self.x1 = e.x()
                self.y1 = e.y()
            if self.movex != "" and self.movey != "":
                self.label_x = self.label_x + (self.x1 -self.movex)
                self.label_y = self.label_y + (self.y1 -self.movey)
        self.movex = self.x1
        self.movey = self.y1
        self.ui.label.setGeometry(QtCore.QRect(self.label_x, self.label_y, self.label_w, self.label_h))
        self.ui.label.setPixmap(QPixmap(self.FilePath).scaled(self.ui.label.width(),self.ui.label.height()))

    def wheelEvent(self, e):
        angle=e.angleDelta()                                       
        angleY=angle.y()  # 竖直滚过的距离
        if angleY > 0:

            self.label_w*=1.05 
            self.label_h*=1.05                                                    
        elif angleY < 0:
            self.label_w/=1.05 
            self.label_h/=1.05  
        
        self.ui.label.setGeometry(QtCore.QRect(self.label_x, self.label_y, self.label_w, self.label_h))
        self.ui.label.setPixmap(QPixmap(self.FilePath).scaled(self.ui.label.width(),self.ui.label.height()))



    #点击首条
    def on_click_First(self):
        #初始化DataID为0，将界面内容全部刷新并显示数据
        self.DataID=0
        self.ui.ID.setText("第  "+ str(self.DataID + 1)+"   条")
        self.ui.ErrorLocation.setPlainText(self.listErrorLocation[self.DataID])
        self.ui.ErrorType.setPlainText(self.listErrorType[self.DataID])
        self.ui.ErrorDescription.setPlainText(self.listErrorDescription[self.DataID])
    
    #点击上一条
    def on_click_Previous(self):
        #判断是否为首条
        if self.DataID==0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '已是首条')
            msg_box.exec_()
        else:    
            self.DataID=self.DataID-1   
            self.ui.ErrorLocation.setPlainText(self.listErrorLocation[self.DataID])
            self.ui.ErrorType.setPlainText(self.listErrorType[self.DataID])
            self.ui.ErrorDescription.setPlainText(self.listErrorDescription[self.DataID])      
        self.ui.ID.setText("第  "+ str(self.DataID + 1)+"   条")

    #点击下一条
    def on_click_Next(self):
        #判断是否为末条
        if self.DataID==self.NumOfData :
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '已是末条')
            msg_box.exec_()
        else:   
            self.DataID=self.DataID+1
            #判断是否已添加数据，若存在则显示已有数据，若为添加则刷新文本框
            if (len(self.listErrorLocation) - 1) >= self.DataID:
                self.ui.ErrorLocation.setPlainText(self.listErrorLocation[self.DataID])
                self.ui.ErrorType.setPlainText(self.listErrorType[self.DataID])
                self.ui.ErrorDescription.setPlainText(self.listErrorDescription[self.DataID])     
            else: 
                self.ui.ErrorLocation.clear()
                self.ui.ErrorType.clear()
                self.ui.ErrorDescription.clear()
        self.ui.ID.setText("第  "+ str(self.DataID + 1)+"   条")  

    #点击末条
    def on_click_Last(self):
        #初始化DataID为NumOfData-1，将界面内容全部刷新并显示数据
        self.DataID = self.NumOfData - 1 
        self.ui.ErrorLocation.setPlainText(self.listErrorLocation[self.DataID])
        self.ui.ErrorType.setPlainText(self.listErrorType[self.DataID])
        self.ui.ErrorDescription.setPlainText(self.listErrorDescription[self.DataID])      
        self.ui.ID.setText("第  "+ str(self.DataID + 1)+"   条")

    #点击保存
    def on_click_Record(self):
        #获取文本框内容
        ErrorLocation=self.ui.ErrorLocation.toPlainText()
        ErrorType=self.ui.ErrorType.toPlainText()
        ErrorDescription=self.ui.ErrorDescription.toPlainText()
        #将数据写入到错误信息集中
        f=open(File_Name+"_错误信息集.txt",'a+',encoding='utf-8')
        f.write(str(self.DataID)+' '+ErrorLocation+' '+ErrorType+' '+ErrorDescription+'\n')
        f.close()
        #数据数加一
        self.NumOfData = self.NumOfData + 1
        #临时存储所有数据
        self.listErrorLocation.append(ErrorLocation)
        self.listErrorType.append(ErrorType)
        self.listErrorDescription.append(ErrorDescription)
        #给用户提示
        SaveBox=QMessageBox()
        SaveBox.about(None,'保存成功','数据保存成功')

    #点击取消
    def on_click_Cancel(self):
        #清空文本框内容
        self.ui.ErrorLocation.clear()
        self.ui.ErrorType.clear()
        self.ui.ErrorDescription.clear()
    
    #点击检索
    def on_click_Find(self):
        #获取文本框内容
        info=self.ui.textFind.toPlainText()
        #判定是否找到
        flag = 0
        for n in range(self.NumOfData):
            if info==self.listErrorDescription[n] or info==self.listErrorDescription[n] or info==self.listErrorDescription[n] :
                self.ui.ErrorLocation.setPlainText(self.listErrorLocation[n])
                self.ui.ErrorType.setPlainText(self.listErrorType[n])
                self.ui.ErrorDescription.setPlainText(self.listErrorDescription[n])      
                self.ui.ID.setText("第  "+ str(n + 1)+"   条")  
                flag =1
            if n==self.NumOfData-1 and  flag ==0:
                QMessageBox.warning(self,"Warning",'NONE')
        self.ui.textFind.clear()


    #读取已有数据文件
    def ReadDataFile(self,filepath):
        f=open(filepath,'r',encoding='utf-8')
        linelists=f.readlines() #读取所有数据
        f.close()
        num=0
        #变量数据分别存储的到listErrorLocation,listErrorType,listErrorDescription中
        for line in linelists: 
            id,a,b,c=line.split()
            self.listErrorLocation.append(a)
            self.listErrorType.append(b)
            self.listErrorDescription.append(c)
            num+=1
    #返回现有数据个数
        return num  




