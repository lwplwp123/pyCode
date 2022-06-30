from socket import *
from time import ctime

Host =''
Port= 1111
BufSize=1024
Addr =(Host,Port)
tcpServer = socket(AF_INET,SOCK_STREAM) #socket(AddressFamily.AF_INET,SocketKind.SOCK_STREAM)
tcpServer.bind(Addr)  #tcpServer.bind((Host,Port)) 
tcpServer.listen(5)


while True:
    print("waiting for connect......")
    tcpCli ,addr2 = tcpServer.accept()
    print( '...Connected from :' ,addr2)
    while True:
        print("will receive")
        data = tcpCli.recv(BufSize)
        print("After receive")
        if not data:
            print("Socket client broken!")
            break
        print( "received:" ,data.decode('utf-8'))
        tcpCli.send(('[%s] %s' % (ctime(),data.decode('utf-8'))).encode('utf-8'))
    tcpCli.close()
tcpServer.close()

