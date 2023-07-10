from shlex import quote
import subprocess
import requests
from ipaddress import IPv4Address, IPv6Address, ip_address


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
		return "\n".join(filtered_result).split("For more information on ")[0]
	else:
		return None


def ip_info(ip):
	result = f'Target: `{ip}`\n'
	ipinfo_response = requests.get(f'https://ipinfo.io/{ip}/json').json()
	ipapi_response = requests.get(f'http://ip-api.com/json/{ip}').json()
	result += f'Region: `f{ipinfo_response["city"]}` \- `{ipinfo_response["region"]}` \- `{ipinfo_response["country"]}`\n'
	result += f'ASN: `{ipinfo_response["org"].split(" ")[0]}`\n'
	if 'hostname' in ipinfo_response:
		result += f'Hostname: `{ipinfo_response["hostname"]}`\n'
	result += f'ISP: `{ipapi_response["isp"]}`\n'
	result += f'Organization: `{ipapi_response["org"]}`\n'
	if 'anycast' in ipinfo_response:
		result += 'This is an anycast IP address'
	return result


def ip_info_alicloud(ip, appcode):
	result = f'Target: `{ip}`\n'
	response = None
	ip = ip_address(ip)
	if isinstance(ip, IPv4Address):
		response = requests.get(url=f'https://ipcity.market.alicloudapi.com/ip/city/query?coordsys=coordsys&ip={ip}',
														headers={"Authorization": f"APPCODE {appcode}"}
														).json()['data']['result']
	if isinstance(ip, IPv6Address):
		response = requests.get(url=f'https://ipv6city.market.alicloudapi.com/ip/ipv6/query?coordsys=coordsys&ip={ip}',
														headers={"Authorization": f"APPCODE {appcode}"}
														).json()['data']['result']
	result += f'Region: `{response["city"]}` \- `{response["prov"]}` \- `{response["country"]}`\n'
	result += f'ASN: `{response["asnumber"]}`\n'
	result += f'ISP: `{response["isp"]}`\n'
	return result
