#coding:utf-8

import time
import subprocess
from sys import stderr, stdout,stdin
import threading

#sample 1 out.readlines() need subProcess finish.
# proc = subprocess.Popen(['ls','/'], stdout=subprocess.PIPE,stderr=subprocess.STDOUT) #send erro also to stdout.
# out=proc.stdout
# print("".join( [ x.decode() for x in  out.readlines()])) #readlines need the process finish then read all lines.

#sample 2  ,every time there is output, then read it.
# proc = subprocess.Popen(['ping','-t','3','127.0.0.1'] ,stdout= subprocess.PIPE,stderr=subprocess.STDOUT)
# # proc = subprocess.Popen(['/usr/local/bin/python3'] ,stdout= subprocess.PIPE,stderr=subprocess.STDOUT)
# out=proc.stdout
# # while proc.poll() == None: 
# #     print("stdout=============")
# #     print(out.readline().decode())
# while out.peek() != b'': 
#     # print("stdout=============")
#     print(out.readline().decode(),end='')

#sample 3 
def readAproc(procOut):
    print("reading process begin....")
    while procOut.peek() != b'':
        #print('peek found ...')
        print(procOut.read(1).decode(),end='')
    print('read process finished.')

# fwe = open("tmpoute",'wb')

# proc = subprocess.Popen(['/usr/local/bin/python3',] ,stdout= subprocess.PIPE,stderr=subprocess.STDOUT,stdin=subprocess.PIPE)
# proc = subprocess.Popen(['ping','-t','3','127.0.0.1'] ,stdout= subprocess.PIPE ,stdin=subprocess.PIPE)
proc = subprocess.Popen(['/vault/cli1',] , stdout= subprocess.PIPE, stderr=subprocess.PIPE,stdin=subprocess.PIPE)
out1=proc.stdout
outErr = proc.stderr 
inpip=proc.stdin

threading.Thread(target=readAproc,args=(out1,)).start()
threading.Thread(target=readAproc,args=(outErr,)).start()

# time.sleep(1)
# inpip.write("abc\r\n".encode())
# inpip.flush()
# time.sleep(1)
# inpip.write("exit\r\n".encode())
# inpip.flush()
while proc.poll() == None:
    in1 = input("")+'\r\n'
    inpip.write( in1.encode())
    inpip.flush()
proc.wait()

# proc.terminate()

#sample 4.
#based on this sample. we can see , after the cmd run ok, the stderr output, then stdout output. this is not what we want.
#we want to read all stdout,stderr realtime.

# fwo = open("tmpout",'wb')
# fwe = open("tmpoute",'wb')
# # fr = open('tmpout','r')
# proc=subprocess.Popen(['/vault/cli1',] , stdout=fwo,stderr=fwe,stdin=subprocess.PIPE,bufsize=1 )
# time.sleep(1)
 
# proc.stdin.write("abc\r\n".encode())
 
# time.sleep(1)
# proc.stdin.write("exff\r\n".encode())
# time.sleep(1)

# proc.stdin.write("exit\r\n".encode())
# # print('fwo.read ',fr.read()) 
