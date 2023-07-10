import logging
import requests
from aiogram import types
from os import getenv
from dotenv import load_dotenv
from main import dp
from utils import icmp_ping, tcp_ping, run_nexttrace, dns_lookup


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	load_dotenv()
	SHOW_PUBLIC_IP = getenv("SHOW_PUBLIC_IP")
	content = '''
Hello!
I'm Ping Bot!
I can ping your server with ICMP or TCP protocols.

Usage:
/icmp <ip> - ICMP ping to IP
/tcp <ip> <port> - TCP ping to IP:PORT
/trace <ip> - Show the route to a server
/dns <host> [record_type] - Resolve a domain name
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
	logging.info(f'{message.from_id} ICMP ping {ip}')
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
	logging.info(f'{message.from_id} TCP ping {ip} {port}')
	waiting_message = await message.reply(f"TCP pinging to {ip}:{port} ...")
	result = tcp_ping(ip, port)
	await waiting_message.edit_text(f"TCP ping to {ip}:{port}:\n {result}")


@dp.message_handler(commands=['trace'])
async def trace(message: types.Message):
	ip = message.get_args()
	logging.info(f'{message.from_id} trace {ip}')
	if not ip:
		await message.reply("You must specify IP address!")
		return
	waiting_message = await message.reply(f"Tracing to {ip} ...")
	try:
		result = run_nexttrace(ip)
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
	record_type = 'A'
	if len(args) > 1:
		record_type = args[1]
	logging.info(f'{message.from_id} DNS lookup {host} as {record_type}')
	waiting_message = await message.reply(f"DNS lookup {host} as {record_type} ...")
	try:
		result = dns_lookup(host, record_type)
		await waiting_message.edit_text(f"DNS lookup {host} as {record_type}:\n{result}")
	except Exception as e:
		await waiting_message.edit_text(f"DNS lookup {host} as {record_type} failed:\n{e}")
