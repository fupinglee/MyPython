__Date__="20180612"


'''
Usage:
    python port_check_jsp.py http://localhost:8088/dama.jsp 192.168.135.133
	python port_check_jsp.py http://localhost:8088/dama.jsp 192.168.135.0/24
	
Python version: 3.6.2
requirements:IPy==0.83
beautifulsoup4==4.6.0
'''

import requests
from bs4 import BeautifulSoup
from IPy import IP
import sys
import time

def writeFile(path,content):
	with open(path,"a")as f:
		f.write(content)

def check(url,path,ip):
	try:
		data = {
			'o':'portScan',
			'ip':ip,
			'ports':'80,8080,8088,8888,1433,3306,3389,7001,7002',
			'timeout':'2',
			'submit':'Scan',
		}
		cookies = {
			'JSESSIONID':'E806EE7B710702AA8AB7383060FAACEA',
			'BIGipServerweishequ_app_38085_pool':'1678118922.50580.0000'
		}
		res = requests.post(url,data=data,cookies=cookies)
		soup = BeautifulSoup(res.content,'lxml')
		ip_results_text = soup.find_all(attrs={"style":"margin:10px"})[0].text
		ip_results_str = ip_results_text.strip().replace(' ','')
		print(ip_results_str)
		results = ''
		all_results = ip_results_str.split("\n")
		for all_result in all_results:
			if all_result.find("Open")>0:
				results += all_result + "\n"
		# print(results)
		if results != '':
			writeFile(path,results+"")
	except Exception as e:
		print(ip,"error")
	

if __name__ == '__main__':
	url = sys.argv[1]
	ip = sys.argv[2]
	t = str(round(time.time()*1000))
	if ip.rfind("/")<0:
		path = ip+'_'+t+".txt"
	else:
		pos = ip.rfind(".")
		path = ip[:pos]+'_'+t+".txt"
	ips = IP(ip)
	for i in ips:
		check(url,path,i)