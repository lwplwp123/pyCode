# coding:utf-8

'''
目的:你直接访问我给你的port,就相当于访问了你要的IP,Port.
#过程:你访问我的10088
# 当连上时,第一句话就说IP,Port 格式(IP,port 如果出错就结束,需要连就重新发起)
# 我回复你一个OK。接下来就交给SSH来处理了
# 然后我就把这个连接和你要的IP,port 绑定到一起。直到有一方断开链接结束。
跟V1 不同之处就是,v1 重新开了一个port等你来连,V2 就用当前这个链接了。
''' 
from time import ctime,sleep
from socket import *
import threading
import  traceback
import random

localPort= 10088
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

 

def oneProxy(SocketAsServer:socket , targetHost:str,targetPort:int ):
    global intThread
    intThread+=1
    
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


def AsServer2Client():
    '''
作为ProxServer,接受一个客户端的socket请求
'''
    Addr =(localHost,localPort)
    tcpServer = socket(AF_INET,SOCK_STREAM) #socket(AddressFamily.AF_INET,SocketKind.SOCK_STREAM)
    tcpServer.bind(Addr)  #tcpServer.bind((Host,Port)) 
    tcpServer.listen(5)# 在接受新连接前，允许排队待连接的请求个数，
    tcpServer.setblocking(False)
    print(f"waiting for connect on:{localPort}.....")
    while True:
        try:
            tcpCli ,addr2 = tcpServer.accept()
            sleep(0.3)
            print('connect ok.')
            pData=tcpCli.recv(BufSize)
            if not pData: continue
            print(pData)
            tHost,tPort=pData.decode('utf-8',errors='ignor').split(',')
            freePort=getFreePort()
            print(tHost,tPort,freePort,'-----------------')
            tcpCli.send('OK'.encode('utf-8'))
            sleep(0.1)
            t = threading.Thread(target= oneProxy,args=(tcpCli, tHost,int(tPort),))  #use just function as Enter point.
            t.start()
            
        except Exception as e1:
            # print(' 0    exception , ' ,e1)
            sleep(1)

    tcpServer.close()


if __name__ == '__main__':
    AsServer2Client()


