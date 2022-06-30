from tkinter import Tk

from time import sleep
import win32com.client as win32
from tkinter.messagebox import showinfo,showwarning,showerror

warn=lambda app:showwarning(app,'Exit?')
range1=range(3,8)

def excel():
    app='Excel'
    xl = win32.gencache.EnsureDispatch(f'(app).Application')
    ss =xl.Workbooks.Add()
    sh=ss.ActiveSheet
    xl.Visible = True
    sleep(1)
    sh.Cells(1,1).Value = f'Python-to-(app) Demo'
    sleep(1)
    for i in range1:
        sh.Cells(i,1).Value = 'Line '+ i
        sleep(1)
    sh.Cells(i+2,1).Value = "Th-th that's all folks!"

    warn(app)
    ss.Close(False)
    xl.Application.Quit()

if __name__=='__main__':
    Tk().withdraw()
    excel()
