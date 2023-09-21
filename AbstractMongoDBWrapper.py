from pymongo import MongoClient
from abc import ABC, abstractclassmethod


class MongoDbWrapper(ABC):
    def __init__(self, db_name, collection_name):
        self.client = MongoClient(
            "mongodb+srv://Reuben:Fire@systemcluster.hwra6cw.mongodb.net/"
        )
        self.db = self.client[db_name]
        self.user_collection = self.db[collection_name]
        print("Connected to MongoDB" + db_name + " " + collection_name)

class Users(MongoDbWrapper):
    


# user = Users("Online-Exam-System", "Users")