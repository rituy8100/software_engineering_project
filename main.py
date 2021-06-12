import pymongo
from pymongo import MongoClient
import urllib.parse

cluster=MongoClient(f"mongodb+srv://rituy8100:wkrwjs@cluster0.qmr2a.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db=cluster["testdb"]
collection=db["testdb"]

post={"_id":0,"name":"jung","score":90}

collection.insert_one(post)