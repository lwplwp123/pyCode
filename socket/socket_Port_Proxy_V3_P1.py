# coding:utf-8

'''
目的:你直接访问我给你的port,就相当于访问了你要的IP,Port.
#过程:你访问我的10088
# 当连上时,第一句话就说IP,Port 格式(IP,port 如果出错就结束,需要连就重新发起) 连上后0.5秒内
# 我回复你一个OK。
client<->P1代理<->P2代理<->Target
# 这里是1级代理。
因为我也不能直接找到目标电脑,所以需要2级代理。
2级代理会主动找我, 我再发IP,Port 给2级代理,他回复OK那就是他准备好了
''' 
from time import ctime,sleep
from socket import *
import threading
import  traceback
import random 

P1Port= 10088
P2Port= 8080
localHost =''
BufSize=1024 
intThread=0
FreeP2Socket:socket = None
lock = threading.Lock()

def getFreePort()->int:
    sck= socket(AF_INET,SOCK_STREAM)
    rnd1=random.randrange(10000,19000)

    for a in range(rnd1,20000):
        rt=sck.connect_ex(('127.0.0.1',a))
        if rt==0:
            sck.close()
        else:
            return a

def oneProxy(SocketAsServer:socket  ):
    global intThread, FreeP2Socket,lock
    intThread+=1
    
    lock.acquire()
    Socket2P2 = FreeP2Socket
    FreeP2Socket=None
    lock.release()
    Socket2P2.setblocking(True)
    SocketAsServer.setblocking(True)
    try: 
        t = threading.Thread(target= replayToClient,args=(Socket2P2,SocketAsServer,)) 
        t.start()
        while True:
            data=SocketAsServer.recv(BufSize) 
            if data:
                Socket2P2.send(data)
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
    global localHost,P1Port,P2Port, BufSize,lock,FreeP2Socket
    Addr =(localHost,P1Port)
    try:
        tcpServer = socket(AF_INET,SOCK_STREAM) #socket(AddressFamily.AF_INET,SocketKind.SOCK_STREAM)
        tcpServer.bind(Addr)  #tcpServer.bind((Host,Port)) 
        tcpServer.listen(5)# 在接受新连接前，允许排队待连接的请求个数，
        tcpServer.setblocking(False)
        print(f"waiting for connect on:{P1Port}.....")
    except:
        print("AsServer2Client listen to ",P1Port," Fail.")
        exit(1)

    while True:
        try:
            tcpCli ,addr2 = tcpServer.accept()
            # sleep(0.5)
            # print('client connect ok.',addr2)
            # pData=tcpCli.recv(BufSize)
            # if not pData:
            #     tcpCli.close()
            #     continue
            # print(pData)
            # tHost,tPort=pData.decode('utf-8',errors='ignor').split(',')
            # tcpCli.send('OK'.encode('utf-8'))
            sleep(0.1)

            t = threading.Thread(target= oneProxy,args=(tcpCli ,))  #use just function as Enter point.
            t.start()
            
        except Exception as e1:
            # print(' 0    exception , ' ,e1)
            sleep(1)

    tcpServer.close()

def AsServer2P2():
    '''永远listen并保持一个空闲连接,随时备用'''
    global localHost,P1Port,P2Port, BufSize,lock,FreeP2Socket
    Addr =(localHost,P2Port)
    try:
        tcpServer = socket(AF_INET,SOCK_STREAM) #socket(AddressFamily.AF_INET,SocketKind.SOCK_STREAM)
        tcpServer.bind(Addr)  #tcpServer.bind((Host,Port)) 
        tcpServer.listen(5)# 在接受新连接前，允许排队待连接的请求个数，
        tcpServer.setblocking(False)
        print(f"waiting for connect on:{P2Port}.....")
    except:
        print("AsServer2P2 listen to ",P2Port," Fail.")
        exit(1)
    while True:
        lock.acquire()
        if not FreeP2Socket: # 没有闲置连接了，要生一个备用
            try:
                FreeP2Socket ,addr2 = tcpServer.accept() 
                print('P2 connect ok.',addr2 ) 
            except Exception as e1:
                # print(' 0    exception , ' ,e1)
                sleep(1)
        lock.release()
        sleep(0.1)


if __name__ == '__main__':
    t = threading.Thread(target= AsServer2Client,args=())  #use just function as Enter point. 
    t.start() 
    AsServer2P2()
 