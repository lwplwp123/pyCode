# coding:utf-8

'''
目的:你直接访问我给你的port,就相当于访问了你要的IP,Port.
#过程:你访问我的10086
# 当连上时,第一句话就说IP,Port 格式(IP,port 如果出错就结束,需要连就重新发起)
# 我回复你一个端口号,你要在3秒内来连这个端口,否则就过时了。
# 连上后我就把这个新连接和你要的IP,port 绑定到一起。直到有一方断开链接结束。
'''

from time import ctime,sleep
from socket import *
import threading
import  traceback
import random

localPort= 10086
localHost =''
BufSize=1024
intThread=0

def getFreePort()->int:
    sck= socket(AF_INET,SOCK_STREAM)
    rnd1=random.randrange(10000,19000)

    for a in range(rnd1,20000):
        rt=sck.connect_ex(('127.0.0.1',a))
        if rt==0:
            sck.close()
        else:
            return a



def oneProxy(targetHost:str,targetPort:int, proxyPort:int,timeoutSec:int = 3):
    global intThread
    intThread+=1
    sckLinsten=socket(AF_INET,SOCK_STREAM)
    sckLinsten.bind(('',proxyPort))
    sckLinsten.listen()
    sckLinsten.setblocking(False)
    
    iwaitSec=0
    while True:
        try:
            SocketAsServer,addr2=sckLinsten.accept()
            break
        except:
            if iwaitSec >timeoutSec:
                print('client connect time out,' , iwaitSec )
                return
            iwaitSec+=1
            sleep(1)
    
    print('client connect ok in time ',iwaitSec ,' address:', addr2 )
    Addr=(targetHost,int(targetPort))
    SocketToServer= socket(AF_INET ,SOCK_STREAM)
    SocketToServer.setblocking(True)
    SocketAsServer.setblocking(True)
    try:
        SocketToServer.connect(Addr)
        t = threading.Thread(target= replayToClient,args=(SocketToServer,SocketAsServer,)) 
        t.start() 
        while True:
            data=SocketAsServer.recv(BufSize) 
            if data:
                SocketToServer.send(data)
            else: 
                sleep(1)
                print(data)
                raise "error socket recv empty."
    except Exception as E1:
        intThread -=1
        print('oneProxy socket close:', E1  ,' thread count:',intThread)
        print(traceback.format_exc())
        return

def replayToClient(socketReceive:socket,socketTo:socket):
    global intThread
    intThread+=1
    try:
        while True:
            data=socketReceive.recv(BufSize)
            if data:
                socketTo.send(data)
            else:
                # sleep(0.1)
                raise "error socket recv empty."
    except:
        intThread -=1
        print('replayToClient socket close: thread count:',intThread)
        return

BufSize=1024
Addr =(localHost,localPort)
tcpServer = socket(AF_INET,SOCK_STREAM) #socket(AddressFamily.AF_INET,SocketKind.SOCK_STREAM)
tcpServer.bind(Addr)  #tcpServer.bind((Host,Port)) 
tcpServer.listen(5)# 在接受新连接前，允许排队待连接的请求个数，
tcpServer.setblocking(False)
print(f"waiting for connect on {localPort}......")
while True:
    try:
        tcpCli ,addr2 = tcpServer.accept()
        print('client connect ok.',addr2)
        sleep(0.2)
        pData=tcpCli.recv(BufSize)
        if not pData: continue
        print(pData)
        tHost,tPort=pData.decode('utf-8',errors='ignor').split(',')
        freePort=getFreePort()
        t = threading.Thread(target= oneProxy,args=(tHost,int(tPort), freePort,10,))  #use just function as Enter point.
        t.start()
        tcpCli.send(str(freePort).encode('utf-8'))
        tcpCli.close()
    except Exception as e1:
        # print(' 0    exception , ' ,e1)
        sleep(0.3)

tcpServer.close()

