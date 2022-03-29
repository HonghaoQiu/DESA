 

from pymongo import MongoClient
from gridfs import *
import os
#链接mongodb
client=MongoClient('localhost',27017)
#取得对应的collection
collectionName="UserInfo"
db=client.Users
co=db[collectionName]
userinfo={
    '_id':'0',
    'UserName':'test',
    'PassWord':'test',
}
#result=co.insert_one(userinfo)

condition = {'UserName':'test',
             'PassWord':'test',}  
if co.find_one(condition) :
  print(1)






