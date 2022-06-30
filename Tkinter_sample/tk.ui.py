import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        # root = tk.Tk( )
        super().__init__( width=1000,height=800,bg='gray')
        self.pack_propagate(False)
        # self.master = root
        self.pack()
        
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        # self.hi_there.pack(side="top")
        self.hi_there.place(x=10,y=10)

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy,width=40,height=2)
        # self.quit.pack(side="bottom")
        self.quit.place(x=10,y=100)

        self.txtV1= tk.Variable()
        self.txtV1.set("xxx")
        self.inputbox1=tk.Entry(self , textvariable=self.txtV1)
        # self.inputbox1["textvariable"]=self.txtV1   #we can use this to set , but can't use this to read the text from the Entry.
        print(self.inputbox1["textvariable"])
        self.inputbox1.place(x= 200,y=10)

        for i in range(0,10): 
            # tk.Button(self, text= 'button'+str(i)  ,command= self.bt_Click  ).place(x=10*i,y=200,width=40,height=(i+1) )
            tk.Button(self, text= 'button'+str(i)  ,width=40,height= i ,command= self.bt_Click ,bg= 'green'  ).place(x=10*i,y=200 )

        for i in range(0,10): 
            tk.Button(self, text= 'button 2_ '+str(i)  ,command= self.bt_Click ,bg="green",fg='green'  ).place(x=10*i + 500,y=200,width=40,height=(i+1) )
            # tk.Button(self, text= 'button'+str(i)  ,width=40,height= i ,command= self.bt_Click  ).place(x=10*i,y=200 )

        tk.Label(self,text="""set width , height for a button/label... , if you use tk.button(self,text='xx',height=1)  
        this will not height=1,
        please use button.place(height=xx) it works well.
        dont know why bg='green' dont work.""").place(x=10,y=400)


    def say_hi(self):
        print("hi there, everyone! textinput is:" ,self.txtV1.get(),self.inputbox1["textvariable"])
        self.hi_there.place(width= self.hi_there.winfo_width()+1,height=self.hi_there.winfo_height()+1)

    def bt_Click(self):
        self.quit.place(width= self.quit.winfo_width()+1,height=self.quit.winfo_height()+1)
        print("button clicked")

app = Application()
app.mainloop()