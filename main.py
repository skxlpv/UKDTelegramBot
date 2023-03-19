import logging, os

from aiogram import Bot, Dispatcher, executor

from dotenv import load_dotenv
load_dotenv()

API_TOKEN = os.environ.get('TOKEN')

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)