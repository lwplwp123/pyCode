import telnetlib

t1 = telnetlib.Telnet("",23)

t1.write("hello")
vread= t1.read_until("lsajfiawef",0.1)

print(vread )
t1.close()


