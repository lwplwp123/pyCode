

from ctypes import addressof
from hashlib import new
from logging import exception
from time import ctime,sleep
from socket import *
import threading 
import traceback


'''
#目的,作为P2 server，代理访问172.21.63.154:9500
#工作方式:主动连接 P1 server ，并在需要时代理连接target
client<->P1代理<->P2代理<->Target
''' 

class Mapping:
    targetHost ='172.19.74.244'
    targetPort= 5900
    P1Port= 5901
    P1Host ='10.42.222.206'
    BufSize=1024
    FreeSocket2P1:socket 
    intThread=0
    MainThread:threading.Thread
    
    def __init__ (self, _targetHost,_targetPort,_P1Host,_P1Port):   #类的初始化函数
        self.targetHost=_targetHost
        self.targetPort=_targetPort
        self.P1Host =_P1Host
        self.P1Port=_P1Port
        self.sema_FreeSocket= threading.Semaphore(1)   # 信号量。释放就可以重新建立freeconnection.
        


    def oneProxy(self,SocketAsServer:socket , targetHost:str,targetPort:int ):
       
        IholdFreeSocket=True
        self.intThread+=1
        isWorking:bool=False
        Addr=(targetHost,int(targetPort))
        SocketToServer= socket(AF_INET ,SOCK_STREAM)
        SocketToServer.settimeout(100)
        SocketAsServer.settimeout(100)
        SocketToServer.setblocking(True)
        SocketAsServer.setblocking(True)
        try:
            
            print('will connect to server:',Addr)
            SocketToServer.connect(Addr)
            t = threading.Thread(target= self.replayToClient,args=(SocketToServer,SocketAsServer,)) 
            t.start()
            
            while True:
                data=SocketAsServer.recv(self.BufSize)
                if  isWorking==False:
                    isWorking=True
                    self.FreeSocket2P1=None 
                    self.sema_FreeSocket.release()
                    print('release=====+++one proxy normal')
                    IholdFreeSocket=False

                    SocketToServer.settimeout(600)
                    SocketAsServer.settimeout(600)
                if data:
                    SocketToServer.send(data)
                else: 
                    sleep(1)
                    SocketToServer.close()
                    raise  exception( "oneProxy error socket recv empty.")
        except Exception as E1:
            self.intThread -=1
            if IholdFreeSocket:
                try:
                    self.sema_FreeSocket.release()
                    print('release=====+++ one Porxy exception')
                    self.FreeSocket2P1.close()
                except:
                    pass
                self.FreeSocket2P1=None

            print('oneProxy socket close:', E1  ,' thread count:',self.intThread, 'Addr=',Addr)
            print(traceback.format_exc())
            return

    def replayToClient(self,socketReceive:socket,socketTo:socket):
        #global intThread
        self.intThread+=1
        socketReceive.settimeout(600)#test this.
        try:
            while True:
                data=socketReceive.recv(self.BufSize)
                if data:
                    socketTo.send(data)
                else:
                    # sleep(0.1)
                    raise exception("replayToClient error socket recv empty.")
        except:
            self.intThread -=1
            print('replayToClient socket close: thread count:',self.intThread)
            return

    def Main(self):
        '''
    作为P2 Proxy ,找P1 并保持一个Free socket.
    ''' 

        Addr =(self.P1Host,self.P1Port)
        self.FreeSocket2P1=None
        while True:

            self.sema_FreeSocket.acquire()
            try:
                self.FreeSocket2P1= socket(AF_INET ,SOCK_STREAM)
                self.FreeSocket2P1.setblocking(True) 
                self.FreeSocket2P1.settimeout(60)
                self.FreeSocket2P1.connect(Addr)
                print('connect to P1 ok.',Addr, self.FreeSocket2P1)  
                # sleep(0.01)
                t = threading.Thread(target= self.oneProxy,args=(self.FreeSocket2P1, self.targetHost,int(self.targetPort),))  #use just function as Enter point.
                t.start() 

            except Exception as e1:
                print(' 0    exception , ' ,e1,' Addr=',Addr)
                self.FreeSocket2P1=None
                self.sema_FreeSocket.release()
                print('release=====+++ main exception')
                sleep(3)
  
    def Main_BackThread(self):
        '''run Main in back thread. (no block main thread.)'''
        self.MainThread = threading.Thread(target= self.Main,args=())  #use just function as Enter point.
        self.MainThread.start()

if __name__ == '__main__':
    lstAllGroup:list = []
 
    # lstAllGroup.append( Mapping('127.0.0.1',8888,'10.42.222.206',8888))
    
    lstAllGroup.append( Mapping('172.31.1.50',80,'10.42.222.206',10050))
    lstAllGroup.append( Mapping('10.42.24.213',80,'10.42.222.206',10150))

    # lstAllGroup.append(Mapping('172.31.134.205',5900,'10.42.222.206',6000))
    # lstAllGroup.append(Mapping('172.31.134.146',5900,'10.42.222.206',6001))
    # lstAllGroup.append( Mapping('172.31.167.114',5900,'10.42.222.206',6002))
    # lstAllGroup.append(Mapping('172.19.74.244',5900,'10.42.222.206',6003))
    # lstAllGroup.append(Mapping('172.19.74.117',5900,'10.42.222.206',6004))
    # lstAllGroup.append( Mapping('172.17.73.16',5900,'10.42.222.206',6005))
    # lstAllGroup.append( Mapping('172.19.20.67',5900,'10.42.222.206',6006))


    for c in lstAllGroup:
        c.Main_BackThread()
        sleep(0.2)

    while True:
        for c in lstAllGroup:
            print(c.targetHost, "is Alive:", c.MainThread.isAlive())
        print('----'.center(40,"*"))
        sleep(30)
