#  coding:utf-8

from multiprocessing.connection import Connection
import time
 

from multiprocessing import Process, Pipe

def LongJob(pipe:Connection):
    cmd="" 
    while cmd != 'exit':
        cmd = pipe.recv()
        print('-----server read cmd:'+cmd)
        pipe.send('I am server, and I got comd:'+cmd)
    print('Server have got cmd exit , and terminate.'.center(70,'='))

if __name__ == '__main__':
    # (con1, con2) = Pipe()
    # sender = Process(target = send, name = 'sendxx', args = (con1, ))
    # sender.start()
    # print ("con2 got: %s" % con2.recv())#从send收到消息
    # con2.close()
    # (parentEnd, childEnd) = Pipe()
    # child = Process(target = LongJob, name = 'talkxx', args = (childEnd,))
    # child.start()
    # print('parent got:', parentEnd.recv())
    # parentEnd.send({x * 2 for x in 'spam'})
    # child.join()
    # print('parent exit')

    (parentEnd, childEnd) = Pipe()
    child = Process(target = LongJob, name = 'LongJobProcessName', args = (childEnd,))
    child.start()
    while child.is_alive():
        aCmd=input("please input a cmd for server:")
        if child.is_alive() ==False:
            print("server have stope.")
            break
        parentEnd.send(aCmd)
        time.sleep(0.01)
        print(f'server responsed:{ parentEnd.recv()}\r\n') 
        




