 
from pymongo import MongoClient
from gridfs import *
import os
#链接mongodb
client=MongoClient('localhost',27017)
#取得对应的collection
db=client.info
#本地硬盘上的图片目录
dirs = 'E:\PHOTO\Cycle'
#列出目录下的所有图片
files = os.listdir(dirs)
#遍历图片目录集合
for file in files:
    #图片的全路径
    filesname = dirs + '\\' + file
    #分割，为了存储图片文件的格式和名称
    f = file.split('.')
    #类似于创建文件
    datatmp = open(filesname, 'rb')
    #创建写入流
    imgput = GridFS(db)
    #将数据写入，文件类型和名称通过前面的分割得到
    insertimg=imgput.put(datatmp,content_type=f[1],filename=f[0])
    datatmp.close()
print("js")

# gridFS = GridFS(db, collection="fs")
# count=0
# for grid_out in gridFS.find():
#     count+=1
#     print(count)
#     data = grid_out.read() # 获取图片数据
#     outf = open(str(count)+'.jpg','wb')#创建文件
#     outf.write(data)  # 存储图片
#     outf.close()


