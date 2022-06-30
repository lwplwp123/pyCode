from socket import *
from time import ctime

Host = "localhost"
Port =10087
Addr=(Host,Port)
BufSize=1024

udpServer =socket(AF_INET,SOCK_DGRAM)
udpServer.bind(Addr)

while True:
    print ("waitting a UDP message...")
    data , addr2 = udpServer.recvfrom(BufSize)
    udpServer.sendto('%s  %s' % (ctime(),data) , addr2)
    print ("UDP received:" ,data,addr2)
udpServer.close()

