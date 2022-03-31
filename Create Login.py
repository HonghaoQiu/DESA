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
    'UserName':'test',
    'PassWord':'test',
}
#result=co.insert_one(userinfo)


if co.find_one(userinfo) :
  i=0
else :
  result=co.insert_one(userinfo)



      





