
import os,sys

newPath=os.path.join(os.environ['HOME'],'Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages')
sys.path.append(newPath)
import psutil

# disklst=['/System/Volumes/Data','/Volumes/HedgehogRepo']
disks=psutil.disk_partitions( all=False)
for x in disks:
    Apart=psutil.disk_usage(x.mountpoint)
    print(x.mountpoint,str.format('{:.2f}GB', Apart.total/1024/1024/1024),'Free:{:.2f}GB'.format(Apart.free/1024/1024/1024),' used:{:.2f}%'.format(Apart.percent))

c1=psutil.virtual_memory()
print(type(c1),c1, c1.used,c1.total , 'used:{:.2f}%'.format(100*c1.used/c1.total))

