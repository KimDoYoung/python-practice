import asyncio
from datetime import datetime
from beanie import Document
import beanie
import beanie.exceptions
from bson import ObjectId
import motor
from pydantic import Field


print("beanie test code 1")
'''
class Task:
    content : text 
    is_complete : bool -> False
    created_at : datetime = datetime.now()
'''

class Task(Document):
    content : str = Field(max_length=100)
    is_complete :bool =  Field(default=False)
    created_at : datetime = Field(default=datetime.now())
    
    def to_json(self):
        return {
            "id": str(self.id),
            "revision_id": str(self.revision_id),
            "content": self.content,
            "is_complete": self.is_complete,
            "created_at": self.created_at
        }
class User(Document):
    user_id : str = Field(max_length=100),
    user_name : str = Field(max_length=100),
    password : str = Field(max_length=100),
    email : str = Field(max_length=100)
    created_at : datetime = Field(default=datetime.now())
    
    def to_json(self):
        return {
            "id": str(self.id),
            "revision_id": str(self.revision_id),
            "content": self.content,
            "is_complete": self.is_complete,
            "created_at": self.created_at
        }


async def main():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")
    await beanie.init_beanie(database=client.beaniedb, document_models=[Task, User])

    task1 = Task(content="Buy Milk")
    task2 = Task(content="Learn Mongodb")
    task3 = Task(content="Eat good food", is_complete=True)
    
    # await task1.insert()
    # await task2.insert()
    # await task3.insert()

    
    found_task = await Task.find_one({"_id": ObjectId("66317261588b3afe3f378bfc")})
    try:
        found_task.content = "Buy Milk and Bread"
        await found_task.replace()
    except (ValueError, beanie.exceptions.DocumentNotFound) :
        print("Task not found")

    tasks = await Task.all().to_list()
    for task in tasks:
        print(task.to_json())


asyncio.run(main())