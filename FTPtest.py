from ftplib import FTP



Host = "10.42.222.202"
Port=21
f=FTP(Host)
f.port=Port
f.login('K0509462' ,'lwplwp123')
f.debugging= 0
f.encoding = 'utf-8'
# w=f.getwelcome()

lst=f.nlst('/Work/WP_Li/test')

#print(lst)
for var in lst:
    print(var)
 

# with open( r'/vault/ftpout.tmp','w+') as newF : 
#     pass
#Download binary file.
f.retrbinary('RETR %s' % '/Work/WP_Li/app_icon2.zip' ,open( r'/vault/ftpout.tmp','wb').write )
print('download finished.')
#upload binary file.
f.storbinary('STOR %s' % '/Work/WP_Li/app_icon2.zip.test' , open( r'/vault/ftpout.tmp','rb')  )
print('upload finished.')

#delete a file.
f.delete('/Work/WP_Li/app_icon2.zip.test')
print('delete server file. finished.')

f.quit()
print(" test finished.".center(40,'-'))