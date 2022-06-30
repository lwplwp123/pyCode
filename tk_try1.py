
import tkinter

# f1= tkinter.Frame( width=800,height=300)
# f1.mainloop()
 
# root = tkinter.Tk()
# root.mainloop()


from tkinter import ttk

root = tkinter.Tk()

style = ttk.Style()
style.map("C.TButton",
    foreground=[('pressed', 'red'), ('active', 'blue')],
    background=[('pressed', '!disabled', 'black'), ('active', 'white')]
    )

colored_btn = ttk.Button(text="Test", style="C.TButton").pack()

root.mainloop()




