

from time import ctime,sleep
from socket import *
import threading
from tkinter import E 
#目的，你访问我的10086，就等于访问了10.42.24.213:80
targetHost ='10.42.151.26'
targetPort= 22
localPort= 80
localHost =''
BufSize=1024

intThread=0

def oneTCPPip(SocketAsServer:socket):
    global intThread
    intThread+=1
    Addr=(targetHost,targetPort)
    SocketToServer= socket(AF_INET ,SOCK_STREAM)
    try:
        SocketToServer.connect(Addr)
        SocketAsServer.setblocking(True);
        SocketToServer.setblocking(True);
        t = threading.Thread(target= replayToClient,args=(SocketToServer,SocketAsServer,)) 
        t.start() 
        while True:
            data=SocketAsServer.recv(BufSize)
            if data:
                SocketToServer.send(data)
                print('toServer-->',SocketToServer.getpeername(),':',data)
            else: 
                # sleep(0.1)
                raise "error socket recv empty."
    except:
        intThread -=1
        print('oneTCPPip socket close: thread count:',intThread)
        return

def replayToClient(socketReceive:socket,socketTo:socket):
    global intThread
    intThread+=1
    try:
        while True:
            data=socketReceive.recv(BufSize)
            if data:
                socketTo.send(data)
                print('toCleint-->',socketTo.getpeername(),':',data)
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
tcpServer.listen(5)
 
while True:
    print("waiting for connect......")
    tcpCli ,addr2 = tcpServer.accept()
    print( '...Connected from :' ,addr2)
    print('total thread count:',intThread)
    t = threading.Thread(target= oneTCPPip,args=(tcpCli,))  #use just function as Enter point.
    t.start()  
tcpServer.close()

