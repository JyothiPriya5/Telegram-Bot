import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = pymongo.MongoClient(MONGO_URI)
db = client["telegram_bot"]  # Database Name
users_collection = db["users"]  # Collection for user data
chats_collection = db["chats"]  # Collection for storing chats
files_collection = db["files"]  # Collection for storing file metadata
