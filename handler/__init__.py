import logging
import requests
import utils
from aiogram import types
from os import getenv
from dotenv import load_dotenv
from main import dp


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
	load_dotenv()
	show_public_ip = getenv("SHOW_PUBLIC_IP")
	appcode = getenv("ALICLOUD_APPCODE")
	content = '''
Hello!
I'm Ping Bot!
I can ping your server with ICMP or TCP protocols.

Usage:
/icmp <ip> - ICMP ping to IP
/tcp <ip> <port> - TCP ping to IP:PORT
/trace <ip> - Show the route to a server
/dns <host> [record_type] - Resolve a domain name
/whois <domain> - Get WHOIS information
/ip <ip> - Get IP information
'''
	if 'appcode' in locals():
		content += "/ip_alicloud <ip> - Get IP information using AlibabaCloud API\n"
	if show_public_ip:
		ip = requests.get("https://ipinfo.io/json").json()['ip']
		city = requests.get("https://ipinfo.io/json").json()['city']
		content += f"Running on {ip} in {city}\n"
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
		result = utils.icmp_ping(ip)
		if result:
			await waiting_message.edit_text(f"ICMP ping to `{ip}`:\n`{result}`", parse_mode="MarkdownV2", disable_web_page_preview=True)
		else:
			await waiting_message.edit_text(f"ICMP ping to `{ip}`:\nNo result", parse_mode="MarkdownV2", disable_web_page_preview=True)
	except Exception as e:
		await waiting_message.edit_text(f"ICMP ping to `{ip}`:\n`{e}`", parse_mode="MarkdownV2", disable_web_page_preview=True)


@dp.message_handler(commands=['tcp'])
async def tcp(message: types.Message):
	args = message.get_args().split()
	if len(args) < 2:
		await message.reply("You must specify IP address and port!")
		return
	ip = args[0]
	port = args[1]
	logging.info(f'{message.from_id} TCP ping {ip} {port}')
	waiting_message = await message.reply(f"TCP pinging to `{ip}:{port}` ...", parse_mode="Markdown", disable_web_page_preview=True)
	result = utils.tcp_ping(ip, port)
	await waiting_message.edit_text(f"TCP ping to `{ip}:{port}`:\n `{result}`", parse_mode="Markdown", disable_web_page_preview=True)


@dp.message_handler(commands=['trace'])
async def trace(message: types.Message):
	ip = message.get_args()
	logging.info(f'{message.from_id} trace {ip}')
	if not ip:
		await message.reply("You must specify IP address!")
		return
	waiting_message = await message.reply(f"Tracing to `{ip}` ...")
	try:
		result = utils.run_nexttrace(ip)
		await waiting_message.edit_text(f"Trace to `{ip}`:\n`{result}`", parse_mode="MarkdownV2", disable_web_page_preview=True)
	except Exception as e:
		await waiting_message.edit_text(f"Trace to `{ip}`:\n` {e}`", parse_mode="MarkdownV2", disable_web_page_preview=True)


@dp.message_handler(commands=['dns'])
async def dns(message: types.Message):
	args = message.get_args().split()
	if len(args) < 1:
		await message.reply("You must specify hostname!")
		return
	host = args[0]
	record_type = "A"
	if len(args) > 1:
		record_type = args[1]
	logging.info(f'{message.from_id} DNS lookup {host} as {record_type}')
	waiting_message = await message.reply(f"DNS lookup {host} as {record_type} ...")
	try:
		result = utils.dns_lookup(host, record_type)
		await waiting_message.edit_text(f"`DNS lookup {host} as {record_type}:\n{result}`", parse_mode="MarkdownV2", disable_web_page_preview=True)
	except Exception as e:
		await waiting_message.edit_text(f"`DNS lookup {host} as {record_type} failed:\n{e}`", parse_mode="MarkdownV2", disable_web_page_preview=True)


@dp.message_handler(commands=['whois'])
async def whois(message: types.Message):
	domain = message.get_args()
	if not domain:
		await message.reply("You must specify domain!")
		return
	logging.info(f'{message.from_id} whois {domain}')
	waiting_message = await message.reply(f"Checking WHOIS information for {domain} ...")
	try:
		result = utils.whois(domain)
		await waiting_message.edit_text(f"`{result}`", parse_mode="MarkdownV2", disable_web_page_preview=True)
	except Exception as e:
		await waiting_message.edit_text(f"Checking `{domain}` failed:\n`{e}`", parse_mode="MarkdownV2", disable_web_page_preview=True)


@dp.message_handler(commands=['ip'])
async def ip(message: types.Message):
	ip = message.get_args()
	if not ip:
		await message.reply("You must specify IP address!")
		return
	logging.info(f'{message.from_id} ip {ip}')
	waiting_message = await message.reply(f"Checking IP information for {ip} ...")
	try:
		result = utils.ip_info(ip)
		await waiting_message.edit_text(f"{result}", parse_mode="MarkdownV2", disable_web_page_preview=True)
	except Exception as e:
		await waiting_message.edit_text(f"Checking {ip} failed:\n{e}")


@dp.message_handler(commands=['ip_alicloud'])
async def ip_alicloud(message: types.Message):
	appcode = getenv('ALICLOUD_APPCODE')
	ip = message.get_args()
	if not ip:
		await message.reply("You must specify IP address!")
		return
	logging.info(f'{message.from_id} ip_alicloud {ip}')
	waiting_message = await message.reply(f"Checking IP information for {ip} ...")
	try:
		result = utils.ip_info_alicloud(ip, appcode)
		await waiting_message.edit_text(f"{result}", parse_mode="MarkdownV2", disable_web_page_preview=True)
	except Exception as e:
		await waiting_message.edit_text(f"Checking {ip} failed:\n{e}")
