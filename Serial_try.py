# this is just for readme.
# this 3th is reading page:203 list vs set 
# page 215 list vs dictionary


import os
import sys
import serial
import serial.tools.list_ports ,serial.tools.list_ports_common
import serial.tools.list_ports_osx
import time
 
aSer = serial.Serial(port='/dev/cu.usbserial-UUT1A')
# aSer.open()
print('isopen=',aSer.isOpen())
for i in range(1,3):
    aSer.write(  f'sending {i} ,see it.\r\n'.encode())
    aSer.write(  f'sending {i*2} ,see it.\r\n'.encode())
    time.sleep(3)
    ret=aSer.read_all().decode(encoding='utf-8')
    print('read :',ret)
    time.sleep(0.03)

aSer.close()

aSer.open()
str1=aSer.read_all()
print('read all====')
print(str1)

