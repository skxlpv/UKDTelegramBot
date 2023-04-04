import logging

from pymongo import MongoClient

from configs import CONNECTION_STRING, MONGO_HOST, MONGO_PORT, MONGO_PASS, MONGO_USER, MONGO_DB


client = MongoClient(CONNECTION_STRING)

