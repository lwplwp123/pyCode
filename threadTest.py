import threading
from time import sleep , ctime

loops = [4,2]
class ThreadFunc(object):
    def __init__ (self, func,args,name=''):
        self.name=name
        self.func = func
        self.args = args
        print( 'class inited...' , name)
    def __call__ (self): 
        print('args:',self.args)
        print('*args:',*self.args)

        self.func( *self.args)

def loop(nloop,nsec):
    print('start loop' , nloop,'at:',ctime())
    sleep(nsec)
    print ('loop' , nloop,'done at:' , ctime())
def main():
    print('starting main at:',ctime())
    threads =[]
    nloops =range(len(loops))
    for i in nloops:
        t = threading.Thread(target=ThreadFunc(loop,(i,loops[i]),loop.__name__)) #use class object.
        #t = threading.Thread(target= loop,args=(i,loops[i]))  #use just function as Enter point.
        threads.append(t)

        t.start()
    # for i in nloops:     #let all thread go.
        # threads[i].start()
    for i in nloops:     #block until all thread done.
        threads[i].join()
    print('all DONE at:',ctime())

if __name__ =='__main__':
    main()
    

