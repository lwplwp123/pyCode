# failed to ....

from time import sleep
import win32com.client as win32


warn =lambda app:showwarning(app,'Exit?')
RANGE = range(3,8)
def excel():
    app= 'Excel'
    x1 = win32.gencache.EnsureDispatch('%s.Application'% app)
    ss = x1.Workbooks.Add()
    sh =ss.ActiveSheet
    x1.Visible =True
    sleep(1)
    sh.Cells(1,1).Value = 'py is good.'
