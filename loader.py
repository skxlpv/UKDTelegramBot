from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from bot.worker.scheduler import scheduler
from configs import API_TOKEN

import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logger = logging.getLogger('BOT_LOG')
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler('bot/storage/logs/bot_log', maxBytes=1024*1024, backupCount=100)
file_handler.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')

file_handler.setFormatter(log_formatter)
stream_handler.setFormatter(log_formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Initialize bot and dispatcher
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# Starts the Scheduled jobs
scheduler.start()
