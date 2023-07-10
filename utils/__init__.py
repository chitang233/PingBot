from shlex import quote
import subprocess
import requests


def icmp_ping(ip):
	command = "ping {} -c 4".format(quote(ip))
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	result = ''
	for line in process.stdout.read().decode().split('\n'):
		if not ('PING' in line or '---' in line):
			result += line + '\n'
	return result.strip()


def tcp_ping(ip, port):
	command = "tcping {} -p {} -c 4".format(quote(ip), quote(port))
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	return process.stdout.read().decode()


def dns_lookup(host, record_type):
	command = "nslookup -type={} {}".format(quote(record_type), quote(host))
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	result = ''
	for line in process.stdout.read().decode().split('\n'):
		if not (';' in line):
			result += line + '\n'
	return result.strip()


def run_nexttrace(ip):
	command = "./lib/nexttrace -g cn -q 1 -c {}".format(quote(ip))
	process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	process.wait()
	result = ''
	for line in process.stdout.read().decode().split('\n'):
		if not ('*' in line or 'BestTrace' in line):
			result += line + '\n'
	return result.strip()


def whois(domain):
	response = requests.get('https://namebeta.com/api/search/check?query={}'.format(domain))
	if response.status_code == 200:
		return response.json()['whois']['whois']
	else:
		return None


def ip_info(ip):
	response = requests.get('https://ipinfo.io/{}/json'.format(ip))
	if response.status_code == 200:
		result = f'Target: {ip}'
		result += f'Region: {response.json()["city"]} - {response.json()["region"]} - {response.json()["country"]}'
		result += f'Organization: {response.json()["org"]}'
		if ['hostname'] in response.json():
			result += f'Hostname: {response.json()["hostname"]}'
		if ['anycast'] in response.json():
			result += f'This is an anycast IP address'

	else:
		return None
