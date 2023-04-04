from pymongo import MongoClient

from configs import CONNECTION_STRING

client = MongoClient(CONNECTION_STRING)
