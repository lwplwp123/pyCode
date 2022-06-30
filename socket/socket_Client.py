from socket import *
from time import sleep
Host = "172.16.30.48"
Port = 8020
BufSize = 1024
Addr=(Host,Port)

tcpCli= socket(AF_INET ,SOCK_STREAM)
tcpCli.connect(Addr)
while True:
    data = input("please input something , this will send to server.\n>")
    if not data:
        break
    data += "\r\n"
    tcpCli.send(data.encode('utf-8'))
    data=tcpCli.recv(BufSize)
    if not data:
        break
    print (data.decode('utf-8'))
tcpCli.close() #shutdown 关闭连接 ; close 关闭套接字

# ~/Library/Frameworks/Python.framework/Versions/3.7/bin/python3 /vault/sck1.py
