from calendar import day_abbr
from pymongo import MongoClient
import datetime

class MongoDbWrapperExam:
    def __init__(self, db_name="Online-Exam-System", collection_name="Exams"):
        self.client = MongoClient(
            "mongodb+srv://Reuben:Fire@systemcluster.hwra6cw.mongodb.net/"
        )
        self.db = self.client[db_name]
        self.exam_collection = self.db[collection_name]
        print("Connected to MongoDB" + db_name + " " + collection_name)
    
    def insert_exam(
            self, id_exam, exam_name, supervisor_Id, year, month, day, start_hour, start_min, end_hour, end_min
    ):
        
        start_date_time = datetime.datetime(year, month, day, start_hour, start_min, 0, 0)
        end_date_time = datetime.datetime(year, month, day, end_hour, end_min, 0, 0)

        new_document = {
            "id": id_exam,
            "examName": exam_name,
            "supervisorId": supervisor_Id,
            "start_time": start_date_time,
            "end_time": end_date_time,
            "students": [],
            "seat": []
        }
        insertion_result = self.exam_collection.insert_one(new_document)
        if insertion_result.inserted_id:
            return insertion_result.inserted_id
        else:
            return None
        

    def insert_student_exam(self, id_exam, student_id):
        self.exam_collection.update_one({'id': id_exam}, {'$push': {"students": student_id}})
        self.exam_collection.update_one({'id': id_exam}, {'$push': {"seat": student_id}})

    def delete_exam(self, id_exam):
        query = {'id': id_exam}
        self.exam_collection.delete_one(query)

    def query_single_field(self, id_exam, field_to_return):
       query = {"id": id_exam}
       projection = self.exam_collection.find_one(
           query, {field_to_return: True, "_id": False}
           )
       return projection

    def query_whole_document(self, id_exam):
        query = {'id': id_exam}
        found_documents = list(self.exam_collection.find(query))
        if found_documents:
            return found_documents
        else:
            return None
        