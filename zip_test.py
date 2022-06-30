

import pprint


rows=[]
rows.append ([1,2,3,4,5])
rows.append(['r2.1','r2.2','r2.3','r2.4'])
rows.append(['r3.1','r3.2','r3.3','r3.4','r3.5'])

tout = zip(*rows)
pprint.pprint(rows) 
print('after tran'.center(50,'-')) 
pprint.pprint(list(tout))
