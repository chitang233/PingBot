import logging
from aiogram import Bot, Dispatcher, executor
import handler
from config import API_TOKEN, PROXY_URL

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)

if __name__ == '__main__':
	executor.start_polling(handler.dp)
