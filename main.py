import logging
import subprocess
import requests
from aiogram.utils import markdown as md
from aiogram import Bot, Dispatcher, executor, types

from config import API_TOKEN, PROXY_URL, SHOW_PUBLIC_IP
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, proxy=PROXY_URL)
dp = Dispatcher(bot)


def icmp_ping(ip):
	process = subprocess.Popen(f"ping {ip} -c 4", shell=True, stdout=subprocess.PIPE)
	process.wait()
	result = ''
	for line in process.stdout.read().decode().split('\n'):
		if not ('PING' in line or '---' in line):
			result += line + '\n'
	return result.strip()


def tcp_ping(ip, port):
	process = subprocess.Popen(f"tcping {ip} -p {port} -c 4 --report", shell=True, stdout=subprocess.PIPE)
	process.wait()
	result_arr = process.stdout.read().decode().split('\n')
	keys = result_arr[-5].strip('|').split('|')
	values = result_arr[-3].strip('|').split('|')
	result = ''
	for subscript in range(2, 8):
		result += md.escape_md(keys[subscript].strip()) + ": " + md.code(values[subscript].strip()) + '\n'
	return result.strip()


def run_besttrace(ip):
	process = subprocess.Popen(f"./lib/besttrace -g cn -q1 {ip}", shell=True, stdout=subprocess.PIPE)
	process.wait()
	result = ''
	for line in process.stdout.read().decode().split('\n'):
		if not ('*' in line or 'BestTrace' in line):
			result += line + '\n'
	return result.strip()


def dns_lookup(host, type):
	process = subprocess.Popen(f"nslookup -type={type} {host}", shell=True, stdout=subprocess.PIPE)
	process.wait()
	result = ''
	for line in process.stdout.read().decode().split('\n'):
		if not (';' in line):
			result += line + '\n'
	return result.strip()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	content = '''
Hello!
I'm Ping Bot!
I can ping your server with ICMP or TCP protocols.

Usage:
/icmp <ip> - ICMP ping to IP
/tcp <ip> <port> - TCP ping to IP:PORT
'''
	if SHOW_PUBLIC_IP:
		ip = requests.get("https://ipinfo.io/json").json()['ip']
		city = requests.get("https://ipinfo.io/json").json()['city']
		await message.reply(f"{content}\nRunning on {ip} in {city}".strip())
	else:
		await message.reply(content.strip())


@dp.message_handler(commands=['icmp'])
async def icmp(message: types.Message):
	ip = message.get_args()
	logging.info(f'ICMP ping {ip}')
	if not ip:
		await message.reply("You must specify IP address!")
		return
	waiting_message = await message.reply(f"ICMP pinging to {ip} ...")
	try:
		result = icmp_ping(ip)
		if result:
			await waiting_message.edit_text(f"ICMP ping to {ip}:\n{result}")
		else:
			await waiting_message.edit_text(f"ICMP ping to {ip}:\nNo result")
	except Exception as e:
		await waiting_message.edit_text(f"ICMP ping to {ip}:\n{e}")


@dp.message_handler(commands=['tcp'])
async def tcp(message: types.Message):
	args = message.get_args().split()
	if len(args) < 2:
		await message.reply("You must specify IP address and port!")
		return
	ip = args[0]
	port = args[1]
	logging.info(f'TCP ping {ip} {port}')
	waiting_message = await message.reply(f"TCP pinging to {ip}:{port} ...")
	try:
		result = tcp_ping(ip, port)
		await waiting_message.edit_text(md.escape_md(f"TCP ping to {ip}:{port}:\n") + result, parse_mode='MarkdownV2')
	except Exception as e:
		await waiting_message.edit_text(f"TCP ping to {ip}:{port}:\n{e}")


@dp.message_handler(commands=['trace'])
async def trace(message: types.Message):
	ip = message.get_args()
	logging.info(f'Trace {ip}')
	if not ip:
		await message.reply("You must specify IP address!")
		return
	waiting_message = await message.reply(f"Tracing to {ip} ...")
	try:
		result = run_besttrace(ip)
		await waiting_message.edit_text(f"Trace to {ip}:\n{result}")
	except Exception as e:
		await waiting_message.edit_text(f"Trace to {ip}:\n{e}")


@dp.message_handler(commands=['dns'])
async def dns(message: types.Message):
	args = message.get_args().split()
	if len(args) < 1:
		await message.reply("You must specify hostname!")
		return
	host = args[0]
	type = 'A'
	if len(args) > 1:
		type = args[1]
	logging.info(f'DNS lookup {host} as {type}')
	waiting_message = await message.reply(f"DNS lookup {host} as {type} ...")
	try:
		result = dns_lookup(host, type)
		await waiting_message.edit_text(f"DNS lookup {host} as {type}:\n{result}")
	except Exception as e:
		await waiting_message.edit_text(f"DNS lookup {host} as {type} failed:\n{e}")


if __name__ == '__main__':
	executor.start_polling(dp)
