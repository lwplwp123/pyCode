import imp


import sys

globalP1=3

def funcTestG1():
    global globalP1
    globalP1 +=1;
    print(globalP1)
    print('my file name:', sys.path[0],sys.path[1],sys.path[2] ,sys.path[0],sys._getframe(0).f_code.co_filename,__file__)

class Ctest1:
    classG1=1
    def printSelf(self,N):
        self.classG1+=1
        print('Ctest1 print:',self.classG1,'you input is :',N)

