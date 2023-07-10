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
		result = response.json()['whois']['whois']
		lines = result.splitlines()
		filtered_result = [line for line in lines if
											 'REDACTED FOR PRIVACY' not in line and 'Please query the' not in line]
		return "\n".join(filtered_result).split(
			"For more information on Whois status codes, please visit https://icann.org/epp")[0]
	else:
		return None


def ip_info(ip):
	result = f'Target: `{ip}`\n'
	ipinfo_response = requests.get('https://ipinfo.io/{}/json'.format(ip))
	ipapi_response = requests.get("http://ip-api.com/json/{}".format(ip))
	if ipinfo_response.status_code != 200 or ipapi_response.status_code != 200:
		return None
	region = f'{ipinfo_response.json()["city"]} \- {ipinfo_response.json()["region"]} \- {ipinfo_response.json()["country"]}'
	asn = ipinfo_response.json()["org"].split(" ")[0]
	if 'hostname' in ipinfo_response.json():
		hostname = ipinfo_response.json()["hostname"]
	if 'anycast' in ipinfo_response.json():
		anycast = 'This is an anycast IP address'
	isp = ipapi_response.json()["isp"]
	org = ipapi_response.json()["org"]
	result += f'Region: `{region}`\n'
	result += f'ASN: `{asn}`\n'
	if 'hostname' in locals():
		result += f'Hostname: `{hostname}`\n'
	result += f'ISP: `{isp}`\n'
	result += f'Org: `{org}`\n'
	if 'anycast' in locals():
		result += f'Anycast: {anycast}\n'
	return result
