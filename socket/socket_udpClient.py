from socket import *
from time import ctime

Host = "localhost"
Port =10087
Addr=(Host,Port)
BufSize=1024


udpCli =socket(AF_INET,SOCK_DGRAM)

while True:
    data = raw_input('please input something to send to UDP server.\n>')
    if not data:
        break
    udpCli.sendto(data,Addr)
    data,addr2 = udpCli.recvfrom(BufSize)
    if not data:
        break
    print("reveived from server:",data,addr2[0],addr2[1])

udpCli.close()


