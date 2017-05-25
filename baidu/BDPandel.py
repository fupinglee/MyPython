#! -*- coding:utf-8 -*-
__author__="浮萍"
__Date__="20170524"

import re
import urllib2
import urllib
import json
import MySQLdb
import sys  
import argparse

reload(sys)  
sys.setdefaultencoding('utf8')   
headers = {
   'Host':"pan.baidu.com",
    'Accept':'*/*',
    'Accept-Language':'en-US,en;q=0.8',
    'Cache-Control':'max-age=0',
    'Referer':'https://pan.baidu.com/',
    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
    'Cookie':"BDUSS=;STOKEN=; "
    }

def getbdstoken():
    res_content=r'bdstoken":"(\w*)","quota'
    url = "https://pan.baidu.com/wap/home"
    try:
        req=urllib2.Request(url,headers=headers)
        f=urllib2.urlopen(req)
        content=f.read()
        r = re.compile(res_content)
        return r.findall(content)[0]
    except Exception,e:
        print "[Error]",str(e)
def getFiles(dir):
    url = "https://pan.baidu.com/api/list?bdstoken="+getbdstoken()+"&web=5&app_id=250528&logid=MTQ5NTQxMzA2Njg4ODAuODE0NzYwMjEyMzAzOTY5Mg==&channel=chunlei&clienttype=5&order=time&desc=1&showempty=0&page=1&num=2000&dir="+dir;
    req=urllib2.Request(url,headers=headers)
    f=urllib2.urlopen(req)
    #content=f.read() 
    result = json.loads(f.read())
    for i in result['list']:
        if(i['isdir']):
            p = i['path']
            path = p.decode("utf-8")
            getFiles(urllib.quote(path.encode('utf-8')))
        else:
            #print type((i['path']).encode('utf-8'))
            print i['path']+'-----'+i['md5'] + '------'+str(i['size'])
            #addDatas(i['size'], (i['md5']).encode('utf-8'), (i['path']).encode('utf-8'), (i['server_filename']).encode('utf-8'))
            addDatas(i['size'], i['md5'], i['path'], i['server_filename'])
def addDatas(size,md5,path,server_filename):
    conn= MySQLdb.connect(
            host='127.0.0.1',
            port = 3306,
            user='root',
            passwd='password',
            db ='test',
            charset='utf8'
            ) 
    cur = conn.cursor() 
    sql = "INSERT INTO `test`.`mypan` ( `size`, `md5`, `path`, `server_filename`) VALUES (%s, %s, %s, %s)"
    cur.execute(sql,(size,md5,path,server_filename))
    cur.close()
    conn.commit()
    conn.close()    
def getDelFilePath():
    pathlist = []
    conn= MySQLdb.connect(
            host='127.0.0.1',
            port = 3306,
            user='root',
            passwd='password',
            db ='test',
            charset='utf8'
            ) 
    cur = conn.cursor() 
    sql1 = "select count(*),md5,server_filename from `test`.`mypan` where size > 1024*1024*500 group by md5 HAVING COUNT(md5) >0 order by path"
    r1 = cur.execute(sql1)
    info = cur.fetchmany(r1)
    for ii in info:
        md5 = (ii[1]).encode("utf-8")
        sql2 = "select min(LENGTH(path)) from  `test`.`mypan` where md5= '%s' " % (md5)
        r2 = cur.execute(sql2)  
        info_length = cur.fetchall()
        filesize = info_length[0][0]
        sql3 = "select path from `test`.`mypan` where md5='%s' and LENGTH(path) > %s" % (md5,filesize)
        r3 = cur.execute(sql3)  
        paths = cur.fetchall()
        for path in paths:
            pathlist.append(path[0])
    cur.close()
    conn.commit()
    conn.close()
    return pathlist
def getFileList(filelist):
    result = '["'
    for path in pathlist:
        
        result = result +path   +'","' 
    result = result + '**************'
    return result.replace(',"**************', "]")
def delFiles(filelist):
    filelist =  filelist.decode("utf-8")
    url = "https://pan.baidu.com/api/filemanager?opera=delete&async=2&channel=chunlei&web=1&app_id=250528&bdstoken="+getbdstoken()+"&logid=MTQ5NTU0ODk4Mjk2MjAuMzgyNjczNDYzNDM0MTU0NA==&clienttype=0"
    data = {
        'filelist':filelist
    }
    req=urllib2.Request(url,headers=headers,data=urllib.urlencode(data))
    f=urllib2.urlopen(req)
    #print type(f.read())
    json_r = f.read()
    result = json.loads(json_r)
    if (result['errno']):
        print "文件删除失败"
    else:
        print "文件删除成功，删除成功的文件为"+filelist
        
    #result = json.loads(f.read().encode('utf-8')) 
def delJob():
    pathlist = getDelFilePath()
    filelist = getFileList(pathlist)
    delFiles(filelist)
if __name__ == '__main__':
    #getbdstoken()
    #getFiles('/')
    #delJob()
    
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-m',help="method to do")
    args=parser.parse_args()
    if args.m:
        if args.m == '1':
            getFiles('/')
        elif args.m == '2':
            delJob()
        else:
            print 'error args'
    else:
    print parser.print_help()
    exit(0)
    
    
            
    