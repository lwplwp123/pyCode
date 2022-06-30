# coding:utf-8

import paramiko
server='127.0.0.1'
user='A'
pwd='1234'

server='10.42.56.24'
user='gdadmin'
pwd='gdadmin'


# ssh = paramiko.SSHClient() #create ssh object
# # 允许连接不在know_hosts文件中的主机
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# # 连接服务器
# ssh.connect(hostname=server, port=22, username=user, password=pwd)

# stdin,stdou,stderr = ssh.exec_command('ls /vault/logTE/')
# result = stdou.read() # get result.
# print(str(result,encoding='utf-8'))
# ssh.close()


# test2
#SSHClient()里有个transport变量,是用于获取连接，我们也可单独的获取到transport变量，然后执行连接操作

transport = paramiko.Transport((server, 22))
transport.connect(username=user, password=pwd)

ssh = paramiko.SSHClient()
ssh._transport = transport

stdin, stdout, stderr = ssh.exec_command('ls /vault/logTE/')
print (str(stdout.read(),encoding='utf-8'))

ssh.get_transport()

transport.close()


