import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ.get('TOKEN')
MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')
MONGO_DB = os.environ.get('MONGO_DB')
MONGO_HOST = os.environ.get('MONGO_HOST')
MONGO_PORT = os.environ.get('MONGO_PORT')
CONNECTION_STRING = os.environ.get('DATABASE_URL')
CONTAINER_NAME = os.environ.get('CONTAINER_NAME')
DEBUG = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
