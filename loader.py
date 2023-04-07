import logging

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from bot.worker.scheduler import scheduler
from configs import API_TOKEN

# Configure logging
logger = logging.getLogger('UKD_bot')
logger.setLevel(logging.WARNING)

file_handler = logging.FileHandler('UKD_bot.log')
file_handler.setLevel(logging.WARNING)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.WARNING)

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
