from pymongo import MongoClient


class MongoDbWrapper:
    def __init__(self, db_name="Online-Exam-System", collection_name="Users"):
        self.client = MongoClient(
            "mongodb+srv://Reuben:Fire@systemcluster.hwra6cw.mongodb.net/"
        )
        self.db = self.client[db_name]
        self.user_collection = self.db[collection_name]
        print("Connected to MongoDB" + db_name + " " + collection_name)

    def insert_user(
        self, id, name, loggedIn, userType, email, password, image, encodeIp
    ):
        new_document = {
            "id": id,
            "name": name,
            "loggedIn": loggedIn,
            "userType": userType,
            "email": email,
            "password": password,
            "imageURL": image,
            "encodeIP": encodeIp,
        }
        insertion_result = self.userCollection.insert_one(new_document)
        if insertion_result.inserted_id:
            return insertion_result.inserted_id
        else:
            return None

    def delete_one(self, key, value):
        query = {key: value}
        self.userCollection.delete_one(query)

    # Reutrns the whple doucment can use any key vale pair so can return muliple users
    def query_whole_document(self, key, value):
        query = {key: value}
        found_documents = list(self.userCollection.find(query))

        if found_documents:
            return found_documents
        else:
            return None

    def query_single_field(self, id_value, field_to_return):
        query = {"id": id_value}
        projection = self.userCollection.find_one(
            query, {field_to_return: True, "_id": False}
        )
        return projection

    def logged_in(self, id_value):
        query = {"id": id_value}
        self.userCollection.update_one(query, {"$set": {"loggedIn": True}})

    def logged_out(self, id_value):
        query = {"id": id_value}
        self.userCollection.update_one(query, {"$set": {"loggedIn": False}})

    def all_users(self):
        all_users = self.user_collection.find({})
        all_users = list(all_users)
        for user in all_users:
            user["_id"] = str(user["_id"])
        return all_users

    def close_connection(self):
        self.client.close()
