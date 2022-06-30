#-*- coding: utf-8 -*-
#lock thread sync.   线程同步 debug mode not work ok, run mode is ok.

import atexit
import random
import threading
import time

 
class CleanOutputSet(set):
    def __str__(self):
        return ','.join( x for x in self)

lock = threading.Lock()

loops =(random.randrange(2,8) for x in range(random.randrange(3,7))) # 3~6 threads. 2~7 seconds for each
remaining = CleanOutputSet()
def loop(nsec:int):
    myname= threading.current_thread().name
    
    lock.acquire()
    remaining.add(myname)
    print (time.ctime(), 'started' , myname,nsec,lock)
    lock.release()

    # with lock:
    #     remaining.add(myname)
    #     print (time.ctime(), 'started' , myname,nsec,lock)
    
    time.sleep(nsec)
    with lock:
        print( remaining)
        remaining.remove(myname)
        print(f'current thread object active_count={threading.active_count()}   enumerate(thread list)={threading.enumerate()}')
        print ( time.ctime(),myname , 'completed ' , nsec)

def main ():
    for a in loops:
        threading.Thread(target=loop,args=(a,)).start()

    

@atexit.register
def atexit1212():
    print("all done....")
    print(f"in Main thread, active_count={threading.active_count()}")

if __name__ == "__main__":
     main()
     

