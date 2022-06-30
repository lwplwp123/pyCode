 
import pexpect.pxssh
 
ssh1 = pexpect.pxssh.pxssh() 
ssh1.login('10.42.151.96','gdadmin','gdadmin')
ssh1.sendline('ls -l /vault/')
ssh1.prompt()

ret=ssh1.before.decode('utf-8','ignore')
aft=ssh1.after.decode('utf-8','ignore')
print(ret)
print('after:',aft)
ssh1.close()
