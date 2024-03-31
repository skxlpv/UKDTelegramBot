from pymongo import MongoClient

from configs import MONGO_PORT, MONGO_PASS, MONGO_USER, CONTAINER_NAME, MONGO_HOST, DEBUG

client = MongoClient(host=MONGO_HOST if DEBUG else CONTAINER_NAME,
                     port=int(MONGO_PORT),
                     username=MONGO_USER,
                     password=MONGO_PASS,
                     authSource="admin")
db = client['user']

db['schedule_picked'].create_index('user_id', unique=True)
db['user_preferences'].create_index('user_id', unique=True)
