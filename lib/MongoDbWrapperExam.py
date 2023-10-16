from calendar import day_abbr
from pymongo import MongoClient
from datetime import datetime

class MongoDbWrapperExam:
    def __init__(self, db_name="Online-Exam-System", collection_name="Exams"):
        self.client = MongoClient(
            "mongodb+srv://Reuben:Fire@systemcluster.hwra6cw.mongodb.net/"
        )
        self.db = self.client[db_name]
        self.exam_collection = self.db[collection_name]
        print("Connected to MongoDB" + db_name + " " + collection_name)
    
    def insert_exam(
            self, id_exam, exam_name, supervisor_Id
    ):

        new_document = {
            "id": id_exam,
            "examName": exam_name,
            "supervisorId": supervisor_Id,
            "has_started": False
        }
        insertion_result = self.exam_collection.insert_one(new_document)
        if insertion_result.inserted_id:
            return insertion_result.inserted_id
        else:
            return None


    def delete_exam(self, id_exam):
        query = {'id': id_exam}
        self.exam_collection.delete_one(query)

    def query_single_field(self, id_exam, field_to_return):
       query = {"id": id_exam}
       projection = self.exam_collection.find_one(
           query, {field_to_return: True, "_id": False}
           )
       if projection:
           return projection
       else:
           return None    

    def query_whole_document(self, id_exam):
        query = {'id': id_exam}
        found_documents = list(self.exam_collection.find(query))
        if found_documents:
            return found_documents
        else:
            return None

    def start_exam(self, id_exam):
        query = {'id': id_exam}
        self.exam_collection.update_one(query, {"$set": {'has_started': True}})
    
    def rest_exam(self, id_exam):
        query = {'id': id_exam}
        self.exam_collection.update_one(query, {"$set": {'has_started': False}})

    def flip_exam(self, id_exam):
        filter = {"id": id_exam}

        # Find the document
        document = self.exam_collection.find_one(filter)

        if document is not None:
            # Get the current value of the boolean field
            current_value = document.get("has_started", False)

            # Calculate the new value
            new_value = not current_value

            # Update the document with the new value
            update = {"$set": {"has_started": new_value}}
            self.exam_collection.update_one(filter, update)
        else:
            return None
