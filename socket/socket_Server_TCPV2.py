#this need client always send a string with crlf. not good.
#after deal one message, socket broken...

from SocketServer import TCPServer as TCP, StreamRequestHandler as SRH
from time import ctime



Host =''
Port  =10086
Addr = (Host,Port)

class MyHandler(SRH):
    def handle(self):
        print('..connected from :',self.client_address )
        data = self.rfile.readline()
        self.wfile.write('%s  %s' % (ctime(),data))
        print("return data for client",data )
tcpServer= TCP(Addr,MyHandler)
print ('waitting for a connection....')
tcpServer.serve_forever()




