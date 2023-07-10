from shlex import quote
import subprocess


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
