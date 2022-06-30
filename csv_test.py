import csv
 

data= (
    (4,'web clients and servers','base64,urllib'),
    (5,'web programing:cgi & WSGI','cgi,time,wsgiref'),
    (6,'Web services','urllib,twython'),
)

print('****** Writing csv Data')
with  open('bookdata.csv','w') as f:
    write = csv.writer(f)
    for row in data:
        write.writerow(row)
print('****review of saved data')
with open('bookdata.csv','r') as f:
    reader = csv.reader(f)
    # for Num,title,modpkgs in reader:
    #     print(Num,title,modpkgs)
    for a in reader:
        print (a)
