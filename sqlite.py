import sqlite3
import random
import pprint


conn = sqlite3.connect('test.db')
cursor = conn.cursor()
#list all tables.
allTables=cursor.execute('select * from sqlite_master where type=\'table\' ').fetchall()
# print(cursor.description)
for x in cursor.description:
    print(x[0],'   ',end='')
print('')
# pprint.pprint(allTables)
for  x in allTables:
    for v in x:
        print(v,'   ',end='')
    print('')
print('')

#list all name.
allTables=cursor.execute(r"select name from sqlite_master where type='table' ").fetchall()[0]

if allTables.count('table1')==0:
    cursor.execute('''create table table1 (
        id  INTEGER ,
        name Text,
        value Text
    )''')
    print('Create table result:',cursor.fetchall())

n=random.randint(1,100)

cursor.execute(""" insert into table1 (id,name,value) values (?,?,?) """ ,[n,'name_' +str(n)  ,'value_'+str(n)])
cursor.execute("select * from table1")
# cursor.executemany("insert into users values(?,?)" , [(a,b) for a,b in getABfunc() ])
# cursor.execute("select date('now')")
pprint.pprint(cursor.fetchall())
conn.commit()
# conn.rollback()
conn.close()
