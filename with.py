
import os
import re

f = os.popen('who','r')
for strline in f:
    print (strline.replace('\n',''))
f.close()

with os.popen('who','r') as f:
    for l1 in f:
        print(l1)

isbn = {
    'a':'value of a',
    'b':'value of b',
    'c':'value of c'
}

for v in isbn:
    print ('the key is :%s' % v)

import random
loops= ( 3 for x in range( random.randrange(3,7)))
# loops = xrange(2,7)
for a in loops:
    print (a)

print ("---------")
a=( random.randrange(1,11) for x in range(1,5))
for v in a:
    print (v)
print ('=====')
 

