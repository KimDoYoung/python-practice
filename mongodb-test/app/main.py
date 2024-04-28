from bson import SON, ObjectId
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['stock']
people = db['people']

people.insert_one({'name': 'John', 'age': 25, 'city': 'New York'})  
inserted_id = people.insert_one({'name': 'Hong', 'age': 23, 'city': 'Seoul', "interests" :['C++','Python','Piano']}).inserted_id
print(inserted_id)
print("------------------------------")
list = people.find()
for item in list:
    print(item)
print("------------------------------")

print([ p for p in people.find( { '_id': ObjectId('662de596535c5c9509ddcf3b')})])
print("------------------------------")
print("John count : " , people.count_documents({"name" : "John"}))
people.update_one({'name': 'John'}, {'$set': {'age': 26}})
people.delete_one({'name': 'Hong'})
list = people.find()
for item in list:
    print(item)

pipeline = [
    {
        "$group": {
            "_id": "$city",
            "avgAge": {"$avg": "$age"}  
        }
    },
    {
        "$sort": SON([ ("avgAge", -1),("_id", -1) ])
    }
]   
result = people.aggregate(pipeline)
print("------------------------------")
for item in result:
    print(item) 