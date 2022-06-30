# coding:utf-8

'''
目的:你直接访问我给你的port,就相当于访问了你要的IP,Port.
#过程:你访问我的10088
# 当连上时,第一句话就说IP,Port 格式(IP,port 如果出错就结束,需要连就重新发起)连上后0.5秒内
# 我回复你一个OK。
client<->P1代理<->P2代理<->Target
# 这里是2级代理。
我可以链接到target,也可以连到P1级代理。我会主动连到P1.
当P1发给我消息IP,Port时,我就把当前socket 和target 绑定到一起
并重新发起一个到P1的连接,总是保持一个空闲的连接。

''' 
from glob import glob
from time import ctime,sleep
from socket import *
import threading
import  traceback
import random
 
P1Port= 8080
P1Host ='10.42.152.61'
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

def oneProxy(SocketAsServer:socket , targetHost:str,targetPort:int ):
    global intThread
    intThread+=1
    
    Addr=(targetHost,int(targetPort))
    SocketToServer= socket(AF_INET ,SOCK_STREAM)
    SocketToServer.setblocking(True)
    SocketAsServer.setblocking(True)
    SocketToServer.settimeout(600)
    SocketAsServer.settimeout(600)
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
                SocketToServer.close()
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


def Conn2P1():
    '''
作为P2 Proxy ,找P1 并保持一个Free socket.
'''
    global P1Port,P1Host,BufSize

    Addr =(P1Host,P1Port) 
    FreeSocket2P1:socket=None

    while True:
        if FreeSocket2P1==None:
            try:
                FreeSocket2P1= socket(AF_INET ,SOCK_STREAM)
                FreeSocket2P1.setblocking(True) 
                FreeSocket2P1.settimeout(60)
                FreeSocket2P1.connect(Addr)
                print('connect to P1 ok.',FreeSocket2P1) 
                pData=FreeSocket2P1.recv(BufSize)
                print(pData)
                tHost,tPort=pData.decode('utf-8',errors='ignor').split(',') 
                FreeSocket2P1.send('OK'.encode('utf-8'))
                sleep(0.1)
                t = threading.Thread(target= oneProxy,args=(FreeSocket2P1, tHost,int(tPort),))  #use just function as Enter point.
                t.start()
                FreeSocket2P1=None 
            except Exception as e1:
                print(' 0    exception , ' ,e1,)
                FreeSocket2P1=None
                sleep(3)
        else:
            sleep(0.5)

if __name__ == '__main__':
    Conn2P1()


