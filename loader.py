import logging
import re
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from bot.worker.scheduler import scheduler
from configs import API_TOKEN

# Configure logging
logger = logging.getLogger('BOT_LOG')
logger.setLevel(logging.INFO)

file_handler = TimedRotatingFileHandler('bot/storage/logs/bot_log.log', when='w0', backupCount=100)
file_handler.suffix = '%Y_%m_%d'
file_handler.namer = lambda name: name.replace('.log', '') + '.log'

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
