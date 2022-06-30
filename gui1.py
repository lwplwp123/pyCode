
from functools import partial as pto
from tkinter import Tk,Button,X
from tkinter.messagebox import showinfo,showwarning,showerror

Warn = 'warning'
Crit = 'crit'
Regu = 'regu'

Signs = {'do not enter': Crit,
'railroad crossing':Warn,
'55\nspeed limit':Regu,
'wrong way':Crit,
'merging traffic':Warn,
'one way':Regu,
}

critCB = lambda:showerror('Error','Error Button Pressed!')
warnCB = lambda:showwarning('warning','Warning Button Pressed!')
infoCB = lambda:showinfo('Info','Info Button Pressed!')

top=Tk()
top.title('Road Signs')
Button(top,text='Quit',command=top.destroy,bg='green',fg='red').pack()  #top.quit also work for MAC os, but not work for Win(python3.4)

Mybutton=pto(Button,top)
CritButton = pto(Mybutton,command=critCB,bg='white',fg='red')
WarningButton =pto(Mybutton,command=warnCB,bg='goldenrod1')
ReguButton=pto(Mybutton,command=infoCB,bg='white')

for eachSign in Signs:
    signType = Signs[eachSign]
    cmd='%sButton(text=%r%s).pack(fill=X,expand=True)' % (signType.title(),eachSign,'.upper()' if signType == Crit else '.title()')
    print(cmd)
    eval(cmd)

top.mainloop()


