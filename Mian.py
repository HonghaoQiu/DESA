import sys
import os
import Ui_dilizhijian


from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog,QMessageBox
from PyQt5.QtGui import QPixmap





class MainWindow(QMainWindow):
    #索引
    DataID = 0
    #数据数量
    NumOfData = 0
    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui =Ui_dilizhijian.Ui_MainWindow()
        # 初始化界面
        self.ui.setupUi(self)
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
        FilePath, _  =QFileDialog.getOpenFileName(None,"选择打开文件")
        #显示文件路径显示
        self.ui.FilePath.setText(FilePath)
        #File_Name为全局变量
        global File_Name
        #获取文件名字以及文件类型
        File_Name,file_extension=os.path.splitext(FilePath)
        #如果文档为txt类型，在文档类型中显示
        if file_extension=='.txt': 
           f=open(FilePath,'r',encoding='utf-8')
           content=f.readlines()
           for line in content:
              self.ui.textShow.append(line)
        #若为其它类型则读为图片，此处仅为栅格数据
        else:
            self.ui.label.setPixmap(QPixmap(FilePath).scaled(self.ui.label.width(),self.ui.label.height()))
        
        #判断错位信息集是否已经存在，若存在存入临时list中便与操作，特别注意文件名且文件与打开文件位于同一路径下
        if os.path.exists(File_Name+"_错误信息集.txt") == True:
            self.NumOfData=ReadDataFile(File_Name+"_错误信息集.txt")
            self.DataID=0
            self.ui.ID.setText("第  "+ str(self.DataID + 1)+"   条")
            self.ui.ErrorLocation.setPlainText(listErrorLocation[self.DataID])
            self.ui.ErrorType.setPlainText(listErrorType[self.DataID])
            self.ui.ErrorDescription.setPlainText(listErrorDescription[self.DataID])
    #点击首条
    def on_click_First(self):
        #初始化DataID为0，将界面内容全部刷新并显示数据
        self.DataID=0
        self.ui.ID.setText("第  "+ str(self.DataID + 1)+"   条")
        self.ui.ErrorLocation.setPlainText(listErrorLocation[self.DataID])
        self.ui.ErrorType.setPlainText(listErrorType[self.DataID])
        self.ui.ErrorDescription.setPlainText(listErrorDescription[self.DataID])
    
    #点击上一条
    def on_click_Previous(self):
        #判断是否为首条
        if self.DataID==0:
            msg_box = QMessageBox(QMessageBox.Warning, '警告', '已是首条')
            msg_box.exec_()
        else:    
            self.DataID=self.DataID-1   
            self.ui.ErrorLocation.setPlainText(listErrorLocation[self.DataID])
            self.ui.ErrorType.setPlainText(listErrorType[self.DataID])
            self.ui.ErrorDescription.setPlainText(listErrorDescription[self.DataID])      
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
            if (len(listErrorLocation) - 1) >= self.DataID:
              self.ui.ErrorLocation.setPlainText(listErrorLocation[self.DataID])
              self.ui.ErrorType.setPlainText(listErrorType[self.DataID])
              self.ui.ErrorDescription.setPlainText(listErrorDescription[self.DataID])     
            else: 
              self.ui.ErrorLocation.clear()
              self.ui.ErrorType.clear()
              self.ui.ErrorDescription.clear()
        self.ui.ID.setText("第  "+ str(self.DataID + 1)+"   条")  

    #点击末条
    def on_click_Last(self):
        #初始化DataID为NumOfData-1，将界面内容全部刷新并显示数据
        self.DataID = self.NumOfData - 1 
        self.ui.ErrorLocation.setPlainText(listErrorLocation[self.DataID])
        self.ui.ErrorType.setPlainText(listErrorType[self.DataID])
        self.ui.ErrorDescription.setPlainText(listErrorDescription[self.DataID])      
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
        listErrorLocation.append(ErrorLocation)
        listErrorType.append(ErrorType)
        listErrorDescription.append(ErrorDescription)
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
            if info==listErrorDescription[n] or info==listErrorDescription[n] or info==listErrorDescription[n] :
               self.ui.ErrorLocation.setPlainText(listErrorLocation[n])
               self.ui.ErrorType.setPlainText(listErrorType[n])
               self.ui.ErrorDescription.setPlainText(listErrorDescription[n])      
               self.ui.ID.setText("第  "+ str(n + 1)+"   条")  
               flag =1
            if n==self.NumOfData-1 and  flag ==0:
               QMessageBox.warning(self,"Warning",'NONE')
        self.ui.textFind.clear()


#读取已有数据文件
def ReadDataFile(filepath):
    f=open(filepath,'r',encoding='utf-8')
    linelists=f.readlines() #读取所有数据
    f.close()
    num=0
    #变量数据分别存储的到listErrorLocation,listErrorType,listErrorDescription中
    for line in linelists: 
        id,a,b,c=line.split()
        listErrorLocation.append(a)
        listErrorType.append(b)
        listErrorDescription.append(c)
        num+=1
    #返回现有数据个数
    return num  


if __name__=='__main__':
  #作临时存储方便后续操作  
  listErrorLocation=[]
  listErrorType=[]
  listErrorDescription=[]

  app = QApplication(sys.argv)
  mainWindow = MainWindow()
  mainWindow.show()
  sys.exit(app.exec_())
  
      

