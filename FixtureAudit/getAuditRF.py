#-*- coding: utf-8 -*-
# 1. get 站别列表。
# 2. 读取testlog  SN，FixtureSN , 这样就把资料丢到IT。
# 3. 
# 4. 上传

import os,re,paramiko,glob ,traceback
import datetime,json,sys,requests,time
from paramiko import SSHClient

logName = 'getAuditRFLog'

def readSetting():
    global Jsetting     
    with open(sys.path[0] + os.path.sep + 'getAuditRFSet.json' ,'r') as jf:
        Jsetting = json.load(jf)

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

def cleanLog(pattern:str,keepDays:int):
    '''
    删除某目录下log ， 保留N天
    sample. cleanLog('/vault/getAuditRFLog*.txt',10)
    '''
    for f in glob.glob(pattern):
        info=os.stat(f)
        mt= time.localtime(info.st_mtime)
        dtmt = datetime.datetime(mt[0],mt[1],mt[2],mt[3],mt[4],mt[5])
        passedDay = datetime.datetime.now()-dtmt
        if passedDay.days>keepDays:
            os.remove(f)
            myLog('delete file ' + f)

def getStationIDList(product,stationType)->dict:
    '''
    通过URL 得到对应的站别的IP列表。
    '''
    kw = {'c':'getstationlist','product':product,"stationtype":stationType}
    # headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
    response = requests.get(Jsetting['getStationListurl'], params = kw) 
    return json.loads(response.text)

def getARecentNewFile_Today(_IP,_rPathDir:str,_lPath:str)->bool:
    '''
    给出一个IP，_rPath一个远程目录，把最新的一个.log 文件copy回来 ,修改日期要1天之内。
     , _lPath 本地文件路径。
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
        
        sftp=ssh.open_sftp() 
         
        lstAttr=sftp.listdir_attr(_rPathDir)
        d = datetime.datetime.now()-datetime.datetime.strptime('1970/1/1 00:00:00', '%Y/%m/%d %H:%M:%S')
        curSec= d.total_seconds() - 60*60*24
        lstAttr=[x for x in  lstAttr if x.filename.endswith('.log') and x.st_mtime > curSec ]

        lstAttr.sort(key= lambda a : -a.st_mtime )
        if lstAttr.__len__() >0:
            myLog( 'getting file :' + _IP +' ' + os.path.join( _rPathDir ,lstAttr[0].filename))
            sftp.get( os.path.join( _rPathDir ,lstAttr[0].filename) ,_lPath)
            ssh_Exec_Wait(ssh,f'for i in {_rPathDir}*.log;do mv "$i" "$i.txt" ;done')
            ssh.close()   
            return True
        else:
            ssh_Exec_Wait(ssh,f'for i in {_rPathDir}*.log;do mv "$i" "$i.txt" ;done')
            ssh.close()   
            myLog(f"No found new log for {_IP}")
            return False
    except Exception as e1: 
        myLog("getARecentNewFile Failed",_IP,traceback.format_exc())
        try:
            ssh.close()
        except:
            pass
        return False


def getA_CalFile (_IP,_rPathDir:str,_lPath:str)->str:
    '''
    给出一个IP，_rPath一个远程目录， 每次搞回来一个文件 ,return '' 就是找不到文件了.搞不回来文件就不再掉用这个函数了
    找到的文件不处理。如需转移，需调用MoveAFile_ssh
    '''
    try:
        a = os.popen(f'ping -c 1 -t 1 {_IP}')
        res=a.read()
        if re.search("ttl=",res):
            pass
        else: 
            return ''
        ssh = paramiko.SSHClient() 
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy )
        ssh.connect(_IP,port=22,username='gdlocal',password='gdlocal')
        
        sftp=ssh.open_sftp() 
         
        lstAttr=sftp.listdir_attr(_rPathDir) 
        lstAttr=[x for x in  lstAttr if x.filename.endswith('.log')  ]
        if lstAttr.__len__() >0:
            myLog( 'getting file :' + _IP +' '+ os.path.join( _rPathDir ,lstAttr[0].filename))
            sftp.get( os.path.join( _rPathDir ,lstAttr[0].filename) ,_lPath) 
            ssh.close()
            return lstAttr[0].filename
        else: 
            ssh.close()   
            myLog(f"No found new log for {_IP}")
            return ''
    except Exception as e1: 
        myLog(f"{sys._getframe().f_code.co_name} Failed",traceback.format_exc())
        try:
            ssh.close()
        except:
            pass
        return ''


def getA_T677File (_IP,_rPathDir:str,_lPath:str)->str:
    '''
    给出一个IP，_rPath一个远程目录， 每次搞回来一个文件 ,return '' 就是找不到文件了.搞不回来文件就不再掉用这个函数了
    找到的文件不处理。如需转移，需调用MoveAFile_ssh
    T677 Cal 里是以文件夹存放的。要单独处理
    '''
    try:
        a = os.popen(f'ping -c 1 -t 1 {_IP}')
        res=a.read()
        if re.search("ttl=",res):
            pass
        else: 
            return ''
        ssh = paramiko.SSHClient() 
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy )
        ssh.connect(_IP,port=22,username='gdlocal',password='gdlocal')
        
        sftp=ssh.open_sftp() 
        
        lstAttr=sftp.listdir_attr(_rPathDir) 
        lstAttr=[x for x in  lstAttr if x.filename.count('_')>3  ] #2021_11_26_19_22_1637925741 文件夹名字
        if lstAttr.__len__() >0:
            lstAttrFile=sftp.listdir_attr(_rPathDir + lstAttr[0].filename )
            lstAttrFile=[x for x in lstAttrFile if x.filename.endswith('csv')]
            if len(lstAttrFile) >0:
                myLog( 'getting file :' + _IP +' ' + os.path.join( _rPathDir ,lstAttr[0].filename) + os.path.sep +lstAttrFile[0].filename)
                sftp.get( os.path.join( _rPathDir ,lstAttr[0].filename) +os.path.sep + lstAttrFile[0].filename  ,_lPath)
                ssh.close()
                return lstAttr[0].filename
            else:
                with open(_lPath,'w') as ww:
                    ww.write('no found csv file.')
                return lstAttr[0].filename
        else: 
            ssh.close()   
            myLog(f"No found new log for {_IP}")
            return ''
    except Exception as e1: 
        myLog(f"{sys._getframe().f_code.co_name} Failed",traceback.format_exc())
        try:
            ssh.close()
        except:
            pass
        return ''

def MoveAFile_ssh (_IP,_rPathDir:str ,fileName:str)->bool:
    '''
    给出一个IP，_rPath一个远程目录， 每次搞回来一个文件.搞不回来文件就不再掉用这个函数了
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
        
        sftp=ssh.open_sftp()    
        myLog( 'Move file :' + os.path.join( _rPathDir ,fileName))
        _rPathDir = _rPathDir if _rPathDir[-1] != '/' else _rPathDir[:-1]
        ssh_Exec_Wait(ssh,f'mkdir {_rPathDir}DONE/')
        ssh_Exec_Wait(ssh,f'mv '+os.path.join( _rPathDir ,fileName) + f' {_rPathDir}DONE/')
        # ssh.exec_command(f'mkdir {_rPathDir}DONE/') 
        # ssh.exec_command(f'mv '+os.path.join( _rPathDir ,fileName) + f' {_rPathDir}DONE/') 
        ssh.close()
        return True 
    except Exception as e1: 
        myLog(f"{sys._getframe().f_code.co_name} Failed",traceback.format_exc())
        try:
            ssh.close()
        except:
            pass
        return False
def ssh_Exec_Wait(_ssh:SSHClient,cmd:str)->str:
    '''
    use ssh to run the command and read the result.
    if you do not read the result.
    it may fail. because of the command did not run finish.'''
    stdin,stdout,stdErr=_ssh.exec_command(cmd)
    outTxt = stdout.read().decode('utf-8')
    return outTxt 


def uploadAResult_Online(stationID,equipSN,equipName,AuditDate:datetime.datetime,expDay:int,AlertDay:int,stationtype,product,line,IP=''):
    '''
        上线才倒计时。 flag=N 
        alertDay 提前多少天预警
       {"SN":"xxx","stationId":"xxx","product":"xxx","stationType":"xxx","fixtureType":
"xxx","line":"xxx","expDay":"xxx","alertDay":"xxx","ip":"xxx","operateType":"radioStart"}
    ''' 
    kw = { 
    'SN':equipSN,
    'stationId':stationID,
    'product':product,
    'stationType': stationtype,
    'fixtureType':equipName,
    'line':line,
    'expDay':expDay,
    'alertDay':AlertDay,
    'ip':IP,
    'operateType':'radioStart',
    'flag':'N'
    }
    headers1={ "Content-Type":"application/json","token":"test"
    }
    kwStr= json.dumps(kw)
  
    response = requests.post(Jsetting['uploadAuditDateurl'],data= kwStr, params = kw ,headers=headers1) 
    if response.text.lower().__contains__('success'):
        myLog(stationID + f' {IP} upload {sys._getframe().f_code.co_name} ok  auditDate=' , AuditDate,equipSN,equipName )
    else:
        myLog(stationID + f' {IP} upload {sys._getframe().f_code.co_name} Fail **********' + '\r\nsend:'+kwStr+'\r\nReceive:'+ response.text) 

def uploadAResult_Cal_Wait1STonline(stationID,equipSN,equipName,AuditDate:str,expDay:int,AlertDay:int,stationtype,product,line,IP='')->bool:
    '''
        T536,T265 Cal 不倒计时，上线才倒计时。  
      {"SN":"xxx","stationId":"xxx","product":"xxx","stationType":"xxx","fixtureType":
        "xxx","line":"xxx","auditDate":"xxx","ip":"xxx","operateType":"radioStartReset"}
    ''' 
    kw = { 
    'SN':equipSN,
    'stationId':stationID,
    'product':product,
    'stationType': stationtype,
    'fixtureType':equipName,
    'line':line,
    'auditDate':AuditDate, 
    'ip':IP,
    'operateType':'radioStartReset'
    }
    headers1={ "Content-Type":"application/json","token":"test"
    }
    kwStr= json.dumps(kw)
  
    response = requests.post(Jsetting['uploadAuditDateurl'],data= kwStr, params = kw ,headers=headers1) 
    if response.text.lower().__contains__('success'):
        myLog(stationID + f' {IP} upload {sys._getframe().f_code.co_name} ok  auditDate=' , AuditDate,equipSN,equipName )
        return True
    else:
        myLog(stationID + f' {IP} upload {sys._getframe().f_code.co_name} Fail **********' + '\r\nsend:'+kwStr+'\r\nReceive:'+ response.text)
        return False

def uploadAResult_CalCountDownNow(stationID,equipSN,equipName,AuditDate:str,expDay:int,AlertDay:int,stationtype,product,line,IP='')->bool:
    '''
        只要完成了cal , 就开始倒计时。T677 ,   (T625,T877 同样逻辑，但是手动上传)
        flag=Y
        alertDay 提前多少天预警
       {"SN":"xxx","stationId":"xxx","product":"xxx","stationType":"xxx","fixtureType":
"xxx","line":"xxx","auditDate":"xxx","expDay":"xxx","alertDay":"xxx","ip":"xxx",
"operateType":"xxx","flag":"XXX"}
    ''' 
    kw = { 
    'SN':equipSN,
    'stationId':stationID,
    'product':product,
    'stationType': stationtype,
    'fixtureType':equipName,
    'line':line,
    'auditDate':AuditDate,
    'expDay':expDay,
    'alertDay':AlertDay,
    'ip':IP,
    'operateType':'radioStart',
    'flag':'Y'
    }
    headers1={ "Content-Type":"application/json","token":"test"
    }
    kwStr= json.dumps(kw)
  
    response = requests.post(Jsetting['uploadAuditDateurl'],data= kwStr, params = kw ,headers=headers1) 
    if response.text.lower().__contains__('success'):
        myLog(stationID + f' {IP} upload {sys._getframe().f_code.co_name} ok  auditDate=' , AuditDate,equipSN,equipName )
        return True
    else:
        myLog(stationID + f' {IP} upload {sys._getframe().f_code.co_name} Fail **********' + '\r\nsend:'+kwStr+'\r\nReceive:'+ response.text)
        return False
 
def getDateFromLog(_lPath:str,equipReg:str)->str:
    '''
    return Equipment SN,DateTimeString(format:'%Y/%m/%d %H:%M:%S')
    todo date format
    '''
    strCont = open(_lPath,'rb').read().decode('utf-8' , 'ignore')
    strSN=re.findall(equipReg,   strCont) 
    strDate= re.findall('Time:\s?(.*?),',strCont)
    strDate= len(strDate) >0 and strDate[0] or ''
    if strDate.count(':')>0:
        strDate=datetime.datetime.strptime(strDate, '%H:%M:%S %m-%d-%Y').strftime('%Y/%m/%d %H:%M:%S') #14:36:53 12-01-2021 ->xx

    if strSN !='':
        strSN =  strSN.__len__()>0  and strSN[0] or "" 
        return strSN,strDate
    else:
        return "",strDate

def int2Time(intIn:int)->datetime.datetime:
    date1 = datetime.datetime.strptime('1970/1/1 00:00:00', '%Y/%m/%d %H:%M:%S')
    date1 = date1 + datetime.timedelta(seconds=intIn)+datetime.timedelta(hours=8)
    return date1

def mainAction_K_Wait1STonline():
    '''
    T536,T265 只是reset,等上线时开始计时
    '''
    myLog('begin K_Wait1STonline (T536,T265 只是reset)'.center(60,'-'))
    readSetting()
    for product,pv in Jsetting["k_list_Wait1STonline"].items():
        
        for aStation,stationV in pv.items():
            if aStation.startswith("#"):
                myLog('bypass ', aStation)
                continue

            IPs = getStationIDList(product,stationV['stationtype'])
            for aIP in IPs: 
                while True :
                    fName= getA_CalFile(aIP['IP'],stationV['audit_file'],"/vault/tmp.1")
                    if fName =='':
                        break

                    equips = stationV["equips"]
                    for Aequip in equips:
                        sn,kDate=getDateFromLog("/vault/tmp.1",Aequip["reg"])
                        if sn !="" and kDate!='': 
                            if uploadAResult_Cal_Wait1STonline(aIP['StationID'],sn,Aequip['name'],kDate,Aequip['expDay'] ,Aequip['alertDay'] , aIP['StationType'],aIP['Product'],aIP['Line'],aIP['IP']):
                                MoveAFile_ssh(aIP['IP'],stationV['audit_file'],fName)

                        else:
                            myLog("read equipment SN fail***",Aequip["name"],aIP['StationID'],aIP['IP'])
                            MoveAFile_ssh(aIP['IP'],stationV['audit_file'],fName)

                # else:
                #     myLog("get log fail*** ", aIP['StationID'], aIP['IP'])

def mainAction_K_CountDownNow():
    '''Re-CalLine (T677 DEVELOPMENT9) 测试PASS开始计时
    '''
    myLog('begin K_CountDownNow (T677)'.center(60,'-'))
    readSetting()
    for product,pv in Jsetting["k_list_CountDownNow"].items():
        
        for aStation,stationV in pv.items():
            if aStation.startswith("#"):
                myLog('bypass ', aStation)
                continue

            IPs = getStationIDList(product,stationV['stationtype'])
            for aIP in IPs:
                while True:
                    fName= getA_T677File(aIP['IP'],stationV['audit_file'],"/vault/tmp.1")
                    if fName =='':
                        break 

                    equips = stationV["equips"]
                    for Aequip in equips: 
                        #T677 get SN,Result,Date from csv
                        strCont = open('/vault/tmp.1','rb').read().decode('utf-8' , 'ignore')
                        strSN=re.findall('\n(.*?),T677,', strCont)  #'C3903060012L69T3X,Pass,,,2021-11-26 19:22:21,2021-11-26 19:33:22'
                        strSN = len(strSN)>0 and strSN[0] or ''
                        ar=re.split(',',strSN)
                        sn = ar[0]
                        kDate = len(ar)>4 and ar[4].replace('-','/') or ''
                        if sn !="" and kDate!='' and ar[1].lower()=='pass': 
                            if uploadAResult_CalCountDownNow(aIP['StationID'],sn,Aequip['name'],kDate,Aequip['expDay'] ,Aequip['alertDay'] , aIP['StationType'],aIP['Product'],aIP['Line'],aIP['IP']):
                                MoveAFile_ssh(aIP['IP'],stationV['audit_file'],fName)
                        else:
                            myLog("read equipment SN fail***",Aequip["name"],aIP['StationID'],aIP['IP'])
                            MoveAFile_ssh(aIP['IP'],stationV['audit_file'],fName)
   
def mainAction_Online():

    myLog('begin Online (T536,T265 online)'.center(60,'-'))
    readSetting()
    for product,pv in Jsetting["station_list_OnLine"].items():
        
        for aStation,stationV in pv.items():
            if aStation.startswith("#"):
                myLog('bypass ', aStation)
                continue

            IPs = getStationIDList(product,stationV['stationtype'])
            for aIP in IPs:
                if getARecentNewFile_Today(aIP['IP'],stationV['audit_file'],"/vault/tmp.1"):
                    equips = stationV["equips"]
                    for Aequip in equips:
                        sn,kDate=getDateFromLog("/vault/tmp.1",Aequip["reg"])
                        if sn !="":
                            #myLog(aIP['StationID'],sn,Aequip["name"],datetime.datetime.now(),Aequip['expDay'] ,Aequip['alertDay'] , aIP['StationType'],aIP['Product'],aIP['Line'],aIP['IP'])
                            uploadAResult_Online(aIP['StationID'],sn,Aequip['name'],datetime.datetime.now(),Aequip['expDay'] ,Aequip['alertDay'] , aIP['StationType'],aIP['Product'],aIP['Line'],aIP['IP'])
                        else:
                            myLog("read equipment SN fail***",Aequip["name"],aIP['StationID'],aIP['IP'])
                        
                else:
                    myLog("get log fail*** ", aIP['StationID'], aIP['IP'])
    myLog("done".center(40,'='))
    cleanLog(f'/vault/{logName}*.txt',9)

def main():
    myLog("program working..")
    readSetting()
    myLog(Jsetting["runTime"])
    lastRun=""
    if datetime.datetime.now().strftime("%H:%M") in Jsetting["runTime"] and datetime.datetime.now().strftime("%H:%M") != lastRun:
        lastRun=datetime.datetime.now().strftime("%H:%M")
        try:
            mainAction_K_CountDownNow()
            mainAction_K_Wait1STonline()
            mainAction_Online()
            time.sleep(60)  #防止重复调用
        except Exception as e:
            myLog (e)
    else:
        time.sleep(10)


if __name__ == "__main__":
    # mainAction_K_Wait1STonline()
    # mainAction_K_CountDownNow()
    # mainAction_Online() 
    main()

    # MoveAFile_ssh('172.16.111.244','/vault/meerkat/F4-MAIN','2022_02_16_13_01_1644987671')


