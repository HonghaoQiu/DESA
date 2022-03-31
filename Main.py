
import sys
import datetime
from unittest import result
from pymongo import MongoClient
from gridfs import *
import os
from  UI_Frame import Ui_dilizhijian


from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore




class MainWindow(QMainWindow):
    #连接Mongodb数据库
    client=MongoClient('localhost',27017)
    #取得对应的collection
    db=client.info
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
        #临时存储数据
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
        self.ui.extractData.clicked.connect(self.on_click_extractData)
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
        f = self.FilePath.split('/')
        File_Name=f[-1].split('.')
        gridFS = GridFS(self.db, collection="fs")
        datatmp = open(self.FilePath, 'rb')
        # 如果数据库中不存在该文件则存入数据库
        if gridFS.exists({'filename':f[-1]})==0:
            gridFS.put(datatmp,filename=f[-1])
            datatmp.close()

           




        #如果文档为txt类型，在文档类型中显示
        if File_Name[1]=='txt': 
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
        
        self.NumOfData=self.ReadDataFile(File_Name[0]+"_错误信息集")

        if self.NumOfData!=0:
            self.DataID=0
            self.ui.ID.setText("第  "+ str(self.DataID + 1)+"   条")
            self.ui.ErrorLocation.setPlainText(self.listErrorLocation[self.DataID])
            self.ui.ErrorType.setPlainText(self.listErrorType[self.DataID])
            self.ui.ErrorDescription.setPlainText(self.listErrorDescription[self.DataID])
    

    #鼠标点击事件重写
    def mousePressEvent(self, e):
        if e.buttons() == QtCore.Qt.LeftButton:
            self.flag = True
    
    #鼠标释放事件重写
    def mouseReleaseEvent(self, e):
        self.flag = False
        self.movex = ""
        self.movey = ""

    #实现拖动图片
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

    #实现缩放图片
    def wheelEvent(self, e):
        angle=e.angleDelta()  
        # 竖直滚过的距离                                     
        angleY=angle.y() 
        if angleY > 0:

            self.label_w*=1.05 
            self.label_h*=1.05                                                    
        elif angleY < 0:
            self.label_w/=1.05 
            self.label_h/=1.05  
        
        self.ui.label.setGeometry(QtCore.QRect(self.label_x, self.label_y, self.label_w, self.label_h))
        self.ui.label.setPixmap(QPixmap(self.FilePath).scaled(self.ui.label.width(),self.ui.label.height()))


    #点击提取
    def on_click_extractData(self):
        gridFS = GridFS(self.db, collection="fs")
        for grid_out in gridFS.find():
            data = grid_out.read() # 获取图片数据
            outf = open('Data\\'+grid_out.filename,'wb')#创建文件
            outf.write(data)  # 存储图片
            outf.close()

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
        currentTime=datetime.datetime.now()
        #获取文本框内容
        ErrorLocation=self.ui.ErrorLocation.toPlainText()
        ErrorType=self.ui.ErrorType.toPlainText()
        ErrorDescription=self.ui.ErrorDescription.toPlainText()
        #将数据写入到错误信息集中
        co=self.db[File_Name[0]+"_错误信息集"]
        errorinfo={
                    '_id':str(self.DataID),
                    'ErrorLocation':ErrorLocation,
                    'ErrorType':ErrorType,
                    'ErroDescription':ErrorDescription,
                    'User': self.username,
                    'Time': str(currentTime)
                    }
        condition = {'_id':str(self.DataID)} 
        if ErrorLocation=='' and ErrorType=='' and ErrorDescription =='':
            SaveBox=QMessageBox()
            SaveBox.about(None,'提示','未输入信息')
        else:
            if co.find_one(condition) :
                errorinfoNOW = co.find_one(condition)  
                errorinfoNOW = errorinfo  
                co.update_one(condition, {'$set': errorinfoNOW})  
                self.listErrorLocation[self.DataID]=ErrorLocation
                self.listErrorType[self.DataID]=ErrorType
                self.listErrorDescription[self.DataID]=ErrorDescription
            else :
                co.insert_one(errorinfo)
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
        res=self.db[filepath].find()
        num=0
        for i in res:
            num+=1
        print(num)
        #变量数据分别存储的到listErrorLocation,listErrorType,listErrorDescription中
        if num >0:
            m=self.db[filepath].find()
            for d in m: 
                self.listErrorLocation.append(d['ErrorLocation'])
                self.listErrorType.append(d['ErrorType'])
                self.listErrorDescription.append(d['ErroDescription'])
    #返回现有数据个数
        return num  


