
import os,paramiko,re,sys

def SendAFile(_IP,_rPath:str,_lPath:str,userName='gdadmin',userPWD='gdadmin')->bool:
    '''
    给出一个IP，_rPath一个远程文件路径，lPath 本地文件路径。 send local path to remote path.
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
        ssh.connect(_IP,port=22,username=userName,password=userPWD)
        
        sftp=ssh.open_sftp()
        sftp.put(_lPath,_rPath)
        #ssh.exec_command('rm /vault/temp.temp')
        ssh.close()
  
        return True
    except Exception as e1: 
        print(e1)
        return False

# lpath=sys.path[0] + os.path.sep +'getAuditData.py'
# rpath='/Users/gdadmin/Documents/getAuditData/getAuditData.app/Contents/Resources/getAuditdata.py'
# a = SendAFile('10.42.151.26',rpath ,lpath)
# print(a)

# lpath=sys.path[0] + os.path.sep +'getAuditDataSet.json'
# rpath='/Users/gdadmin/Documents/getAuditData/getAuditData.app/Contents/Resources/getAuditDataSet.json'
# a = SendAFile('10.42.151.26',rpath ,lpath)
# print(a)

# print('push RF audit...')
# lpath=sys.path[0] + os.path.sep +'getAuditRF.py'
# rpath='/Users/gdadmin/Documents/getAuditData/getAuditData.app/Contents/Resources/getAuditRF.py'
# a = SendAFile('10.42.151.26',rpath ,lpath)
# print(a)

# lpath=sys.path[0] + os.path.sep +'getAuditRFSet.json'
# rpath='/Users/gdadmin/Documents/getAuditData/getAuditData.app/Contents/Resources/getAuditRFSet.json'
# a = SendAFile('10.42.151.26',rpath ,lpath)
# print(a)


print('push py file audit...')
lpath= '/Volumes/DATA/MAC_OS/Program/pythonStudy/socket/socket_Server.py'

rpath='/vault/sck1.py'
a = SendAFile('172.16.30.48',rpath ,lpath,'gdlocal','gdlocal')
print(a)