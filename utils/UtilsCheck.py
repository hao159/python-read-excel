import re
import socket
import netifaces as ni


def look_ip_address():
	ni.ifaddresses('eth0')
	ip = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']
	return ip

def look_port(host):
	startPort = 8180
	port_conf = 8180
	while True:
		print(startPort)
		if is_port_in_use(host, startPort) == False:
			return startPort
		startPort = startPort + 1

def is_port_in_use(host, port):
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		return s.connect_ex((host, port)) == 0

def validUrl(url):
	regex = re.compile(
		r'^(?:http|ftp)s?://' # http:// or https://
		r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
		r'localhost|' #localhost...
		r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
		r'(?::\d+)?' # optional port
		r'(?:/?|[/?]\S+)$', re.IGNORECASE)
	return re.match(regex, url) is not None
