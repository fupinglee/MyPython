#! -*- coding:utf-8 -*-
__author__="浮萍"
__Date__="20170620"


import json
import time
import requests
import time
import hashlib
import re
from urllib import unquote
from collections import OrderedDict
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
class TBAutoSign:
    def __init__(self,BDUSS):
        self.BDUSS = BDUSS
        self.userName = None
        self.userId = None
    def getUserName(self):
        url = 'http://wapp.baidu.com/'
        BAIDUID = getMd5(str(int(time.time())))
        cookies = {
            'BAIDUID':BAIDUID,
            'BDUSS':self.BDUSS
        }
        res = requests.get(url, cookies=cookies)
        userName = re.findall('i?un=(.*?)\">',res.text)[0]
        #
        self.userName = userName
    def getUserID(self):
        url = 'http://tieba.baidu.com/home/get/panel?ie=utf-8&un=' + self.userName
        res = requests.get(url)
        result = json.loads(res.text)
        userid = result['data']['id']
        self.userId = userid
    def getTieba(self):
        url = 'http://c.tieba.baidu.com/c/f/forum/like'
        pn = 1
        data = OrderedDict()
        data['_client_id'] = 'wappc_' + str(int(time.time())) + '_258'
        data['_client_type'] = str(2)
        data['_client_version'] = '6.5.8'
        data['_phone_imei'] = '357143042411618'
        data['from'] = 'baidu_appstore'
        data['is_guest'] = str(1)
        data['model'] = 'H60-L01'
        data['page_no'] = str(pn)
        data['page_size'] = str(200)
        data['timestamp'] = str(int(time.time()))+'903'
        data['uid'] = self.userId
        sign_str = ''
        for k,v in data.items():
            sign_str = sign_str + (k+'='+str(v))
        sign = getMd5(sign_str+'tiebaclient!!!')
        data['sign'] = sign
        cookies = {
            'BDUSS':self.BDUSS
        }
        res = requests.post(url,data=data,cookies=cookies)
        js_non = json.loads(res.text)['forum_list']['non-gconforum']
        js_non.extend(json.loads(res.text)['forum_list']['gconforum'])
        for tb in js_non:
            print tb['name'],'[级别:'+tb['level_id'],'头衔:'+tb['level_name'],'当前经验:'+tb['cur_score'],'下一等级经验:'+tb['levelup_score']+']',DoSign_Client(self.BDUSS,tb['name'])
        #print len(js_non)
        
        
def DoSign_Client(bduss,kw,fid='1'):  
    url = 'http://c.tieba.baidu.com/c/c/forum/sign'
    cookies = {
        'BDUSS':bduss
    }
    data = OrderedDict()
    data['BDUSS'] = bduss
    data['_client_id'] = '03-00-DA-59-05-00-72-96-06-00-01-00-04-00-4C-43-01-00-34-F4-02-00-BC-25-09-00-4E-36'
    data['_client_type'] = '4'
    data['_client_version'] = '1.2.1.17'
    data['_phone_imei'] = '540b43b59d21b7a4824e1fd31b08e9a6'
    data['fid'] = fid
    data['kw'] = kw
    data['net_type'] = '3'
    data['tbs'] = getTBS(bduss) 
    sign_str = ''
    for k,v in data.items():
        sign_str = sign_str + (k+'='+v)
    sign = getMd5(sign_str+'tiebaclient!!!')
    data['sign'] = sign
    res = requests.post(url,data=data,cookies=cookies)
    result = json.loads(res.text)
    return (result['error_msg'])
def getTBS(bduss):
    url = 'http://tieba.baidu.com/dc/common/tbs'
    cookies = {
        'BDUSS':bduss
    }
    res = requests.get(url, cookies=cookies)
    result = json.loads(res.text)
    return result['tbs']
def getMd5(p):
    m = hashlib.md5()
    m.update(p)
    return m.hexdigest().upper()
def getResult(k):
    
    return 
if __name__ == '__main__':

    BDUSS = '你的BDUSS'
    autoSign = TBAutoSign(BDUSS)
    autoSign.getUserName()
    autoSign.getUserID()
    autoSign.getTieba()


