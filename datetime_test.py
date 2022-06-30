import datetime
import time
import math

def format_time(time_str)->str:
    ''' format time SS or MM:SS string to HH:MM:SS
    '''
    tlen = len(time_str)
    if tlen<3:
        format1='%S'
    elif tlen<6:
        format1='%M:%S'
    else:
        format1= '%H:%M:%S'
    time_str = time.strftime('%H:%M:%S',time.strptime(time_str, format1))
    return time_str


def time2sec(time_str)->int:
    time_str= format_time(time_str)
    (h,m,s) = time_str.split(':')
    ses = int(s) + int(m)*60 + int(h)*60*60
    return ses

def sort2(v):
    return abs(v[1])

def findCloseTime(time1:str,lookingInto:list)->str:
    t1 = time2sec(time1)
    diff = [(x, time2sec(x) - t1 )for  x in lookingInto]
    diff.sort(  key= sort2 )
    return  diff[0][0]

def getDateTimeStr()->str:
    # return  datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S.%f") 
    return str(datetime.datetime.now()) 

def getDateTimeStr2()->str:
    # return  datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S.%f") 
    tt=datetime.datetime.now().timetuple()
    return f'{tt.tm_yday}-{tt.tm_mon}-{tt.tm_mday} {tt.tm_hour}:{tt.tm_min}:{tt.tm_sec}'

# lookinto = ['12:21','3:12','32','8:32','10:55','2:20']
# t1='2:23'
# t2=format_time(t1)
# t2=findCloseTime(t1,lookinto)
# print(t2)

print ('Begin  ===',getDateTimeStr())

for i in range(100000):
    s=getDateTimeStr()
    # s= str(datetime.datetime.now()) 

print ('End ======'   , getDateTimeStr())
 
for i in range(100000):
    s=getDateTimeStr2()
    # s= str(datetime.datetime.now())  
print ('End 2======'   , getDateTimeStr())

time_x = datetime.now() + datetime.timedelta(seconds=100)
 



