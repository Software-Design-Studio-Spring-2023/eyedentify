from pymongo import MongoClient
class MongoDbWrapper:
    def insert_user(id, name,loggedIn, userType, email, password, image, encodeIp):
        client = MongoClient("mongodb+srv://Reuben:Fire@systemcluster.hwra6cw.mongodb.net/")
        db = client["Online-Exam-System"]
        userCollection = db["Users"]
        new_document = {
            "id": id,
            "name": name,
            "loggedIn": loggedIn,
            "userType": userType,
            "email": email,
            "password": password,
            "imageURL": image,
            "encodeIP": encodeIp
        }
        insertion_result = userCollection.insert_one(new_document)
        if insertion_result.inserted_id:
            return insertion_result.inserted_id
        else:
            return None
        client.close
    
    # Reutrns the whple doucment
    def query_whole_document(key, value):
        client = MongoClient("mongodb+srv://Reuben:Fire@systemcluster.hwra6cw.mongodb.net/")
        db = client["Online-Exam-System"]
        userCollection = db["Users"]
        query = {key: value}
        found_documents = list(userCollection.find(query))

        if found_documents:
            return found_documents
        else:
            return None
        client.close

    # insert_user(12, "Frank", "Frank@student", "Student")