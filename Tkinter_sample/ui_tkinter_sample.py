import tkinter as tk

#新建一个tk界面
def creatATK():
    root = tk.Tk()
    return root
#运行一个tk界面
def runTK(aTK):
    aTK.mainloop()

#将控件放在其他控件之后,必须先放其他控件后才能after
def packAfterControl(currentControl,afterControl):
    currentControl.pack(after=afterControl)

#将控件放在其他控件之前,必须先放其他控件后才能before
def packBeforeControl(currentControl,beforeControl):
    currentControl.pack(before =beforeControl)

#控件对其方式，n顶对齐，s底对齐，w左对齐，e右对齐
def packAnchor(aControl,aside='top/bottom/left/right'):
    dic_anchor = {"top":tk.TOP,"bottom":tk.BOTTOM,"left":tk.LEFT,"right":tk.RIGHT}
    if aside not in dic_anchor.keys():
        aControl.pack("UNKNOW_aside")
    else:
        aControl.pack(side=dic_anchor[aside])

#define a button
def aButton(aTK,btName,btClickCommand):
    bt = tk.Button(aTK, text =btName, command = btClickCommand)
    return bt

#define a label
def aLabel(aTK,atext):
    lab = tk.Label(aTK, text=atext)
    return lab

#define a canvas
def aCanvax(aTK,awidth=500,aheight=500 ,abg='white'):
    cv = tk.Canvas(aTK, width=awidth, height=aheight, bg=abg)
    return cv

# line − 创建线条/多边形,x0,y0,x1,y1.....输入一个有序整数列表必须x,y配对使用
def aCanvas_line(cv,list1=[1, 1, 2, 2, 3,3,4,4,5,6,7,8,100,120]):
    cv.create_line(list1)

#oval − 创建一个圆,只设置4个值就OK
def aCanvas_oval(cv,list=[10,10,50,50]):
    cv.create_oval(list)

# 创建一个矩形，坐标为(10,10,110,110)
def aCanvas_rectangle(cv,list=[10,10,110,110]):
    cv.create_rectangle(list)

#文本框用来让用户输入一行文本字符串。你如果需要输入多行文本，可以使用 Text 组件。bd边框的大小，默认为 2 个像素
def aEntry(aTK,awidth=20,abd=5):
    E1 =tk.Entry(aTK, width=awidth,bd=abd)
    return E1



if __name__== "__main__":
    atk = creatATK()
    aE1 = aEntry(atk,50,5)
    packAnchor(aE1,"left")

    cv = tk.Canvas(atk, width=500, height=400, bg='red')
    cv.create_line(0,0,100,100,100,200,200,200) 
    packAnchor(cv,'top')
    runTK(atk)