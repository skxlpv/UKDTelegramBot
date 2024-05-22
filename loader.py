import logging
import os
from logging.handlers import RotatingFileHandler

from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import Dispatcher

from bot.worker.scheduler import scheduler
from configs import API_TOKEN

os.environ['TZ'] = 'Europe/Kiev'

# Configure logging
logger = logging.getLogger('BOT_LOG')
logger.setLevel(logging.INFO)


class MyRotatingFileHandler(RotatingFileHandler):
    def doRollover(self):

        with open(self.baseFilename, 'r') as f:
            lines = f.readlines()
            last_lines = lines[-10:]

        super().doRollover()

        with open(self.baseFilename, 'w') as f:
            f.writelines(last_lines)


file_handler = MyRotatingFileHandler('bot/storage/logs/bot_log.log',
                                     maxBytes=15*1024*1024, backupCount=2)

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
