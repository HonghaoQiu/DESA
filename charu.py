 

from pymongo import MongoClient
from gridfs import *
import os
#链接mongodb
client=MongoClient('localhost',27017)
#取得对应的collection
filename="PIC"
db=client.info
co=db[filename]
errorinfo={
    '_id':'1',
    'ErrorLocation':'22',
    'ErrorType':'d',
    'ErroDescreption':'gfdg'
}
#result=co.insert_one(errorinfo)
condition = {'_id': '2'}  
if co.find_one(condition) :
  errorinfo = co.find_one(condition)  
  errorinfo['ErroDescreption'] = ' sdgdfsgdf'  
  co.update_one(condition, {'$set': errorinfo})  






