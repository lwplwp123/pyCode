#coding:utf-8
#
#test 3
#用transport实现上传下载以及命令的执行：
# ditto -cVvk --keepParent /Library/Frameworks/Python.framework/Versions/3.7 /vault/3.7.zip

from datetime import datetime
import paramiko
 
import os,sys


class SSHConnection(object):

    def __init__(self, host='10.42.151.96', port=22, username='gdadmin',pwd='gdadmin'):
        self.host = host
        self.port = port
        self.username = username
        self.pwd = pwd
        self.__k = None

    def connect(self):
        transport = paramiko.Transport((self.host,self.port))
        transport.connect(username=self.username,password=self.pwd)
        self.__transport = transport

    def close(self):
        self.__transport.close()

    def upload(self,local_path,target_path):
        # 连接，上传
        # file_name = self.create_file()
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        # 将location  上传至服务器 /tmp/test.py
        sftp.put(local_path, target_path)

    def download(self,remote_path,local_path):
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        sftp.get(remote_path,local_path)

    def runCmd(self, command):
        ssh = paramiko.SSHClient()
        ssh._transport = self.__transport
        # 执行命令
        stdin, stdout, stderr = ssh.exec_command(command)
        # 获取命令结果
        result = stdout.read().decode('utf-8','ignor')
        print (result)
        return result
    def RemoteScp(self, remote_path, local_path): 
        sftp = paramiko.SFTPClient.from_transport(self.__transport)
        try:
            remote_files = sftp.listdir(remote_path)
            for file in remote_files:   #遍历读取远程目录里的所有文件
                local_file = local_path + file
                remote_file = remote_path + file
                os.makedirs(local_path,exist_ok=True)
                sftp.get(remote_file, local_file)
            return ("remote SCP finished OK.")
        except IOError as e1:   #  如果目录不存在则抛出异常
            return ("remote_path or local_path is not exist "   )

# ssh = SSHConnection(host='10.42.151.96')
def InstallPY3_7(IP:str,ForceReinstall:bool=False,username='gdlocal',pwd='gdlocal'):
    '''
    Make sure ~/Library/Frameworks has installed py3.7
    '''
    a_ssh = SSHConnection(host=IP,username=username,pwd=pwd)
    a_ssh.connect()
    if  ForceReinstall==False:
        checkPy3=a_ssh.runCmd("ls ~/Library/Frameworks/Python.framework/Versions/3.7/bin/python3")
        if checkPy3 !='':
            print("Already have py3.7")
            return ("OK") 
    print('begin upload..')
    a_ssh.upload( os.path.join(  sys.path[0] , '3.7.zip'),'/vault/3.7.zip')
    print('upload zip OK')
    print(a_ssh.runCmd('mkdir -p ~/Library/Frameworks/Python.framework/Versions/'))
    print('begin unzip ...',datetime.now())
    print(a_ssh.runCmd('unzip -o -q /vault/3.7.zip -d ~/Library/Frameworks/Python.framework/Versions/'))
    print('unzip finishe.======',datetime.now())

    checkPy3=a_ssh.runCmd("ls ~/Library/Frameworks/Python.framework/Versions/3.7/bin/python3")
    a_ssh.close()
    
    if checkPy3 !='':
        return ("OK") 
    else:
        print(checkPy3)
        return ("Fail")

if __name__ == '__main__':
    result1=InstallPY3_7('172.16.30.48',True)
    # result1=InstallPY3_7('10.42.151.96',True,'gdadmin','gdadmin')
    print('Final result=',result1)




# tar -xzf /vault/3.7.zip -C /vault/3.7_test