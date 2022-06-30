
#failed.
from smtplib import SMTP
s = SMTP('10.42.222.55') 
s.set_debuglevel (1)
s.sendmail( 'wp.li@luxsan-ict.com','wp.li@luxsan-ict.com','message is here')

