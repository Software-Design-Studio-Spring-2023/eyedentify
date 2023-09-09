from pymongo import MongoClient

client = MongoClient("mongodb+srv://Reuben:Fire@systemcluster.hwra6cw.mongodb.net/")
db = client["Online-Exam-System"]
userCollection = db["Users"]

class MongoDbWrapper:
    def insert_user(id, name,loggedIn, userType, email, password, image, encodeIp):
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
    
    def delete_one(key, value):
        query = {key: value}
        userCollection.delete_one(query)
    
    # Reutrns the whple doucment can use any key vale pair so can return muliple users
    def query_whole_document(key, value):
        query = {key: value}
        found_documents = list(userCollection.find(query))

        if found_documents:
            return found_documents
        else:
            return None
    
    def query_single_field(id_value, field_to_return):
        query = {"id": id_value}
        projection = userCollection.find_one(query, {field_to_return: True, "_id": False})
        return projection
    
    def logged_in(id_value):
        query = {"id": id_value}
        userCollection.update_one(query, {'$set': {'loggedIn': True}})
    
    def logged_out(id_value):
        query = {"id": id_value}
        userCollection.update_one(query, {'$set': {'loggedIn': False}})

  


client.close