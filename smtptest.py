from smtplib import SMTP
from time import sleep

SMTPSVR = '10.42.222.80'
who = 'wp.li@luxsan-ict.com'
body=f'''\
From:{who}
To:{who}
Subject:test Subject

mail body'''

sendSvr = SMTP(SMTPSVR)
errs = sendSvr.sendmail(who,[who],body)
print(errs)
