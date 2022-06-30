#use MySQLdb , this need install mysqlClient. it's quite big.
# so I just test db with pyMysql.

import sqlite3

def CreateDB(): 
    cn=sqlite3.connect(database='/vault/pytest.sqlite3')
    cur=cn.cursor()
    cur.execute('create table users(login varchar(8) , userid integer)')
    cur.close()
    cn.commit()
    cn.close()
def InserDB():
    cn=sqlite3.connect(database='/vault/pytest.sqlite3')
    cur=cn.cursor()

    cur.execute('insert into users values("john3",100),("jane3",110)')
    # cur.execute('insert into users values("jane",110)')

    cur.close()
    cn.commit()
    cn.close()
def SelectDB():
    cn=sqlite3.connect(database='/vault/pytest.sqlite3')
    cur=cn.cursor()

    cur.execute('select * from users')
    print('total rows=',cur.rowcount )
    for aUser in cur.fetchall():
        print(aUser)

    cur.close()
    cn.commit()
    cn.close()

if __name__ == '__main__':
    # CreateDB()
    # InserDB()
    SelectDB()
