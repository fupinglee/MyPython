# -*- coding:UTF-8 -*-
__author__ = "浮萍"
__Date__ = "2018/7/5"

"""
参考https://cloud.tencent.com/document/product/866/17600
"""

import requests
import json
import cv2


def getColor(type):
	if type == 0:
		return (0,0,255)
	elif type == 1:
		return (0,255,255)
	elif type == 2:
		return (255,0,0)
headers = {
    'Authorization': 'xxx',
}
url = 'http://recognition.image.myqcloud.com/ocr/general'
data = {
    "appid":"xxx",
    "bucket":"test",
}

ap_path='ap_1534406211.png'
mp_path='mp_1534406211.png'


ap_files = {'image': open(ap_path, 'rb')}
mp_files = {'image': open(mp_path, 'rb')}


ap_res = requests.post(url,data=data, files=ap_files, headers=headers)
mp_res = requests.post(url,data=data, files=mp_files, headers=headers)
ap_res_json = json.loads(ap_res.text)
ap_items_json = ap_res_json['data']['items']
ap_str = ap_items_json[0]['itemstring']
ap_need_str = ap_str[-3:]


mp_res_json = json.loads(mp_res.text)
mp_items_json = mp_res_json['data']['items']
mp_items_len = len(mp_items_json)
img_mp = cv2.imread(mp_path)
for i in range(len(ap_need_str)):
	for j in range(mp_items_len):
		if mp_items_json[j]['itemstring'] == ap_need_str[i]:
			cv2.rectangle(img_mp, (mp_items_json[j]['itemcoord']['x'],mp_items_json[j]['itemcoord']['y']), (mp_items_json[j]['itemcoord']['x'] + mp_items_json[j]['itemcoord']['width'], mp_items_json[j]['itemcoord']['y'] + mp_items_json[j]['itemcoord']['height']), getColor(i), 2)
cv2.imshow('Detected', img_mp)
cv2.waitKey(0)
cv2.destroyAllWindows()