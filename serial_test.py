
import datetime
import json
from random import randint
import re
import os,io
import threading
from time import sleep
import sys,paramiko,plistlib
from paramiko.client import AutoAddPolicy, SSHClient
import urllib3,urllib
import base64 

import serial,serial.serialutil

ser=serial.Serial()
# ser.baudrate = 115200
ser.port='/dev/cu.usbserial-UUT1A'
ser.bytesize = serial.serialutil.EIGHTBITS
ser.parity = serial.serialutil.PARITY_NONE
ser.stopbits = serial.serialutil.STOPBITS_ONE
ser.open()

# ser.write('good,please ensure this is correct.'.encode('utf-8'))
for i in range(1,300):
    sleep(1)
    ret=ser.read_all()
    print( ret.decode('utf-8'))
    print(i)

ser.close()
 
# class SerialBase(io.RawIOBase):   #from serialutil.py
# def __init__(self,
#              port=None,
#              baudrate=9600,
#              bytesize=EIGHTBITS,
#              parity=PARITY_NONE,
#              stopbits=STOPBITS_ONE,
#              timeout=None,
#              xonxoff=False,
#              rtscts=False,
#              write_timeout=None,
#              dsrdtr=False,
#              inter_byte_timeout=None,
#              exclusive=None,
#              **kwargs): 