import logging
from os import getenv
from aiogram import Bot, Dispatcher, executor
import handler


logging.basicConfig(level=logging.INFO)
bot = Bot(token=getenv('API_TOKEN'), proxy=getenv('PROXY_URL'))
dp = Dispatcher(bot)


if __name__ == '__main__':
	executor.start_polling(handler.dp)
