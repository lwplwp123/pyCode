#-*- coding: utf-8 -*-
#lock thread sync.   线程同步 debug mode not work ok, run mode is ok.

import atexit
import random
import threading
import time

 

sema=threading.Semaphore(3)


def loop(*arg):
    sema.acquire()
    print('thread working...' , arg)
    time.sleep(2)
    sema.release()

def main ():

    for a in range(1,10):
        sema.acquire()
        #threading.Thread(target=loop,args=(a,)).start()
        print(a)

    

@atexit.register
def atexit1212():
    print("all done....")
    print(f"in Main thread, active_count={threading.active_count()}")

if __name__ == "__main__":
     main()
     

