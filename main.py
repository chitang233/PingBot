import logging
import tcping
import subprocess
import aiogram.utils.markdown
from aiogram import Bot, Dispatcher, executor, types
import ping3

API_TOKEN = ''
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def icmp_ping(ip):
	response = ping3.ping(ip) * 1000
	return response


def tcp_ping(ip, port):
	# result = tcping.Ping(ip, port, 4).ping(4).result.table
	process = subprocess.Popen(f"tcping {ip} -p {port} -c 4 --report", shell=True, stdout=subprocess.PIPE)
	process.wait()
	result = '\n'.join(str(process.stdout.read()).split('\\n')[-6:-1])
	return result


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	await message.reply("Hello!\nI'm Ping Bot!\nI can ping your server with ICMP or TCP protocols.\n\n"
											"Usage:\n"
											"/icmp <ip> - ICMP ping to IP\n"
											"/tcp <ip> <port> - TCP ping to IP:PORT")


@dp.message_handler(commands=['icmp'])
async def icmp(message: types.Message):
	try:
		ip = message.get_args()
		if not ip:
			await message.reply("You must specify IP address!")
			return
		response = icmp_ping(ip)
		if response:
			await message.reply(f"ICMP ping to {ip}:\n{response}")
		else:
			await message.reply(f"ICMP ping to {ip}:\nNo response")
	except Exception as e:
		await message.reply(f"ICMP ping to {ip}:\n{e}")


@dp.message_handler(commands=['tcp'])
async def tcp(message: types.Message):
	try:
		args = message.get_args().split()
		if len(args) < 2:
			await message.reply("You must specify IP address and port!")
			return
		ip = args[0]
		port = args[1]
		response = aiogram.utils.markdown.escape_md(".") + aiogram.utils.markdown.escape_md(tcp_ping(ip, port))
		await message.reply(f"TCP ping to {ip}:{port}:\n{response}", parse_mode='MarkdownV2')
	except Exception as e:
		await message.reply(f"TCP ping to {ip}:{port}:\n{e}")


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
