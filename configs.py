import os

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.environ.get('TOKEN')
CONNECTION_STRING = os.environ.get('DATABASE_URL')
