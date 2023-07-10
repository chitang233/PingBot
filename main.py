import logging
from os import getenv
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor
import handler


load_dotenv()
API_TOKEN = getenv('API_TOKEN')
PROXY_URL = getenv('PROXY_URL')


logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)


if __name__ == '__main__':
	executor.start_polling(handler.dp)
