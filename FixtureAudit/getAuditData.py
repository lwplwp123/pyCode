#-*- coding: utf-8 -*-
# 1. get 站别列表。
# 2.每个站读取出来Audit文件
# 3.解析Audit文件的Audit 时间
# 4. 上传
# 搞个配置文件 getAuditdataSet.json
# 使用 socket.bind 保证只运行单个程序
 
import glob
import json , plistlib,re
import os,sys
import time
import datetime 
import requests
import paramiko
import logging
from socket import *
import atexit

from requests.api import request

# 全局变量 Jsetting 
# 

logName = 'AuditLog'


def readSetting():
    '''
       global Jsetting   
    '''
    global Jsetting     
    with open(sys.path[0] + os.path.sep + 'getAuditDataSet.json' ,'r') as jf:
        Jsetting = json.load(jf)

def getStationIDList(product,stationType)->dict:
    '''
    通过URL 得到对应的站别的IP列表。
    '''
    kw = {'c':'getstationlist','product':product,"stationtype":stationType}
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
    response = requests.get(Jsetting['getStationListurl'], params = kw) 
    return json.loads(response.text)

def getAFile(_IP,_rPath:str,_lPath:str)->bool:
    '''
    给出一个IP，_rPath一个远程文件路径，copy回来 _lPath 本地文件路径。
    '''
    try:
        a = os.popen(f'ping -c 1 -t 1 {_IP}')
        res=a.read()
        if re.search("ttl=",res):
            pass
        else: 
            return False

        ssh = paramiko.SSHClient() 
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy )
        ssh.connect(_IP,port=22,username='gdlocal',password='gdlocal')
        
        fname = _rPath.split( os.path.sep)[-1]   #hidden file , sftp can not handle it.
        if fname.startswith('.'):
            stdin,stdout,stdErr=ssh.exec_command('cp '+ _rPath + ' /vault/temp.temp')
            outTxt = stdout.read().decode('utf-8')
            if outTxt=="":
                _rPath = '/vault/temp.temp'
            else:
                return False 

        sftp=ssh.open_sftp()
        sftp.get(_rPath,_lPath)
        #ssh.exec_command('rm /vault/temp.temp')
        ssh.close()

        # transport = paramiko.Transport((_IP,22))
        # transport.connect(username='a',password='1234') 
        # sftp = paramiko.SFTPClient.from_transport(transport)
        # sftp.get(_rPath,_lPath)
 
        return True
    except Exception as e1: 
        return False


def uploadAResult(stationID,AuditDate:datetime.datetime,AuditDay:int,AlertDay:int,stationtype,product,line,IP=''):
    '''
        auditDay 多少天后过期。
        alertDay 提前多少天预警
        updateauditdate&stationid=LXKS_A01-2FT-01_7_QT0&auditdate=2020/2/2%2011:11:11&expdate=2020/3/3%2011:11:11&stationtype=xx&product=xx&line=xx
    '''
    expDate=AuditDate +  datetime.timedelta(days=AuditDay)
    alertDate =expDate + datetime.timedelta(days=-AlertDay)
    kw = {'c':'updateauditdate',
    'operateType':'updateauditdate',
    'stationId':stationID,
    'auditDate':AuditDate.strftime('%Y/%m/%d %H:%M:%S'),
    'expDate':expDate.strftime('%Y/%m/%d %H:%M:%S'),
    'alertDate':alertDate.strftime('%Y/%m/%d %H:%M:%S'),
    'stationType': stationtype,
    'product':product,
    'line':line,
    'ip':IP
    }
    headers1={ "Content-Type":"application/json","token":"test"
    }
    kwStr= json.dumps(kw)
  
    response = requests.post(Jsetting['uploadAuditDateurl_bak'],data= kwStr, params = kw ,headers=headers1)
    response = requests.post(Jsetting['uploadAuditDateurl'],    data= kwStr, params = kw ,headers=headers1)
    # response = requests.post(url=Jsetting['uploadAuditDateurl'], params = kw ) 

    if response.text.lower().__contains__('ok') or response.text.lower().__contains__('success'):
        myLog(stationID + f' {IP} upload ok  auditDate=' , AuditDate )
    else:
        myLog(stationID + f' {IP} upload Fail **********' + '\r\nsend:'+kwStr+'\r\nReceive:'+ response.text)


def readAuditDate_csc(_file):
    '''
    每一站都要有一个专用都读取函数。
    readAuditDate_xxx  xxx为站别明，全小写
    csc(D63 COMPASS-CAL)站， 这是个plist 文件，内容
    '''
    b1=open(_file,'rb').read()
    p1=plistlib.loads(b1)
    return p1['AuditDate'] + datetime.timedelta(hours=8)

def readAuditDate_isd(_file):
    '''
    每一站都要有一个专用都读取函数。
    readAuditDate_xxx  xxx为站别明，全小写
    isd (D63 DISPLAY-POSTBURN)站， json 文件，内容
    '''
    with open( _file ,'r') as jf:
        aJson = json.load(jf)
    auditTime = aJson['AsteriaAuditTime']
    date1 = datetime.datetime.strptime('1970/1/1 00:00:00', '%Y/%m/%d %H:%M:%S')
    date1 = date1 + datetime.timedelta(seconds=auditTime)+datetime.timedelta(hours=8)
    return date1

def readAuditDate_dvi(_file):
    ''' 
    每一站都要有一个专用都读取函数。
    readAuditDate_xxx  xxx为站别明，全小写
    dvi(D63 DISPLAY)站， json 文件，内容
    '''
    with open( _file ,'r') as jf:
        aJson = json.load(jf)
    auditTime = aJson['auditTime']
    date1 = datetime.datetime.strptime('1970/1/1 00:00:00', '%Y/%m/%d %H:%M:%S')
    date1 = date1 + datetime.timedelta(seconds=auditTime)+datetime.timedelta(hours=8)
    return date1

def readAuditDate_xtalk_cal(_file):
    ''' 
    每一站都要有一个专用都读取函数。
    readAuditDate_xxx  xxx为站别明，全小写
    xtalk_cal(D63 ALS X-TALK CAL)站， json 文件，内容
    '''
    with open( _file ,'r') as jf:
        aJson = json.load(jf)
    auditTime = aJson['audit']
    date1 = datetime.datetime.strptime('1970/1/1 00:00:00', '%Y/%m/%d %H:%M:%S')
    date1 = date1 + datetime.timedelta(seconds=auditTime)+datetime.timedelta(hours=8)
    return date1
def readAuditDate_voyager(_file):
    ''' 
    每一站都要有一个专用都读取函数。
    readAuditDate_xxx  xxx为站别明，全小写
    voyager(D63 COMPLIANCE10)站， json 文件，内容
    '''
    b1=open(_file,'rb').read()
    p1=plistlib.loads(b1) 
    auditTime=p1['Timestamp']
    date1 = datetime.datetime.strptime('1970/1/1 00:00:00', '%Y/%m/%d %H:%M:%S')
    date1 = date1 + datetime.timedelta(seconds=auditTime)+datetime.timedelta(hours=8)
    return date1

def readAuditDate_alpha(_file):
    ''' 
    每一站都要有一个专用都读取函数。
    readAuditDate_xxx  xxx为站别明，全小写
    alpha(D63 COMPLIANCE5)站， json 文件，内容
    '''
    b1=open(_file,'rb').read()
    p1=plistlib.loads(b1) 
    auditTime=p1['Records'][0]['Timestamp'] 
    date0 = datetime.datetime.strptime('1970/1/1 00:00:00', '%Y/%m/%d %H:%M:%S')
    return date0 + datetime.timedelta(seconds=auditTime)+datetime.timedelta(hours=8)

def readAuditDate_miyagi(_file):
    ''' 
    每一站都要有一个专用都读取函数。
    readAuditDate_xxx  xxx为站别明，全小写
    miyagi(D63 COMPLIANCE4)站， json 文件，内容
    '''
    b1=open(_file,'rb').read()
    p1=plistlib.loads(b1) 
    auditTime=p1['Timestamp'] 
    date0 = datetime.datetime.strptime('1970/1/1 00:00:00', '%Y/%m/%d %H:%M:%S')
    return date0 + datetime.timedelta(seconds=auditTime)+datetime.timedelta(hours=8)

def readAuditDate_fact21(_file):
    ''' 
    每一站都要有一个专用都读取函数。
    readAuditDate_xxx  xxx为站别明，全小写
    fact21(D63 FACT)站， rlist 文件，内容
    '''
    with open( _file ,'r') as jf:
        aTxt = jf.read()
    
    auditTime=int( re.findall(r'CalibrationDate\s?:\s?(.*?)\n',aTxt)[0])
    # auditTime = aJson['CalibrationData']['CalibrationDate']
    date0 = datetime.datetime.strptime('1970/1/1 00:00:00', '%Y/%m/%d %H:%M:%S')
    return date0 + datetime.timedelta(seconds=auditTime)+datetime.timedelta(hours=8)

def readAuditDate_sa_fact2(_file):
    ''' 
    每一站都要有一个专用都读取函数。
    readAuditDate_xxx  xxx为站别明，全小写
    sa_fact2(D63 SA FACT2)站， rlist 文件，内容
    '''
    return readAuditDate_fact21(_file)
def readAuditDate_vent2(_file):
    ''' 
    每一站都要有一个专用都读取函数。
    readAuditDate_xxx  xxx为站别明，全小写
    vent2(D63 SA vibrator)站， rlist 文件，内容
    '''
    return readAuditDate_fact21(_file)

def mainAction():
    readSetting()
    for product,pv in Jsetting["station_list"].items():
        
        for aStation,stationV in pv.items():
            if aStation.startswith("#"):
                myLog('bypass ', aStation)
                continue

            IPs = getStationIDList(product,stationV['stationtype'])
            for aIP in IPs:
                if (datetime.datetime.now()-datetime.datetime.strptime( aIP['LastHearFrom'],'%Y-%m-%d %H:%M:%S')).days >3 : #3天没有响应的电脑不管了。  
                    myLog(f"{aIP['StationID']}  {aIP['IP']} out of date **********")
                    continue

                lFile='/vault/tmp.xxx'
                if getAFile(aIP['IP'],stationV['audit_file'],lFile):
                    date1 = eval( f"readAuditDate_{aStation.lower()}({lFile!r})")
                    uploadAResult(aIP['StationID'],date1,stationV['auditDay'] ,stationV['alertDay'] , aIP['StationType'],aIP['Product'],aIP['Line'],aIP['IP'])
                else:
                    myLog('Fail *** read audit file ', aIP['StationID'] , aIP['IP'])
    myLog("done".center(40,'='))
    cleanLog(f'/vault/{logName}*.txt',9)
def main():
    global udpServer
    udpServer =socket(AF_INET,SOCK_DGRAM)
    try:
        udpServer.bind(("localhost",10189))
    except Exception as e1:
        myLog(e1)
        myLog("program already running...")
        exit(1)

    lastRun=""
    myLog("program working..")
    readSetting()
    myLog(Jsetting["runTime"])
    # while True:
    #     if datetime.datetime.now().strftime("%H:%M") in Jsetting["runTime"] and datetime.datetime.now().strftime("%H:%M") != lastRun:
    #         lastRun=datetime.datetime.now().strftime("%H:%M")
    #         try:
    #             main()
    #         except Exception as e:
    #             myLog (e)
    #     else:
    #         time.sleep(5)
 
    if datetime.datetime.now().strftime("%H:%M") in Jsetting["runTime"] and datetime.datetime.now().strftime("%H:%M") != lastRun:
        lastRun=datetime.datetime.now().strftime("%H:%M")
        try:
            mainAction()
            time.sleep(60)  #防止重复调用
        except Exception as e:
            myLog (e)
    else:
        time.sleep(10)

def cleanLog(pattern:str,keepDays:int):
    '''
    删除某目录下log ， 保留N天
    sample. cleanLog(f'/vault/{logName}*.txt',10)
    '''
    for f in glob.glob(pattern):
        info=os.stat(f)
        mt= time.localtime(info.st_mtime)
        dtmt = datetime.datetime(mt[0],mt[1],mt[2],mt[3],mt[4],mt[5])
        passedDay = datetime.datetime.now()-dtmt
        if passedDay.days>keepDays:
            os.remove(f)
            myLog('delete file ' + f)

def myLog( *msg,path1='/vault',fileName=logName):
    '''
    在制定目录下生成 filename+日期.txt
    '''
    if not os.path.exists(path1):
        os.makedirs(path1)
    logfile= path1 + os.path.sep+ fileName +datetime.datetime.now().strftime('%Y-%m-%d')+'.txt'
    s = ( str(x) for x in msg ) 
    content=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S ') + ' '.join(s)
    with open(logfile,'a') as fw:
        fw.write( content + '\r\n')
    print(content)

@atexit.register
def finishe_cleanup():
    try:
        myLog("close, clean app.")
        udpServer.close()
    except:
        pass

if __name__ == "__main__":
    main()


