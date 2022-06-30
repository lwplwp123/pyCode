import time


def f1(i:int) :
    la1 = [1,2]
    la1.append(3)
    return i,la1

a=3
b,lsttmp= f1(a)
print(b,lsttmp)

def f2(i:int,l1:list)->int:
    l1.append(4)
    return   i +1,l1

v=35
vl=[1]
v2,l2=f2(v,vl)
print(v,vl,v2,l2)
